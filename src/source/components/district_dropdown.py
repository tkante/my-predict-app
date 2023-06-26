from dash import Dash, html, dcc, Input, Output
from pandas import DataFrame
from typing import List

from ..data.loader import CrimeSchema
from . import ids

def render(data:DataFrame) ->html.Div:
    df = data.copy(deep=True)
    df.dropna(subset=[CrimeSchema.DISTRICT], inplace=True)
    all_districts: List[str] = df[CrimeSchema.DISTRICT].unique().tolist()
    return html.Div(
        children=[
            html.Label("Quartier", className='p-1'),
            dcc.Dropdown(
                id= ids.DISTRICT_DROPDOWN,
                options= [{"label": str(district), "value": str(district)} for district in all_districts],
                multi=True,
                placeholder="Selectionner quartier"
            )
        ]
    )