from dash import Dash, html, dcc
from pandas import DataFrame
from datetime import datetime

from source.data.loader import CrimeSchema
from . import ids

def time_slot(hour:int):
    """TIME SLOT"""
    if 6 <= hour < 13:
        return "morning"
    elif 13 <= hour < 19:
        return "afternoon"
    elif 19 <= hour < 0:
        return "evening"
    else:
        return "night"

def select_current_window(windows):
    hour = datetime.now().hour
    window = time_slot(hour)
    if window in windows:
        return window
    return windows

def render(data:DataFrame,  windows_tranlate:dict) -> html.Div :
    df = data.copy(deep=True)
    df.dropna(subset=[CrimeSchema.WINDOW], inplace=True)
    windows = df[CrimeSchema.WINDOW].unique().tolist()
    return html.Div(
        children=[
            html.Label("Plage horaire", className='p-1'),
            dcc.Dropdown(
                id= ids.WINDOW_DROPDOWN,
                options= [{'label': windows_tranlate.get(window), 'value': windows_tranlate.get(window)} for window in windows],
                value= windows_tranlate.get(select_current_window(windows)),
                multi= True,
            )
        ]
    )