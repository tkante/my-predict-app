from dash import html, Dash
from pandas import DataFrame
import dash_bootstrap_components as dbc

from geopandas import GeoDataFrame
from typing import List

from source.components import(
    controls,
    maps
)

def create_layout(
        app:Dash, 
        gdf:GeoDataFrame, windows_tranlate:dict, targets:List[str], categorical_features:dict, variables:list, crs_projection:dict, classifiers:dict, dbscan_params:dict,
        path:str, update_on) -> html.Div:
    categories = list(targets.keys())
    return html.Div(
        # className="app-div",
        children=[
            # App header
            html.Div(
                children=[
                    html.I(className="fa-solid fa-bars"),
                    html.Span("CITY ZEN", className="m-2"),
                    html.I(className="fa-solid fa-right-from-bracket float-end m-2"),
                    html.I(className="fa-solid fa-user float-end mx-4 my-2"),
                   
                ], 
                style={"backgroundColor":"#003366", "color":"white", "height": "50px"},  
                className="opacity-100 p-2 m-0"
            ),
            html.H2("Anticipation des risques"),
            html.Hr(),
            # App Container
            # html.Br(),
            dbc.Row(
                [
                    dbc.Col(
                        children=[controls.render(app, gdf,  windows_tranlate, categories)],
                        xs=12, sm=12, md=4, lg=4, xl=4
                    ),
                    dbc.Col(children=[maps.render(app, gdf, windows_tranlate, targets, categorical_features, variables, crs_projection, classifiers, dbscan_params, path, update_on)],
                        xs=12, sm=12, md=8, lg=8, xl=8
                    )
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        children=[],
                        xs=12, sm=12, md=8, lg=8, xl=8
                    ),
                    dbc.Col(
                        children=[],
                        xs=12, sm=12, md=8, lg=8, xl=8
                    )
                ]
            )
        ]
    )