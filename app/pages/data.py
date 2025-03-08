# data.py

from dash import html, register_page
import dash_bootstrap_components as dbc
from configuration import TITLE

register_page(__name__, name=TITLE)

# Tabs
tabs = dbc.Tabs(
    children=[
        dbc.Tab(label="Components Map", tab_id="map_features"),
        dbc.Tab(label="Indicators Map", tab_id="map_indicators"),
        dbc.Tab(label="Components Ranking", tab_id="ranking"),
        dbc.Tab(label="Components Evolution", tab_id="evolution"),
        dbc.Tab(label="Dimensions Profile", tab_id="radar"),
        dbc.Tab(label="Components Correlations", tab_id="correlations"),
        dbc.Tab(label="Index Comparison", tab_id="comparison")
    ],
    id="data_tabs",
    active_tab="map_features",
    class_name='d-flex justify-content-around'
)

layout = dbc.Container(
    children=[
        dbc.Row(dbc.Col(tabs)),
        dbc.Row(dbc.Col(id="data_tab_content"), className='mt-2')
    ],
    class_name='mt-4'
)
