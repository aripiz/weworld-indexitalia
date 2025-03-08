# scorecards.py

from dash import html, dcc, register_page
import dash_bootstrap_components as dbc
from configuration import TITLE

register_page(__name__, name=TITLE)

from layout.layout_scorecards import card

layout = dbc.Container(
    children=card,
    class_name='mt-4'
)
