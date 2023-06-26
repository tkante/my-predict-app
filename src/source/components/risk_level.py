from dash import html, dcc 
import matplotlib as mpl 

from . import ids

def render() -> html.Div:
    cmap = mpl.cm.RdBu_r
    levels = ['Fort', 'Moyen', 'Faible']
    return html.Div(
        children=[
            html.Label("Niveau de risque", className='p-1'),
            dcc.Dropdown(
                id=ids.RISK_LEVEL_DROPDOWN,
                options= [{'label': level, 'value':level} for level in levels],
                value= levels,
                multi=True
            )
        ]
    )


    # return html.Div(
    #     children=[
    #         html.Label("Niveau de risque"),
    #         dcc.Checklist(
    #             id= ids.RISK_LEVEL_DROPDOWN,
    #             options=[
    #                 {
    #                     "label": html.Div(['Fort'], className="mr-2", style={'color': mpl.colors.to_hex(cmap(0.95)), 'font-size': 15}),
    #                     "value": "Fort",
    #                 },
    #                 {
    #                     "label": html.Div(['Moyen'], className="mr-2", style={'color': mpl.colors.to_hex(cmap(0.65)), 'font-size': 15}),
    #                     "value": "Moyen",
    #                 },
    #                 {
    #                     "label": html.Div(['Faible'], className="mr-2", style={'color': mpl.colors.to_hex(cmap(0.1)), 'font-size': 15}),
    #                     "value": "Faible",
    #                 },
    #             ],
    #             value= support,
    #             # labelStyle={"display": "flex", "align-items": "center"},
    #             inline= True
    #         )
    #     ]
    # )