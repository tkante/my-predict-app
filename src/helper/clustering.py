import pandas as pd
import numpy as np
from sklearn.cluster import KMeans, DBSCAN
from scipy.sparse.csgraph import connected_components

def dissolve_overlap(data, id='cluster'):
    s = data.geometry
    overlap_matrix = s.apply(lambda x: s.intersects(x)).values.astype(int)
    n, ids = connected_components(overlap_matrix)
    new_data = data.reset_index(drop=True)
    new_data[id] = ids
    new_data = new_data.dissolve(by=id, aggfunc='sum')
    return new_data.reset_index()

# DBSCAN hotspots
def dbscan_hotspots(data, distance, min_samp, sf, cluster_col, district_col, district=None, weight=None):
    # Create data and fit DBSCAN
    d2 = data.reset_index(drop=True)
    if weight is None:
        weight = 'weight'
        d2[weight] = 1
    xy = pd.concat([d2.geometry.x,d2.geometry.y],axis=1)
    db = DBSCAN(eps=distance, min_samples=int(np.ceil(min_samp)))
    db.fit(xy,sample_weight=d2[weight])
    max_labs = max(db.labels_)
    data[cluster_col] = db.labels_ + 1
        
    # Now looping over the samples, creating buffers
    # and return geopandas buffered DF
    res_buff = []
    sf2 = [weight] + sf

    for i in range(max_labs+1):
        if district is not None:
            sub_dat1 = d2[(db.labels_ == i) & (d2[district_col].isin(district))].copy()
        else:
            sub_dat1 = d2[(db.labels_ == i)].copy()
        sd = sub_dat1[sf2].sum().to_dict()
        sub_dat2 = sub_dat1[sub_dat1.index.isin(db.core_sample_indices_)].copy()
        sub_dat2[cluster_col] = i
        sub_dat2.geometry = sub_dat2.buffer(distance)
        sub_dat2 = sub_dat2.dissolve(cluster_col)
        sub_dat2[cluster_col] = i
        for k,v in sd.items():
            sub_dat2[k] = v
        sub_dat2 = sub_dat2[[cluster_col] + list(sd.keys()) + ['geometry']]
        res_buff.append(sub_dat2.copy())
    fin_file = pd.concat(res_buff).reset_index(drop=True)
    dis_file = dissolve_overlap(fin_file, cluster_col)
    dis_file = dis_file.to_crs(4326)
    dis_file.loc[:, 'geometry'] = dis_file.geometry.apply(lambda x: x.simplify(0.0001))
    return dis_file, data