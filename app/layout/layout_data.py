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
                dbc.Card("The map displays the scores of the Index components. You can choose the component (Index/Sub-index/Dimension) and the year to view from the menus. Each area is shaded according to its level of Human Rights Implementation for the selected component. The score ranges for each level are detailed in the Technical Notes.", body=True),
                id="collapse",
                is_open=True,
            ),
        ]), justify='around', class_name='my-2'
    ),
    dbc.Row([
        dbc.Col([
            dbc.Label("Component"), 
            dcc.Dropdown(
                id='feature',
                options=subindexes_list + dimensions_list,
                value=subindexes_list[0],
                style={"width": "75%"}
            )], lg=8, xs=12),
        dbc.Col([
            dbc.Label("Year"),
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
                dbc.Card("The map displays data for the Indicators that are part of the Index. You can use the menus to choose the Indicator, the type of value (original data or normalized score), and the reference year. If you select original data, the map will show blank areas for any missing values.", body=True),
                id="collapse",
                is_open=True,
            ),
        ]), justify='around', class_name='my-2'
    ),
    dbc.Row([
        dbc.Col([
            dbc.Label("Indicator"),
            dcc.Dropdown(
                id='indicator',
                options=components_list,
                value=components_list[0],
                style={"width": "100%"}
            )], lg=6, xs=12
        ),
        dbc.Col([
            dbc.Label("Kind"),
            dbc.RadioItems(
                id='indicator_kind',
                options=kind_list,
                inline=True,
                value=kind_list[1]
            )], lg=2, xs=12
        ),
        dbc.Col([
            dbc.Label("Year"),
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
                dbc.Card("The chart shows the correlation between Index components: each point represents a territory, with x and y coordinates based on its scores in the selected components. You can use the menus to choose which two components (Index/Sub-index/Dimension/Indicator) to compare. Spearmans's correlation coefficient \u03c1\u209b is displayed above the plot. Territories are colored according to their geographic area and sized based on their population (Total/Female/Children). Clicking on the items in the legend you can show/hide them.", body=True),
                id="collapse",
                is_open=True,
            ),
        ]), justify='around', class_name='my-2'
    ),
    dbc.Row([
        dbc.Col([
            dbc.Label("Data (x)"),
            dcc.Dropdown(
                id="corr_x",
                options=subindexes_list + dimensions_list,
                value=subindexes_list[0],
                optionHeight=50
                #style={"width": "75%"}
            )], lg=3, xs=12),
        dbc.Col([
            dbc.Label("Data (y)"),
            dcc.Dropdown(
                id="corr_y",
                options=subindexes_list + dimensions_list,
                value=subindexes_list[1],
                optionHeight=50
                #style={"width": "75%"}
            )], lg=3, xs=12),
        dbc.Col([
            dbc.Label("Population"),
            dcc.Dropdown(
                id="corr_pop",
                options=population_list,
                value=population_list[0],
                optionHeight=50
                #style={"width": "75%"}
            )], lg=3, xs=12),
        dbc.Col([
            dbc.Label("Year"),
            dcc.Slider(
                years_list[0],
                years_list[-1],
                step=1,
                id='slider_year',
                value=years_list[-2],
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
                dbc.Card("The table shows the ranking of territories for the selected component (Index/Sub-index/Dimension) and year. The table updates change in score and rank from 2015. When comparing rank values keep in mind that the number of territories varies in each year (between 157 and 166).", body=True),
                id="collapse",
                is_open=True,
            ),
        ]), justify='around', class_name='my-2'
    ),
    dbc.Row([
        dbc.Col([
            dbc.Label("Component"),
            dcc.Dropdown(
                id="ranking_feature",
                options=subindexes_list + dimensions_list,
                value=subindexes_list[0],
                style={"width": "75%"}
            )], lg=8, xs=12),
        dbc.Col([
            dbc.Label("Year"),
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
                dbc.Card("The chart displays the temporal evolution of the Index components. From the menus, you can select one or more components (Index/Sub-index/Dimension/Indicator) and one or more territories (Country/Area/World) to compare their evolution.", body=True),
                id="collapse",
                is_open=True,
            ),
        ]), justify='around', class_name='my-2'
    ),
    dbc.Row([
        dbc.Col([
            dbc.Label("Component"),
            dcc.Dropdown(
                id="evolution_feature",
                options=subindexes_list +  dimensions_list + components_list,
                value=subindexes_list[0],
                optionHeight=50,
                #style={"width": "75%"},
                multi=True
            )], lg=6, xs=12),
        dbc.Col([
            dbc.Label("Territory"),
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
                dbc.Card("The radar chart shows the scores of the Dimensions for the territory. You can use the menus to select the territories (Country/Area/World) and the years to display. The table beside the chart shows the data presented in the chart.", body=True),
                id="collapse",
                is_open=True,
            ),
        ]), justify='around', class_name='my-2'
    ),
    dbc.Row([
        dbc.Col([
            dbc.Label("Territory"),
            dcc.Dropdown(
                id='radar_territory',
                options=territories_list,
                value='Italia',
                style={"width": "75%"},
                multi=True
            )], lg=9, xs=12),
        dbc.Col([
            dbc.Label("Year"),
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
                dbc.Card("The chart compares the Index and other relevant indicators: GDP per capita and Human Development Index. Each point represents a territory, with x and y coordinates based on its value in the selected datasets. You can use the menus to choose which datasets to compare. Territories are colored according to their geographic area and sized based on their population (Total/Female/Children). Clicking on the items in the legend you can show/hide them. GDP per capita uses a logarithmic scale.", body=True),
                id="collapse",
                is_open=True,
            ),
        ]), justify='around', class_name='my-2'
    ),
    dbc.Row([
        dbc.Col([
            dbc.Label("Data (x)"),
            dcc.Dropdown(
                id="comp_x",
                options=[subindexes_list[0]] + auxiliary_list,
                value=subindexes_list[0],
                #optionHeight=50,
                #style={"width": "75%"}
            )], lg=3, xs=12),
        dbc.Col([
            dbc.Label("Data (y)"),
            dcc.Dropdown(
                id="comp_y",
                options=[subindexes_list[0]] + auxiliary_list,
                value=auxiliary_list[0],
                #optionHeight=50
                #style={"width": "75%"}
            )], lg=3, xs=12),
        dbc.Col([
            dbc.Label("Population"),
            dcc.Dropdown(
                id="comp_pop",
                options=population_list,
                value=population_list[0],
                optionHeight=50
                #style={"width": "75%"}
            )], lg=3, xs=12),
        dbc.Col([
            dbc.Label("Year"),
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
