import os
import folium
from folium import Map, FeatureGroup, GeoJson, LayerControl, Popup
from folium.plugins import HeatMap
import json
from pandas import DataFrame
from typing import List
import numpy as np
import matplotlib as mpl


def heat_map(df:DataFrame, category_col:str, lat:str, lng:str, categories:List[str], path:str) ->None:
    data = df.copy(deep=True)
    # data = df.dropna(subset=[lat, lng], axis=1)
    print("Data")
    print(data.head(2))
    location = [data[lat].median(), data[lng].median()]
    m = Map(location=location, zoom_start= 11)
    for category in categories:
        t_df = data[data[category_col] == category]
        feature_group = FeatureGroup(category)
        HeatMap(t_df[[lat, lng]].values).add_to(feature_group)
        feature_group.add_to(m)
    LayerControl().add_to(m)
    m.save(os.path.abspath(f"{path}/heatmap_data.html"))
    return None

def feature_tooltips(probs, occurrences, target, update_on):
    # cmap = mpl.cm.YlOrRd
    try:
        if probs <=0.3:
            cmap = mpl.cm.RdBu_r
            occurrences = 0
            probs = 0.1
        else:
            cmap = mpl.cm.YlOrRd
    except:
        occurrences = 0
        probs = 0.1
    
    color = mpl.colors.to_hex(cmap(probs))

    if probs <= 0.33:
        risk = 'Risque Faible'
    elif 0.33 < probs <= 0.55:
        risk = 'Risque Singificatif'
    else:
        risk='Risque élevé' 
        
    html_ = f"""<div class="card col " style="border-radius:6px;border-top: 6px solid {color};">
                    <div class="card-body">
                         <div style='display:flex;justify-content:space-between'">
                             <h6 class="card-title mb-4" style="font-size: 14px;">Niveau de risque:</h6>
                             <h6 class="card-title mb-1" style="font-size: 14px;color: {color}">{risk}<br></h6>
                         </div>
                    </div>
                    <div class="table-responsive">
                         <table class="table align-middle table-nowrap mb-0">
                             <thead>
                                 <tr>
                                     <th scope="col" >Evénement cible</th>
                                     <th scope="col">Prob (%)</th>
                                     <th scope="col">Incidents (-7 jours)</th>
                                 </tr>
                             </thead>
                             <tbody>
                                 <tr>

                                     <td>{target}</td>
                                     <td>{np.round(probs, 4)*100}</td>
                                     <td style="text-align: center">{int(occurrences)}</td>

                                 </tr>
                             </tbody>
                         </table>
                     </div>
                     <p class="mb-0" style="font-size: 11px;">
                            PRÉCISION DE LA PRÉVISION +-10%
                     </p>
                     <p class="mb-0" style="font-size: 9px;">
                            mis à jour le {str(update_on)}
                     </p>
                 </div>
             </div>          
        """
    return html_

def geo_json(lat, lon, value, occurrences, target, update_on, step):
    cmap = mpl.cm.YlOrRd
    return {
        "type": "Feature",
        "properties":{
            "weight":0.1,
            "fillColor": mpl.colors.to_hex(cmap(value)),
            "fillOpacity": 0.5,
            "popups": feature_tooltips(value, occurrences, target, update_on)
        },
        "geometry":{
            "type": "Polygon",
            "coordinates":[[
                [lon, lat],
                [lon, lat+step],
                [lon + step, lat + step],
                [lon + step, lat],
                [lon, lat]
            ]]
        }
    }

