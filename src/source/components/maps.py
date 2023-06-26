from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc

import json
import datetime
import random
from geopandas import GeoDataFrame
from typing import List
from pandas import DataFrame, to_datetime
from folium import Map

from ..data.loader import CrimeSchema

from . import ids
from helper.mapping import (
    save_map,
    hotspots_map
)

from helper.clustering import dbscan_hotspots
from helper.utils import (
    feeaturesX,
    predict_proba
)

MAP_FILENAME = 'hotspot.html'
FOLDER = 'maps'

def display_selected_categories(categories) -> html.Ul:
    if isinstance(categories, list):
        return html.Ul([html.Li(t) for t in categories])
    else:
        return html.Ul([html.Li(categories)])

def display_selected_items(days, catgeories) -> html.Ul:
    if isinstance(days, list):
        return html.Ul(
            children=[
                html.Li(children=[
                    html.P(html.Mark(day)),
                    display_selected_categories(catgeories)
                ]) 
                for day in days
            ]
            )
    else:
        return html.Ul([
            html.P(html.Mark(days)),
            display_selected_categories(catgeories)
        ])



def build_cluster_for_target(gdf:GeoDataFrame, target, dbscan_params:dict, cluster_col, district_col, district) -> dict:
    geo_j, df_target = GeoDataFrame(), GeoDataFrame()
    if target is not None:
        gdf = gdf[gdf[target] == 1].copy()
        params = dbscan_params.get(target)
        distance, min_samp = params.get('distance'), params.get('min_samples')
        geo_j, df_target = dbscan_hotspots(gdf, distance, min_samp, [target], cluster_col, district_col, district)
    return geo_j, df_target

def create_map(gdf:GeoDataFrame, path:str, folder:str, filename:str,
               categories,  districts, dayofweeks, windows, support,
               targets, categorical_features, variables, crs_projection, classifiers, dbscan_params, update_on) -> None:
    m = Map(location=[gdf[CrimeSchema.LATITUDE].median(), gdf[CrimeSchema.LONGITUDE].median()], zoom_control=14) 

    if isinstance(categories, str):
        categories = [categories]
    if isinstance(districts, str):
        districts = [districts]
    if isinstance(support, str):
        support = [support]
    if isinstance(dayofweeks, str):
        dayofweeks = [dayofweeks]
    if isinstance(windows, str):
        windows = [windows]
    
    dayofweeks = [to_datetime(day).day_name() for day in dayofweeks]
    month = to_datetime(update_on).month_name()

    for category in categories:
        model = classifiers.get(category)
        geo_j, _ = build_cluster_for_target(gdf, category, dbscan_params, 
                                                    CrimeSchema.CLUSTER, CrimeSchema.DISTRICT, districts) 
        X = feeaturesX(gdf, CrimeSchema.DATE, CrimeSchema.MONTH_NAME, CrimeSchema.DAYOFWEEK, CrimeSchema.WINDOW,  month, dayofweeks,  windows, CrimeSchema.HOLIDAY_NAME, category, categorical_features, variables)
        proba = predict_proba(X, model)
        geo_j[CrimeSchema.PROBABILITY] = geo_j[category]*proba
        geo_j[CrimeSchema.PROBABILITY] = geo_j[category]/geo_j[category].max()
        geo_j[CrimeSchema.OCCURENCES] =  [random.randrange(4) for _ in range(geo_j.shape[0])]
        m = hotspots_map(m, geo_j, category, CrimeSchema.CLUSTER, CrimeSchema.PROBABILITY, CrimeSchema.OCCURENCES, update_on)
    save_map(m, path, folder, filename)


def render_map(path:str, folder:str, filename) -> html.Div:
    return html.Div(
        [
            html.Iframe(id='map', srcDoc=open(path.joinpath(f"{folder}/{filename}"), 'r').read(), width='100%', height='600'),
        ]
    )


def render(
        app:Dash, 
        gdf:GeoDataFrame, targets:List[str], categorical_features:dict, variables:list, crs_projection:dict, classifiers:dict, dbscan_params:dict,
        path:str, update_on) -> html.Div:
    @app.callback(
        Output(ids.HOTSPOTS_MAP, 'children'),
            [
                Input(ids.CATEGORY_DROPDOWN, 'value'),
                Input(ids.DISTRICT_DROPDOWN, 'value'),
                Input(ids.DAYOFWEEK_DROPDOWN, 'value'),
                Input(ids.WINDOW_DROPDOWN, 'value'),
                Input(ids.RISK_LEVEL_DROPDOWN, 'value'),
            ]
        )
    def map_hp(categories, districts, dayofweeks, windows, support):
        
        create_map(
            gdf, path, FOLDER, MAP_FILENAME,
            categories,  districts, dayofweeks, windows, support,
            targets, categorical_features, variables, crs_projection, classifiers, dbscan_params, update_on
        )
        

        return html.Div(
            children=[
                render_map(path, FOLDER, MAP_FILENAME),
                html.Div("Predictions pour les jours(s) ", className='d-inline'), 
                display_selected_items(dayofweeks, categories), 
            ], 
            id= ids.HOTSPOTS_MAP
        )
    
    return html.Div("Pas de predictions!", id=ids.HOTSPOTS_MAP)


