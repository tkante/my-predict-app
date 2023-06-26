import pathlib
from dash import Dash
import dash_bootstrap_components as dbc

from pandas import DataFrame
from geopandas import GeoDataFrame, points_from_xy
import datetime

from source.data.loader import (
    load_crime_data,
    CrimeSchema
)

from source.data.consts import (
    Params
)
from source.components.layout import create_layout

from helper.utils import (
    loadJSON,
    load_classifier,
    set_target_variables
)

from helper.clustering import dbscan_hotspots

class InData:
    def __init__(self, 
                 data_path:str, 
                 models_path:str, 
                 city:str, targets_filename:str,
                 categorical_features_filename:str,
                 variables_filename:str,
                 crs_projection_filename:str,
                 dbscan_params_filename:str) -> None:
        self.data_path = data_path
        self.models_path = models_path
        self.city = city
        self.targets_filename = targets_filename
        self.categorical_features_filename = categorical_features_filename
        self.variables_filename = variables_filename
        self.crs_projection_filename = crs_projection_filename
        self.dbscan_params_filename = dbscan_params_filename

        self.data = None
        self.targets = None
        self.categorical_features = None
        self.variables = None
        self.crs_projection = None
        self.classifiers = None
        self.dbscan_params = None

        self.loader()

    def loader(self):
        self.data = load_crime_data(self.data_path, self.city)
        self.targets = loadJSON(self.data_path, self.city, f"{self.targets_filename}.json")
        self.categorical_features = loadJSON(self.data_path, self.city, f"{self.categorical_features_filename}.json")
        self.variables = loadJSON(self.data_path, self.city, f"{self.variables_filename}.json")
        self.crs_projection = loadJSON(self.data_path, self.city, f"{self.crs_projection_filename}.json")
        self.classifiers = load_classifier(self.models_path, f'{self.city}/crimes', list(self.targets.keys()))
        self.dbscan_params = loadJSON(self.models_path, f"{self.city}/crimes/clusters", "{}.json".format(self.dbscan_params_filename))

    def get_classifiers(self):
        return self.classifiers
    
    def get_dbscan_params(self):
        return self.dbscan_params

    def get_data(self):
        return self.data
    
    def get_targets(self):
        return self.targets
    
    def get_categorical_features(self):
        return list(self.categorical_features.values())[0]
    
    def get_variables(self):
        return self.variables
    
    def get_crs_projection(self):
        return self.crs_projection
    

def data_transformer(data:DataFrame, targets:dict, crs_proj:dict, sub_category_col:str, lat_col:str, lon_col:str) -> GeoDataFrame:
    gdf = data.copy(deep=True)
    gdf = set_target_variables(gdf, sub_category_col, targets)
    loc_proj= crs_proj.get("loc_proj")
    sph_proj = crs_proj.get("sph_proj")
    gdf  = GeoDataFrame(gdf, geometry=points_from_xy(gdf[lon_col], gdf[lat_col]), crs=sph_proj)
    gdf['coordinates'] = list(zip(gdf[lon_col], gdf[lat_col]))
    gdf = gdf.to_crs(loc_proj)
    return gdf

def main() -> None:
    # Path
    BASE_PATH    = pathlib.Path(__file__).parent.resolve()
    DATA_PATH   = BASE_PATH.joinpath("data").resolve()
    MODELS_PATH = BASE_PATH.joinpath("models").resolve()

    
    # Data et Params
    CITY = 'amiens'
    inData = InData(DATA_PATH, MODELS_PATH, CITY, Params.TARGETS, Params.CATEGORICAL_FEATURES, Params.VARIABLES, Params.CRS_PROJECTION, Params.DBSCAN_PARAMS)
    data = inData.get_data() 
    targets = inData.get_targets() 
    categorical_features = inData.get_categorical_features() 
    variables = inData.get_variables() 
    crs_projection = inData.get_crs_projection() 
    classifiers = inData.get_classifiers() 
    dbscan_params = inData.get_dbscan_params() 
    update_on     = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    gdf = data_transformer(data, targets, crs_projection, CrimeSchema.SUB_CATEGORY, CrimeSchema.LATITUDE, CrimeSchema.LONGITUDE)
       
    # APP CONTAINT
    app = Dash(
        __name__, 
        external_stylesheets = [dbc.themes.BOOTSTRAP, dbc.icons.FONT_AWESOME],
        meta_tags=[{'name': 'viewport',
                        'content': 'width=device-width, initial-scale=1.0'}]
    )
    server = app.server
    app.config.suppress_callback_exceptions = True
    app.title = "Anticipation des risques"
    app.layout = create_layout(
        app, 
        gdf, targets, categorical_features, variables, crs_projection, classifiers, dbscan_params,
        DATA_PATH, update_on
    )
    app.run_server(debug=False, port=8053)

if __name__ == '__main__':
   main()
