# layout_download.py

from index import data, metadata
from dash import dcc, html
import dash_bootstrap_components as dbc

# Options
features_list = data.columns[4:]
territories_list = data['territory'].unique()

# Modal window
modal_data_download = dbc.Modal(
    [
        dbc.ModalHeader(dbc.ModalTitle("Data download"), close_button=False),
        dbc.ModalBody(
            html.Div([
                dbc.Label('Download all available data or select a subset from the menus'),
                dbc.Row(
                    dbc.Col([
                        dbc.Label("Select features"),
                        dcc.Dropdown(
                            id='download_indicator',
                            options=features_list,
                            multi=True,
                            # placeholder="All features",
                            style={"width": "100%"}
                        ),
                    ], xs=12), className='mt-2'),
                dbc.Row(
                    dbc.Col([
                        dbc.Label('Select territories'),
                        dcc.Dropdown(
                            id='download_territory',
                            options=territories_list,
                            multi=True,
                            # placeholder="All territories",
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
                "Close", id="close_download", n_clicks=0, className="ml-auto"
            )
        ),
    ],
    id="modal",
    centered=True,
    is_open=False,
    class_name='dbc',
    size='lg'
)
