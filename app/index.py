# index.py

from operator import index
from dash import Dash
import dash_bootstrap_components as dbc
import pandas as pd
import geopandas as gpd

from configuration import (
    DATA_FILE,
    META_FILE,
    GEO_FILE,
    SUMMARY_FILE,
    TITLE,
    DBC_CSS,
    TEMPLATE_CSS
)

# Loading data
data = pd.read_csv(DATA_FILE)
metadata = pd.read_csv(META_FILE, index_col=0)
geodata = gpd.read_file(GEO_FILE)
summary = pd.read_csv(SUMMARY_FILE, index_col=0)

# App
app = Dash(
    __name__,
    title=TITLE,
    external_stylesheets=[TEMPLATE_CSS, DBC_CSS],
    suppress_callback_exceptions=True,
    use_pages=True
)

# Google Analytics
app.index_string = """
<!DOCTYPE html>
<html>
    <head>
        <!-- Global site tag (gtag.js) - Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=G-1348DFKDC1"></script>
        <script>
            window.dataLayer = window.dataLayer || [];
            function gtag() { dataLayer.push(arguments); }
            gtag('js', new Date());

            gtag('config', 'G-1348DFKDC1');
        </script>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
"""