def cluster_grid_map(df:DataFrame, targets:List[str], targets_data:dict, sub_category_col:str, cluster_col:str, lat_col:str, lon_col:str, step:float, update_on:str, path:str)->None:
    data = df.copy(deep=True)
    data = data[data[lat_col] != 0.0]
    m = Map(location=[data[lat_col].median(), data[lon_col].median()], zoom_start=13)
    for target in targets:
        feature_group = FeatureGroup(target)
        t_df = data[data[sub_category_col].isin(targets_data.get(target))]
        clusters = df[cluster_col].unique()
        if t_df.shape[0] > 0:
            for cluster in clusters:
                x = t_df[t_df[cluster_col] == cluster][[lat_col, lon_col]]
                x[lat_col] = np.floor(x[lat_col] / step) * step
                x[lon_col] = np.floor(x[lon_col] / step) * step
                x = x.groupby(list(x)).size().rename('weight').reset_index()
                x['prob (%)'] = x['weight'] / x['weight'].max()
                for _, xi in x.iterrows():
                    c = GeoJson(
                        geo_json(xi[lat_col], xi[lon_col], np.round(xi['prob (%)'], 4), xi['weight'], target, update_on, step),
                        lambda p: p['properties'],
                        tooltip=folium.features.GeoJsonTooltip(
                            fields=['popups'],
                            labels=False,
                            style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") )
                        )
                    
                    Popup(f"<div><h3>{target}</h3></div>").add_to(c)
                    c.add_to(feature_group)
            feature_group.add_to(m)
    LayerControl().add_to(m)
    m.save(os.path.abspath(f"{path}/baseGridRiskMap.html"))
    return m


def baseGridRiskMap(df:DataFrame, category_col:str, sub_category_col:str, lat_col:str, lon_col:str, step:float, categories:List[str], update_on:str, path:str)->None:
    data = df.copy(deep=True)
    data = data[data[lat_col] != 0.0]
    m = Map(location=[data[lat_col].median(), data[lon_col].median()], zoom_start=11)
    for category in categories:
        t_df = data[data[category_col] == category]
        feature_group = FeatureGroup(category)
        subcategories = data[sub_category_col].unique()
        for subcategory in subcategories:
            x = t_df[t_df[sub_category_col] == subcategory][[lat_col, lon_col]]
            x[lat_col] = np.floor(x[lat_col] / step) * step
            x[lon_col] = np.floor(x[lon_col] / step) * step
            x = x.groupby(list(x)).size().rename('weight').reset_index()
            x['prob (%)'] = x['weight'] / x['weight'].max()
            for _, xi in x.iterrows():
                c = GeoJson(
                    geo_json(xi[lat_col], xi[lon_col], np.round(xi['prob (%)'], 4), xi['weight'], subcategory, update_on,step),
                    lambda p: p['properties'],
                    tooltip=folium.features.GeoJsonTooltip(
                        fields=['popups'],
                        labels=False,
                        style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") )
                    )
                
                Popup(f"<div><h3>{subcategory}</h3></div>").add_to(c)
                c.add_to(feature_group)
        feature_group.add_to(m)
    LayerControl().add_to(m)
    m.save(os.path.abspath(f"{path}/baseGridRiskMap.html"))
    return 

def set_cluster_feature(data, value, occurrence, target, update_on):
    d_json = json.loads(data.to_json())
    if value <= 0.30:
        cmap = mpl.cm.RdBu_r
        value = 0.1
    else:
        cmap = mpl.cm.YlOrRd
    for feature in d_json["features"]:
        feature['properties'] = {
            "weight":2,
            "color": mpl.colors.to_hex(cmap(value)),
            "fillColor": mpl.colors.to_hex(cmap(value)),
            "fillOpacity": 0.3,
            "popups": feature_tooltips(value, occurrence, target, update_on)
        }
    # print(d_json)
    geo = GeoJson(
        d_json, 
        lambda p: p['properties'],
            tooltip=folium.features.GeoJsonTooltip(
                fields=['popups'],
                labels=False,
                style=("background-color: white; color: #333333; font-family: arial; font-size: 12px; padding: 10px;") )
    )
    return geo

import random

def hotspots_map(m, geo_j, target, cluster_col, prob_col, occurence_col,  update_on):
    feature_group = FeatureGroup(target)
    for l in geo_j[cluster_col]:
        sub_data  = geo_j.loc[[l],:].copy(deep=True)
        probas     = geo_j.loc[[l], [prob_col]].values[0][0]
        occurence   = geo_j.loc[[l], [occurence_col]].values[0][0]
        sub_data = set_cluster_feature(sub_data, probas, occurence, target, update_on)
        sub_data.add_to(feature_group)
    feature_group.add_to(m)
    return m

def save_map(m, path, folder:str, filename:str) -> None:   
    LayerControl().add_to(m)
    m.save(path.joinpath(f"{folder}/{filename}"))
    return

def coordsInterpolate(gdf, step=0.002):
    x = gdf.copy()
    x['lat_interpolate'] = np.floor(x['LATITUDE'] / step) * step
    x['lon_interpolate'] = np.floor(x['LONGITUDE'] / step) * step
    x = x.groupby(['lat_interpolate', 'lon_interpolate'])['Value'].mean()
    x /= x.max()
    x = x.reset_index()
    print(x.shape)
    return x