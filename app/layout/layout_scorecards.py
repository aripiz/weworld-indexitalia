from index import data, metadata
from dash import dcc, html
import dash_bootstrap_components as dbc

from configuration import SEQUENCE_COLOR

# Options
territories_list = data['territory'].unique()

card = dbc.Container(
    children=[
        dbc.Row(
            children=[
                dbc.Col(
                    html.P(
                        "Select a territory (Country/Area/World) from the list and explore the scorecard to gain insights into its CFA World Index performance."
                    ),
                    lg=8, 
                    xs=12
                ),
                dbc.Col(
                    children=[
                        dbc.Label("Territory"),
                        dcc.Dropdown(
                            id='scorecard_territory',
                            options=territories_list,
                            value='World'
                        )
                    ],
                    lg=4, 
                    xs=12, 
                    align='end'
                ),
            ],
            className='mt-4', 
            justify='evenly'
        ),
        dbc.Row(
            children=[
                dbc.Col(
                    html.H2(id='scorecard_header'),
                    lg=12, 
                    xs=12
                )
            ],
            className='mt-4', 
            justify='evenly'
        ),
        dbc.Row(
            children=[
                dbc.Col(
                    dcc.Loading(
                        dcc.Graph(
                            id="scorecard_map", 
                            style={'height': 200, 'width': 200},
                            config={'displayModeBar': False, 'editable': False}
                        ),
                        color=SEQUENCE_COLOR[0]
                    ),
                    lg=2, 
                    xs=12, 
                    align='center'
                ),
                dbc.Col(
                    children=[
                        html.H4("Area"),
                        html.P(id="scorecard_area", style={'align': 'right'}),
                        html.H4("Population"),
                        html.P(id="scorecard_pop", style={'align': 'right'}),
                        html.H4("GDP per capita"),
                        html.P(id="scorecard_gdp", style={'align': 'right'})
                    ],
                    lg=4, 
                    xs=12, 
                    align='end'
                ),
                dbc.Col(
                    children=[
                        html.H4("CFA World Index Score"),
                        html.P(id="scorecard_score"),
                        html.H4("CFA World Index Rank"),
                        html.P(id="scorecard_rank", style={'align': 'right'}),
                        html.H4("Human Rights Implementation"),
                        html.P(id="scorecard_group")
                    ],
                    lg=5, 
                    xs=12, 
                    align='end'
                )
            ],
            className='mt-4', 
            justify='evenly'
        ),
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        html.H4("Progress"),
                        dcc.Loading(
                            dcc.Graph(
                                id='scorecard_progress',
                                config={
                                    'displaylogo': False, 
                                    'modeBarButtonsToRemove': [
                                        'pan2d', 'select2d', 'lasso2d', 
                                        'zoom2d', 'resetScale2d'
                                    ]
                                }
                            ),
                            color=SEQUENCE_COLOR[0]
                        )
                    ],
                    lg=6, 
                    xs=12
                ),
                dbc.Col(
                    children=[
                        html.H4("Profile"),
                        dcc.Loading(
                            dcc.Graph(
                                id='scorecard_radar',
                                config={
                                    'displaylogo': False, 
                                    'modeBarButtonsToRemove': [
                                        'pan2d', 'select2d', 'lasso2d', 
                                        'zoom2d', 'resetScale2d'
                                    ]
                                }
                            ),
                            color=SEQUENCE_COLOR[0]
                        )
                    ],
                    lg=6, 
                    xs=12
                )
            ],
            className='mt-2', 
            justify='evenly'
        ),
        dbc.Row(
            children=[
                dbc.Col(
                    children=[
                        html.H4("Components"),
                        dcc.Loading(
                            html.Div(
                                id='scorecard_table',
                                className='table-container'
                            ),
                            color=SEQUENCE_COLOR[0]
                        )
                    ]
                )
            ],
            className='mt-4', 
            justify='evenly'
        )
    ]
)
