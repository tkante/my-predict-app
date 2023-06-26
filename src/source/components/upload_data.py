from dash import html, dcc
from . import ids

def render() -> html.Div:
    return html.Div(
        [
            html.P(
               "Téléchargement Fichier:",
                className="control_label",
            ),
            dcc.Upload(
                id=ids.UPLOAD_DATA,
                children=html.Div([
                    'Téléccharger votre fichier ou - ',
                    html.A('ou glisser un fichier ici')
                ]),
                style={
                    'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'align': 'center',
                    'margin': '10px'
                },
                # Allow multiple files to be uploaded
                multiple=True
            ),
            html.Div(id='output-data-upload'),  
        ]
    )