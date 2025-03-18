# layout_methodology.py

from index import data, metadata
from dash import dcc, html
import dash_bootstrap_components as dbc

from configuration import NOTES_FILE

# Options
subindexes_list = [data.columns[4]]
features_list = data.columns[4:23].tolist()
years_list = data['year'].unique()
components_list = [
    f"Indicator {num}: {metadata.loc[num]['name']}" for num in metadata.loc[1:30].index
]
indicators_list = [
    f"{num}: {metadata.loc[num]['name']}" for num in metadata.loc[1:30].index
]

intro_text = f"""
Il WeWorld Index Italia classifica le regioni italiane dal 2018 al 2023 combinando 30 indicatori diversi. L'Indice - insieme ai 3 Sottoindici _Contesto_, _Minori_ e _Donne_ - con l'obiettivo di misurare l'implementazione dei diritti umani di donne, bambini, bambine, adolescenti a livello regionale, d'area e italiano nel complesso.

Per una descrizione completa della costruzione, si veda il report [Medodologia e note tecniche]({NOTES_FILE}).
"""

structure_text = """
La necessità di valutare separatamente le performance delle regioni rispetto ai tre Sottoindici deriva da un presupposto fondamentale: per garantire il rispetto, la garanzia e l’implementazione dei diritti umani di donne e minori, è essenziale considerare le problematiche e i bisogni specifici legati al genere e all’età. Senza adottare un approccio intersezionale, non si può raggiungere la piena realizzazione dei diritti di donne, bambini, bambine e adolescenti.  

Una reale inclusione di queste categorie, infatti, può compiersi solo attraverso la creazione, implementazione e il monitoraggio di policy adeguate che devono essere al tempo stesso multidimensionali, per tenere conto dell’intreccio esistente tra i diritti di donne e minori, e targettizzate, ovvero tarate sulle loro necessità specifiche. Per questo è necessario guardare ancora più da vicino alle loro condizioni.

È necessario, quindi, procedere su due fronti paralleli e complementari: da una parte, è fondamentale lavorare sui contesti in cui vivono donne e minori e renderli il più favorevoli possibile al loro pieno sviluppo; dall’altra, non basta un ambiente favorevole: è fondamentale adottare politiche mirate e interventi concreti che garantiscano la piena implementazione dei loro diritti.  
"""

aggregation_text = """
Il punteggio del WeWorld Index per ogni territorio è costituito da un valore compreso tra **0 e 100**, ottenuto aggregando i dati normalizzati dei suoi **30 Indicatori** in **tre fasi differenti**.  

Innanzitutto sono calcolati i punteggi di ciascuna delle **Dimensioni** prendendo la media aritmetica dei punteggi delle due **Componenti** costituenti (indicatori normalizzati). Successivamente, per evitare una piena compensabilità fra le Dimensioni, il punteggio dei **Sottoindici** è determinato dalla media geometrica delle Dimensioni che ne fanno parte. La media geometrica è infine utilizzata anche per calcolare il **WeWorld Index Italia** a partire dai 3 Sottoindici.

Questo tipo di aggregazione è **non compensativo**: una scarsa performance in un aspetto giudicato cruciale per la realizzazione dei diritti umani non può essere completamente o parzialmente compensato da un punteggio elevato in altri.
"""

indicator_table = dbc.Table(
    children=[
        html.Tbody([
            html.Tr([html.Th("Numero", style={'font-weight': 'bold', 'text-transform': 'uppercase'}), html.Td(id="indicator_num")]),
            html.Tr([html.Th("Nome", style={'font-weight': 'bold', 'text-transform': 'uppercase'}), html.Td(id="indicator_name")]),
            html.Tr([html.Th("Sottoindice", style={'font-weight': 'bold', 'text-transform': 'uppercase'}), html.Td(id="indicator_sub")]),
            html.Tr([html.Th("Dimensione", style={'font-weight': 'bold', 'text-transform': 'uppercase'}), html.Td(id="indicator_dim")]),
            html.Tr([html.Th("Definizione", style={'font-weight': 'bold', 'text-transform': 'uppercase'}), html.Td(id="indicator_des")]),
            html.Tr([html.Th("Unità", style={'font-weight': 'bold', 'text-transform': 'uppercase'}), html.Td(id="indicator_unit")]),
            html.Tr([html.Th("Aggiornamento", style={'font-weight': 'bold', 'text-transform': 'uppercase'}), html.Td(id="indicator_update")]),
            html.Tr([html.Th("Fonte", style={'font-weight': 'bold', 'text-transform': 'uppercase'}), html.Td(html.A(id="indicator_source", target="_blank", rel="noopener noreferrer"))])
        ])
    ],
    bordered=True,
    hover=True,
    responsive=True,
    striped=True,
    size='sm'
)

