from dash import Dash, html, Input, Output
import dash_bootstrap_components as dbc

from pandas import DataFrame


from . import (
    ids, 
    controls, 
    maps
)

def render (app:Dash, data:DataFrame) -> html.Div:
    @app.callback(
        Output(ids.TAB_CONTENT, "children"), 
        [
            Input(ids.TABS, "active_tab")
        ],
    )
    def render_tab_content(active_tab):
        if active_tab :
            if active_tab == ids.PREDICTIONS:
                return html.Div(
                    children=[
                        dbc.Row(
                            [
                                dbc.Col(controls.render(app, data), xs=12, sm=12, md=4, lg=4, xl=4),
                                dbc.Col(maps.render(app, data), xs=12, sm=12, md=8, lg=8, xl=8),  
                            ],
                            align="center",
                        ),
                    ]
                )
            elif active_tab == ids.GRAPH_CAUSAL:
                return html.Div(
                    children=[
                        html.P("Inside relation cause à effet entre événement!")
                    ]
                ),
            elif active_tab == ids.PARAMETRES:
                return html.Div(
                    children=[
                        html.P("Inside Paramétrage de l'application predict!")
                    ]
                )
            elif active_tab == ids.SIMULATION:
                return html.Div(
                    children=[
                        html.P("Optimisation et génération des plannings des tournées sur les 12 prochaines mois!")
                    ]
                )
        return html.Div(
                    children=[
                        html.P("Veuillez sélectionner une option!")
                    ]
                )

