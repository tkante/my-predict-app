from dash import Dash, html, dcc 
from typing import List
from . import ids

def render(categories:List[str]) -> html.Div:
    return html.Div(
        children=[
            html.Label("Evénement", className='p-1'),
            dcc.Dropdown(
                id= ids.CATEGORY_DROPDOWN,
                options=[{'label': category, 'value': category} for category in categories],
                value= categories[0],
                multi=True
            )
        ]
    )