# Methodology tabs
tab_indicators = html.Div(
    children=[
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        dbc.Label("Indicatore"),
                        dcc.Dropdown(
                            id='indicator',
                            options=indicators_list,
                            value=indicators_list[0],
                            style={"width": "100%"}
                        )
                    ]
                )
            ],
            className='mt-2'
        ),
        dbc.Row(
            children=[
                dbc.Col(indicator_table)
            ],
            className='mt-2'
        )
    ]
)

tab_construction = html.Div(
    children=[
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        dcc.Markdown(intro_text)
                    ]
                )
            ],
            className='mt-4', 
            justify='around'
        ),
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        dcc.Markdown("### Struttura dell'Indice"),
                        dcc.Markdown(structure_text)
                    ],
                    lg=6, 
                    xs=12
                ),
                dbc.Col(
                    children=[
                        dbc.CardGroup(
                            children=[
                                dbc.Card(
                                    children=[
                                        dbc.CardImg(
                                            src="assets/icona-contesto.png",
                                            top=True,
                                            style={
                                                "width": "100px",
                                                "height": "100px",
                                                "object-fit": "cover"
                                            }
                                        ),
                                        dbc.CardBody(
                                            children=[
                                                html.H4("Contesto", className="card-title"),
                                                html.Div(
                                                    children=[html.P(dim) for dim in metadata.loc[[1, 3, 5, 7, 9], 'dimension']],
                                                    className="card-text"
                                                )
                                            ]
                                        )
                                    ]
                                ),
                                dbc.Card(
                                    children=[
                                        dbc.CardImg(
                                            src="assets/icona-bambini.png",
                                            top=True,
                                            style={
                                                "width": "100px",
                                                "height": "100px",
                                                "object-fit": "cover"
                                            }
                                        ),
                                        dbc.CardBody(
                                            children=[
                                                html.H4("Minori", className="card-title"),
                                                html.Div(
                                                    children=[html.P(dim) for dim in metadata.loc[[11, 13, 15, 17, 19], 'dimension']],
                                                    className="card-text"
                                                )
                                            ]
                                        )
                                    ]
                                ),
                                dbc.Card(
                                    children=[
                                        dbc.CardImg(
                                            src="assets/icona-donne.png",
                                            top=True,
                                            style={
                                                "width": "100px",
                                                "height": "100px",
                                                "object-fit": "cover"
                                            }
                                        ),
                                        dbc.CardBody(
                                            children=[
                                                html.H4("Donne", className="card-title"),
                                                html.Div(
                                                    children=[html.P(dim) for dim in metadata.loc[[21, 23, 25, 27, 29], 'dimension']],
                                                    className="card-text"
                                                )
                                            ]
                                        )
                                    ]
                                )
                            ]
                        )
                    ],
                    align='center',
                    lg=6,
                    xs=12
                )
            ],
            className='mt-4',
            justify="around"
        ),
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        dcc.Markdown("### Processo di aggregazione"),
                        dcc.Markdown(aggregation_text)
                    ],
                    lg=6,
                    xs=12
                ),
                dbc.Col(
                    children=[
                        dbc.CardGroup(
                            children=[
                                dbc.Card(
                                    children=[
                                        dbc.CardBody(
                                            children=[
                                                html.H4("Dimensioni", className="card-title"),
                                                dcc.Markdown(
                                                    "La **media aritmetica** delle **2 Componenti** (indicatori) di ciascuna Dimensione ne dà il punteggio.",
                                                    className="card-text"
                                                )
                                            ]
                                        )
                                    ]
                                ),
                                dbc.Card(
                                    children=[
                                        dbc.CardBody(
                                            children=[
                                                html.H4("Sottoindici", className="card-title"),
                                                dcc.Markdown(
                                                    "La **media geometrica** delle **5 Dimensioni** di ciascun Sottoindice ne dà il punteggio.",
                                                    className="card-text"
                                                )
                                            ]
                                        )
                                    ]
                                ),
                                dbc.Card(
                                    children=[
                                        dbc.CardBody(
                                            children=[
                                                html.H4("Indidce", className="card-title"),
                                                dcc.Markdown(
                                                    "La **media geometrica** dei **3 Sottoindici** dà il punteggio dell'Indice.",
                                                    className="card-text"
                                                )
                                            ]
                                        )
                                    ]
                                )
                            ]
                        )
                    ],
                    align='center',
                    lg=6,
                    xs=12
                )
            ],
            className='mt-4',
            justify="around"
        )
    ]
)
