# layout_data.py

from index import data, metadata
from dash import dcc, html
import dash_bootstrap_components as dbc

from configuration import SEQUENCE_COLOR

# Options
subindexes_list = data.columns[5:9].to_list()
dimensions_list = data.columns[9:24].to_list()
years_list = data['year'].unique().tolist()
components_list = [f"Indicatore {num}: {metadata.loc[num]['name']}" for num in metadata.loc[1:30].index]
indicators_list = [f"{num}: {metadata.loc[num]['name']}" for num in metadata.loc[1:30].index]
kind_list = ['Dato', 'Punteggio']
territories_list = data['territory'].unique().tolist()
auxiliary_list = metadata.loc[101:103]['name'].to_list()
population_list = data.columns[84:87].to_list()

# Data tabs
tab_map_features = html.Div([
    dbc.Row(
        dbc.Col([
            dbc.Button(
                "Info",
                id="collapse-button",
                className="mb-3",
                color="primary",
                n_clicks=0,
            ),
            dbc.Collapse(
                dbc.Card("La mappa mostra i punteggi delle componenti dell’Indice. È possibile scegliere la componente (Indice/Sottoindice/Dimensione) e l’anno da visualizzare dai menu. Ogni area è colorata in base al livello di implementazione dei diritti umani per la componente selezionata. Gli intervalli di punteggio per ciascun livello sono dettagliati nella Metodologia.", body=True),
                id="collapse",
                is_open=True,
            ),
        ]), justify='around', class_name='my-2'
    ),
    dbc.Row([
        dbc.Col([
            dbc.Label("Componente"), 
            dcc.Dropdown(
                id='feature',
                options=subindexes_list + dimensions_list,
                value=subindexes_list[0],
                style={"width": "75%"}
            )], lg=8, xs=12),
        dbc.Col([
            dbc.Label("Anno"),
            dcc.Slider(
                years_list[0],
                years_list[-1],
                step=1,
                id='slider_year',
                value=years_list[-1],
                marks={str(year): str(year) for year in [years_list[0], years_list[-1]]},
                tooltip={"placement": "bottom", "always_visible": True}
            )
        ], lg=4, xs=12)],
        justify='around'),
    dbc.Row(dbc.Col(
        dcc.Loading(
            dcc.Graph(
                id="map",
                style={'min-height': '70vh'},
                config={'displaylogo': False, 'modeBarButtonsToRemove': ['pan2d', 'select2d', 'lasso2d', 'zoom2d']}
            ), color=SEQUENCE_COLOR[0]),
        lg=12, xs=12), justify='around', class_name='mt-2'),
])

tab_map_indicators = html.Div([
    dbc.Row(
        dbc.Col([
            dbc.Button(
                "Info",
                id="collapse-button",
                className="mb-3",
                color="primary",
                n_clicks=0,
            ),
            dbc.Collapse(
                dbc.Card("La mappa mostra i dati per gli Indicatori che fanno parte dell’Indice. È possibile utilizzare il menu per scegliere l’Indicatore da visualizzare, il tipo di valore (dati originali o punteggio normalizzato) e l’anno di riferimento. Se si selezionano i dati originali, le aree senza dati disponibili appariranno vuote sulla mappa.", body=True),
                id="collapse",
                is_open=True,
            ),
        ]), justify='around', class_name='my-2'
    ),
    dbc.Row([
        dbc.Col([
            dbc.Label("Indicatore"),
            dcc.Dropdown(
                id='indicator',
                options=components_list,
                value=components_list[0],
                style={"width": "100%"}
            )], lg=6, xs=12
        ),
        dbc.Col([
            dbc.Label("Tipo"),
            dbc.RadioItems(
                id='indicator_kind',
                options=kind_list,
                inline=True,
                value=kind_list[1]
            )], lg=2, xs=12
        ),
        dbc.Col([
            dbc.Label("Anno"),
            dcc.Slider(
                years_list[0],
                years_list[-1],
                step=1,
                id='slider_year',
                value=years_list[-1],
                marks={str(year): str(year) for year in [years_list[0], years_list[-1]]},
                tooltip={"placement": "bottom", "always_visible": True}
            )], lg=4, xs=12
        )], justify='around'),
    dbc.Row(dbc.Col(
        dcc.Loading(
            dcc.Graph(
                id="indicators_map",
                style={'min-height': '70vh'},
                config={'displaylogo': False, 'modeBarButtonsToRemove': ['pan2d', 'select2d', 'lasso2d', 'zoom2d']}
            ), color=SEQUENCE_COLOR[0]
        ),
        lg=12, xs=12), justify='around', class_name='mt-2'),
])

