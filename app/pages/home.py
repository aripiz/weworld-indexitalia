# home.py

from dash import html, dcc, register_page
import dash_bootstrap_components as dbc
from configuration import TITLE

register_page(__name__, path='/', name=TITLE)

from layout.layout_home_improved import home

layout = dbc.Container(
    children=home,
    class_name='mt-4'
)
