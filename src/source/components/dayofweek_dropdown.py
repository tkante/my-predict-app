from dash import dcc, html
from pandas import date_range
import datetime

from . import ids

def render() -> html.Div:
    today = datetime.date.today()
    all_dayofweek_from_today = date_range(today, today+datetime.timedelta(6), freq='D')
    all_dayofweek_from_today = [day.date() for day in all_dayofweek_from_today]

    return html.Div(
        children=[
            html.Label("Joure de la semaine", className='p-1'),
            dcc.Dropdown(
                id= ids.DAYOFWEEK_DROPDOWN,
                options= [{'label': day, 'value': day} for day in all_dayofweek_from_today],
                value= all_dayofweek_from_today[0],
                multi=True,
            )
        ]
    )
