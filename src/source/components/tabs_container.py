from dash import Dash, html
import dash_bootstrap_components as dbc

from . import ids

def render() -> html.Div:
    return html.Div(
        children = [
            dbc.Tabs(
                [
                    dbc.Tab(label="Predictions",  tab_id= ids.PREDICTIONS),
                    dbc.Tab(label="MODEL CAUSAL", tab_id= ids.GRAPH_CAUSAL),
                    dbc.Tab(label="SIMULATION",   tab_id= ids.SIMULATION),
                    dbc.Tab(label="Paramètres",   tab_id= ids.PARAMETRES),
                ],
            id=ids.TABS,
            active_tab=ids.PREDICTIONS,
            className="border"
            ),
            html.Div(id=ids.TAB_CONTENT)
        ]
    )
    
    
    
