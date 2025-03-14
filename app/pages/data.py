# data.py

from dash import html, register_page
import dash_bootstrap_components as dbc
from configuration import TITLE

register_page(__name__, name=TITLE)

# Tabs
tabs = dbc.Tabs(
    children=[
        dbc.Tab(label="Mappa componenti", tab_id="map_features"),
        dbc.Tab(label="Mappa indicatori", tab_id="map_indicators"),
        dbc.Tab(label="Classifica", tab_id="ranking"),
        dbc.Tab(label="Serie storiche", tab_id="evolution"),
        dbc.Tab(label="Profili", tab_id="radar"),
        dbc.Tab(label="Correlazioni", tab_id="correlations"),
        dbc.Tab(label="Confronti", tab_id="comparison")
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
