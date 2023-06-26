from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc

import plotly.express as px
from pandas import DataFrame

from . import (
    ids,
    controls,
    maps
)


def render(app:Dash, data:DataFrame) -> html.Div:
    return html.Div(
        children=[
            # html.H4(
            #     children=[
            #         html.I(className="fa-solid fa-handcuffs p-2"),
            #         "Anticipations des événements à risque",
            #     ], 
            #     className="text-primary"
            # ),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(controls.render(app, data), xs=12, sm=12, md=4, lg=4, xl=4),
                    dbc.Col(maps.render(app, data), xs=12, sm=12, md=8, lg=8, xl=8),  
                ],
                align="center",
            ),
        ]
    )
    
