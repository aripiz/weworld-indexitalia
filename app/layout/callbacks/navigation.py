# navigation.py

from index import app
from dash import Input, Output, State
from urllib import parse

from layout.layout_data import (
    tab_map_features, 
    tab_map_indicators, 
    tab_correlations, 
    tab_ranking, 
    tab_evolution, 
    tab_radar, 
    tab_comparison
)

from layout.layout_methodology import tab_construction, tab_indicators

# Data tabs callback
@app.callback(
    Output("data_tab_content", "children"),
    Input("data_tabs", "active_tab")
)
def render_data_tab(active_tab):
    """
    Render the content for the selected data tab.
    """
    if active_tab is not None:
        if active_tab == "map_features":
            return tab_map_features
        elif active_tab == "map_indicators":
            return tab_map_indicators
        elif active_tab == "correlations":
            return tab_correlations
        elif active_tab == 'ranking':
            return tab_ranking
        elif active_tab == 'evolution':
            return tab_evolution
        elif active_tab == 'radar':
            return tab_radar
        elif active_tab == 'comparison':
            return tab_comparison
    return "Select a tab."

# Methodology tabs callback
@app.callback(
    Output("metho_tab_content", "children"),
    Input("metho_tabs", "active_tab")
)
def render_methodology_tab(active_tab):
    """
    Render the content for the selected methodology tab.
    """
    if active_tab is not None:
        if active_tab == "construction":
            return tab_construction
        elif active_tab == "indicators":
            return tab_indicators
    return "Select a tab."

# Collapse info callback
@app.callback(
    Output("collapse", "is_open"),
    [Input("collapse-button", "n_clicks")],
    [State("collapse", "is_open")]
)
def toggle_collapse(n_clicks, is_open):
    """
    Toggle the collapse state of the info section.
    """
    if n_clicks:
        return not is_open
    return is_open

# Scorecard link callback
@app.callback(
    Output('url', 'pathname'),
    Input('map_home', 'clickData')
)
def navigate_to_scorecard(clickData):
    """
    Update the URL to navigate to the scorecard page when a country is clicked on the map.
    """
    if clickData:
        country = clickData['points'][0]['customdata'][0]
        return f'/scorecards?country={parse.quote(country)}'
    return '/'

# Update dropdown callback
@app.callback(
    Output('scorecard_territory', 'value'),
    [Input('url', 'pathname'), Input('url', 'search')]
)
def update_dropdown(pathname, search):
    """
    Update the dropdown value based on the URL parameters when on the scorecards page.
    """
    if pathname == '/scorecards' and search:
        country = parse.unquote(search.split('=')[-1])
        return country
    return 'Italia'
