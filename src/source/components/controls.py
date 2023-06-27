from dash import Dash, html, dcc 
import dash_bootstrap_components as dbc
from pandas import DataFrame

from typing import List

from . import (
    ids, 
    upload_data,
    district_dropdown,
    dayofweek_dropdown,
    window_dropdown,
    risk_level,
    category_dropdown
)

def render(app:Dash, data:DataFrame,  windows_tranlate:dict, categories:List[str]) -> dbc.Card:
    return  dbc.Card(
        [
            html.Div([upload_data.render(),]),
            html.Br(),
            html.Div([category_dropdown.render(categories)]),
            html.Div([district_dropdown.render(data)]),
            html.Div([dayofweek_dropdown.render()]),
            html.Div([window_dropdown.render(data,  windows_tranlate)]),
            html.Div([risk_level.render()]),
        ],
        body=True,
    )

# html.Br(),
# html.Div(
#     id="reset-btn-outer",
#     children=html.Button(id="reset-btn", children="Reset", n_clicks=0),
# ),