tab_correlations = html.Div([
    dbc.Row(
        dbc.Col([
            dbc.Button(
                "Info",
                id="collapse-button",
                className="mb-3",
                color="primary",
                n_clicks=0,
            ),
            dbc.Collapse(
                dbc.Card("Il grafico mostra la correlazione tra le componenti dell’Indice: ogni cerchio rappresenta un territorio, con le coordinate x e y basate sui punteggi nelle componenti selezionate. È possibile utilizzare i menu per scegliere quali delle due componenti (Indice/Sottoindice/Dimensione/Indicatore) confrontare. Il coefficiente di correlazione di Spearman \u03c1\u209b è visualizzato sopra il grafico. I territori sono colorati in base all'area geografica di appartenenza e dimensionati in base alla loro popolazione (Totale/Minori/Donne). Cliccando sugli elementi nella legenda, è possibile mostrarli o nasconderli.", body=True),
                id="collapse",
                is_open=True,
            ),
        ]), justify='around', class_name='my-2'
    ),
    dbc.Row([
        dbc.Col([
            dbc.Label("Dati (x)"),
            dcc.Dropdown(
                id="corr_x",
                options=subindexes_list + dimensions_list,
                value=subindexes_list[0],
                optionHeight=50
                #style={"width": "75%"}
            )], lg=3, xs=12),
        dbc.Col([
            dbc.Label("Dati (y)"),
            dcc.Dropdown(
                id="corr_y",
                options=subindexes_list + dimensions_list,
                value=subindexes_list[1],
                optionHeight=50
                #style={"width": "75%"}
            )], lg=3, xs=12),
        dbc.Col([
            dbc.Label("Popolazione"),
            dcc.Dropdown(
                id="corr_pop",
                options=population_list,
                value=population_list[0],
                optionHeight=50
                #style={"width": "75%"}
            )], lg=3, xs=12),
        dbc.Col([
            dbc.Label("Anno"),
            dcc.Slider(
                years_list[0],
                years_list[-1],
                step=1,
                id='slider_year',
                value=years_list[-1],
                marks={str(year): str(year) for year in [years_list[0], years_list[-1]]},
                tooltip={"placement": "bottom", "always_visible": True}
            )
        ], lg=3, xs=12)],
        justify='between'),
    dbc.Row(dbc.Col(
        dcc.Loading(
            dcc.Graph(
                id="features_correlation",
                style={'min-height': '70vh'},
                config={'displaylogo': False, 'modeBarButtonsToRemove': ['pan2d', 'select2d', 'lasso2d', 'zoom2d']}
            ), color=SEQUENCE_COLOR[0]
        ),
        lg=12, xs=12), justify='around', class_name='mt-2'),
])

tab_ranking = html.Div([
    dbc.Row(
        dbc.Col([
            dbc.Button(
                "Info",
                id="collapse-button",
                className="mb-3",
                color="primary",
                n_clicks=0,
            ),
            dbc.Collapse(
                dbc.Card("La tabella mostra la classifica dei territori per la componente (Indice/Sottoindice/Dimensione) e l’anno selezionati. È riportata la variazione del punteggio dal 2018.", body=True),
                id="collapse",
                is_open=True,
            ),
        ]), justify='around', class_name='my-2'
    ),
    dbc.Row([
        dbc.Col([
            dbc.Label("Componente"),
            dcc.Dropdown(
                id="ranking_feature",
                options=subindexes_list + dimensions_list,
                value=subindexes_list[0],
                style={"width": "75%"}
            )], lg=8, xs=12),
        dbc.Col([
            dbc.Label("Anno"),
            dcc.Slider(
                years_list[0],
                years_list[-1],
                step=1,
                id='slider_year',
                value=years_list[-1],
                marks={str(year): str(year) for year in [years_list[0], years_list[-1]]},
                tooltip={"placement": "bottom", "always_visible": True}
            )
        ], lg=4, xs=12)
    ], justify='around'),
    dbc.Row(
        dcc.Loading(
            dbc.Col(
                id='ranking_table',
                className='table-container',
                lg=12, xs=12
                #style={"height": "60vh", "overflow": "scroll"},
            ), color=SEQUENCE_COLOR[0]), justify='around', class_name='mt-2')
])

tab_evolution = html.Div([
    dbc.Row(
        dbc.Col([
            dbc.Button(
                "Info",
                id="collapse-button",
                className="mb-3",
                color="primary",
                n_clicks=0,
            ),
            dbc.Collapse(
                dbc.Card("Il grafico mostra la serie temporale delle componenti dell’Indice. Dai menu, puoi selezionare una o più componenti (Indice/Sottoindice/Dimensione/Indicatore) e uno o più territori (Regione/Area/Italia) per confrontare la loro performance dal 2018.", body=True),
                id="collapse",
                is_open=True,
            ),
        ]), justify='around', class_name='my-2'
    ),
    dbc.Row([
        dbc.Col([
            dbc.Label("Componente"),
            dcc.Dropdown(
                id="evolution_feature",
                options=subindexes_list +  dimensions_list + components_list,
                value=subindexes_list[0],
                optionHeight=50,
                #style={"width": "75%"},
                multi=True
            )], lg=6, xs=12),
        dbc.Col([
            dbc.Label("Territorio"),
            dcc.Dropdown(
                id='evolution_territory',
                options=territories_list,
                value='Italia',
                #style={"width": "75%"},
                multi=True
            )], lg=6, xs=12)
    ], justify='around'),
    dbc.Row(dbc.Col(
        dcc.Loading(
            dcc.Graph(
                id="evolution_plot",
                style={'min-height': '70vh'},
                config={'displaylogo': False, 'modeBarButtonsToRemove': ['pan2d', 'select2d', 'lasso2d', 'zoom2d']}
            ), color=SEQUENCE_COLOR[0]
        ),
        lg=12, xs=12), justify='around', class_name='mt-2'),
])

