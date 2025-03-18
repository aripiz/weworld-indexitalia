# layout_download.py

from index import data, metadata
from dash import dcc, html
import dash_bootstrap_components as dbc

# Options
features_list = data.columns[5:]
territories_list = data['territory'].unique()

# Modal window
modal_data_download = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Download dei dati dell'Indice"), close_button=False),
        dbc.ModalBody(
            html.Div([
                dbc.Label('Scarica tutti i dati disponibili o scegli dai menu i dati da scaricare.'),
                dbc.Row(
                    dbc.Col([
                        dbc.Label("Componenti:"),
                        dcc.Dropdown(
                            id='download_indicator',
                            options=features_list,
                            multi=True,
                            placeholder="Tutte le componenti",
                            style={"width": "100%"}
                        ),
                    ], xs=12), className='mt-2'),
                dbc.Row(
                    dbc.Col([
                        dbc.Label('Territori:'),
                        dcc.Dropdown(
                            id='download_territory',
                            options=territories_list,
                            multi=True,
                            placeholder="Tutti i territori",
                            style={"width": "100%"}
                        ),
                    ], xs=12), className='mt-2'),
                html.Br(),
                dbc.Button('Download', id='download_button', n_clicks=0, className="ml-auto"),
                dcc.Download(id='download_file')
            ],
            style={'text-align': 'center'})
        ),
        dbc.ModalFooter(
            dbc.Button(
                "Chiudi", id="close_download", n_clicks=0, className="ml-auto"
            )
        ),
    ],
    id="modal",
    centered=True,
    is_open=False,
    class_name='dbc',
    size='lg'
)