tab_radar = html.Div([
    dbc.Row(
        dbc.Col([
            dbc.Button(
                "Info",
                id="collapse-button",
                className="mb-3",
                color="primary",
                n_clicks=0,
            ),
            dbc.Collapse(
                dbc.Card("Il grafico radar mostra i punteggi delle Dimensioni per il territorio scelto. Puoi utilizzare i menu per selezionare i territori (Regioni/Area/Italia) e gli anni da visualizzare.", body=True),
                id="collapse",
                is_open=True,
            ),
        ]), justify='around', class_name='my-2'
    ),
    dbc.Row([
        dbc.Col([
            dbc.Label("Territorio"),
            dcc.Dropdown(
                id='radar_territory',
                options=territories_list,
                value='Italia',
                style={"width": "75%"},
                multi=True
            )], lg=9, xs=12),
        dbc.Col([
            dbc.Label("Anno"),
            dcc.Dropdown(
                id='radar_year',
                options=years_list,
                value=[years_list[0], years_list[-1]],
                #style={"width": "75%"},
                multi=True
            )], lg=3, xs=12)
    ], justify='around'),
    dbc.Row([
        # dbc.Col(html.Div(
        #     id='radar_table',
        #     className='table-container',
        #     #style={"height": "60vh", "overflow": "scroll"},
        # ), lg=6, xs=12),
        dbc.Col(dcc.Loading(dcc.Graph(
            id="radar_chart",
            style={'min-height': '70vh'},
            config={'displaylogo': False, 'modeBarButtonsToRemove': ['pan2d', 'select2d', 'lasso2d', 'zoom2d']}
        ), color=SEQUENCE_COLOR[0]), lg=12, xs=12)
    ], justify='around', class_name='mt-2'),
])

tab_comparison = html.Div([
    dbc.Row(
        dbc.Col([
            dbc.Button(
                "Info",
                id="collapse-button",
                className="mb-3",
                color="primary",
                n_clicks=0,
            ),
            dbc.Collapse(
                dbc.Card("Il grafico confronta il WeWorld Index Italia con altri indici rilevanti. Ogni cerchio rappresenta un territorio, con le coordinate x e y basate sui punteggi degli indici selezionati. È possibile utilizzare i menu per scegliere quali dati confrontare. Il coefficiente di correlazione di Spearman \u03c1\u209b è visualizzato sopra il grafico. I territori sono colorati in base all'area geografica di appartenenza e dimensionati in base alla loro popolazione (Totale/Minori/Donne). Cliccando sugli elementi nella legenda, è possibile mostrarli/nasconderli. Il PIL pro capite è rappresentato su una scala logaritmica per meglio confrontarlo le altre tipologie di dato.", body=True),
                id="collapse",
                is_open=True,
            ),
        ]), justify='around', class_name='my-2'
    ),
    dbc.Row([
        dbc.Col([
            dbc.Label("Dati (x)"),
            dcc.Dropdown(
                id="comp_x",
                options=[subindexes_list[0]] + auxiliary_list,
                value=subindexes_list[0],
                #optionHeight=50,
                #style={"width": "75%"}
            )], lg=3, xs=12),
        dbc.Col([
            dbc.Label("Dati (y)"),
            dcc.Dropdown(
                id="comp_y",
                options=[subindexes_list[0]] + auxiliary_list,
                value=auxiliary_list[0],
                #optionHeight=50
                #style={"width": "75%"}
            )], lg=3, xs=12),
        dbc.Col([
            dbc.Label("Popolazione"),
            dcc.Dropdown(
                id="comp_pop",
                options=population_list,
                value=population_list[0],
                optionHeight=50
                #style={"width": "75%"}
            )], lg=3, xs=12),
        dbc.Col([
            dbc.Label("Anno"),
            dcc.Slider(
                years_list[0],
                years_list[-1],
                step=1,
                id='slider_year',
                value=years_list[-1],
                marks={str(year): str(year) for year in [years_list[0], years_list[-1]]},
                tooltip={"placement": "bottom", "always_visible": True}
            )
        ], lg=3, xs=12)],
        justify='between'),
    dbc.Row(dbc.Col(dcc.Loading(dcc.Graph(
        id="comparison_chart",
        style={'min-height': '70vh'},
        config={'displaylogo': False, 'modeBarButtonsToRemove': ['pan2d', 'select2d', 'lasso2d', 'zoom2d']}
    ), color=SEQUENCE_COLOR[0]), lg=12, xs=12), justify='around', class_name='mt-2'),
])
