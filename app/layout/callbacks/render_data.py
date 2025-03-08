import numpy as np
import pandas as pd
import plotly.express as px
import plotly.io as pio
from dash import Input, Output, html
from dash_bootstrap_templates import load_figure_template
import dash_bootstrap_components as dbc

from configuration import (
    FIGURE_TEMPLATE, 
    OCEAN_COLOR, 
    SEQUENCE_COLOR,
    TIER_BINS, 
    TIER_COLORS, 
    TIER_LABELS
)
from index import app, data, metadata
from utilis import get_score_change_arrow, get_value, sig_format, sig_round

load_figure_template(FIGURE_TEMPLATE)
pio.templates.default = FIGURE_TEMPLATE


@app.callback(
    Output("map", "figure"),
    Input("feature", "value"),
    Input('slider_year', 'value')
)
def display_map_index(feature, year):
    """
    Display a choropleth map based on the selected feature and year.

    Args:
        feature (str): The feature to display on the map.
        year (int): The year for which to display data.

    Returns:
        plotly.graph_objs._figure.Figure: The choropleth map figure.
    """
    df = data[(data['area'].notna()) & (data['year'] == year)].rename(
        columns={'year': 'Year', 'area': 'Area'}
    )
    df['Tier'] = pd.cut(
        df[feature],
        bins=TIER_BINS,
        labels=TIER_LABELS,
        right=False
    ).cat.remove_unused_categories()

    fig = px.choropleth(
        df,
        locations='code',
        color='Tier',
        color_discrete_map=dict(zip(TIER_LABELS, TIER_COLORS)),
        category_orders={'Tier': TIER_LABELS},
        custom_data=['territory', 'Area', feature, 'Tier', 'Year']
    )

    fig.update_layout(
        legend=dict(title_text="Human Rights<br>Implementation"),
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        geo=dict(
            projection_type='natural earth',
            showland=True,
            showocean=True,
            oceancolor=OCEAN_COLOR,
            showlakes=True,
            lakecolor=OCEAN_COLOR,
            showrivers=False
        )
    )

    template = (
        "<b>%{customdata[0]}</b><br>"
        "<i>%{customdata[1]}</i><br><br>"
        f"{feature}: %{{customdata[2]:#.3g}}/100<br>"
        f"Human Rights Implementation: %{{customdata[3]}}<br><br>"
        f"Year: %{{customdata[4]}}"
        "<extra></extra>"
    )
    fig.update_traces(hovertemplate=template)

    fig.update_layout(
        legend=dict(
            orientation='h',
            yanchor="bottom",
            y=-0.3,
            xanchor="left",
            x=0.01,
            yref="container"
        ),
    )

    return fig


@app.callback(
    Output("indicators_map", "figure"),
    Input("indicator", "value"),
    Input('slider_year', 'value'),
    Input('indicator_kind', 'value')
)
def display_map_indicators(indicator, year, kind):
    """
    Display a choropleth map of indicators based on selected parameters.

    Args:
        indicator (str): The indicator to display.
        year (int): The year for which to display data.
        kind (str): The kind of data to display ('Data' or 'Scores').

    Returns:
        plotly.graph_objs._figure.Figure: The choropleth map figure.
    """
    indicator = indicator.split(":")[0].split(" ")[1]
    name = metadata.loc[int(indicator)]['name']
    
    if metadata.loc[int(indicator)]['inverted'] == 'yes':
        colors = TIER_COLORS[::-1]
        limits_scale = [
            metadata.loc[int(indicator)]['best_value'],
            metadata.loc[int(indicator)]['worst_value']
        ]
    else:
        colors = TIER_COLORS
        limits_scale = [
            metadata.loc[int(indicator)]['worst_value'],
            metadata.loc[int(indicator)]['best_value']
        ]

    df = data.loc[data['year'] == year].rename(columns={'year': 'Year', 'area': 'Area'})
    
    if kind == 'Data':
        unit = metadata.loc[int(indicator)]['unit']
        col = f'Indicator {int(indicator)} (data)'
        fig = px.choropleth(
            df,
            locations='code',
            color=col,
            range_color=limits_scale,
            color_continuous_scale=colors,
            custom_data=['territory', 'Area', col, 'Year']
        )
        template = (
            "<b>%{customdata[0]}</b><br>"
            "<i>%{customdata[1]}</i><br><br>"
            f"{name}: %{{customdata[2]:#.3g}} {unit}<br><br>"
            f"Year: %{{customdata[3]}}"
            "<extra></extra>"
        )
    elif kind == 'Scores':
        unit = 'Scores'
        col = f'Indicator {int(indicator)}'
        fig = px.choropleth(
            df,
            locations='code',
            color=col,
            range_color=[0, 100],
            color_continuous_scale=TIER_COLORS,
            custom_data=['territory', 'Area', col, 'Year']
        )
        template = (
            "<b>%{customdata[0]}</b><br>"
            "<i>%{customdata[1]}</i><br><br>"
            f"{col}: %{{customdata[2]:#.3g}}/100<br><br>"
            f"Year: %{{customdata[3]}}"
            "<extra></extra>"
        )

    fig.update_traces(hovertemplate=template)
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        geo=dict(
            projection_type='natural earth',
            showland=True,
            showocean=True,
            oceancolor=OCEAN_COLOR,
            showlakes=True,
            lakecolor=OCEAN_COLOR,
            showrivers=False
        )
    )
    fig.update_layout(
        coloraxis_colorbar=dict(
            len=0.5,
            title=unit,
            orientation='h',
            yanchor="bottom",
            y=-0.3,
            xanchor="left",
            x=0.01,
            yref="container"
        ),
    )
    return fig


@app.callback(
    Output("features_correlation", "figure"),
    Input('corr_x', 'value'),
    Input('corr_y', 'value'),
    Input('corr_pop', 'value'),
    Input('slider_year', 'value')
)
def display_corr(x_data, y_data, population, year):
    """
    Display a correlation scatter plot for selected features.

    Args:
        x_data (str): Feature for x-axis.
        y_data (str): Feature for y-axis.
        population (str): Population metric to use for point size.
        year (int): Year for which to display data.

    Returns:
        plotly.graph_objs._figure.Figure: The correlation scatter plot.
    """
    df = data[(data['area'].notna()) & (data['year'] == year)].rename(
        columns={'year': 'Year', 'area': 'Area'}
    )
    x_data = x_data.split(":")[0]
    y_data = y_data.split(":")[0]
    corr = df.corr('spearman', numeric_only=True)
    df['population_milions'] = df[population] / 1e6

    fig = px.scatter(
        df,
        x=x_data,
        y=y_data,
        size=population,
        color='Area',
        color_discrete_sequence=SEQUENCE_COLOR,
        size_max=50,
        custom_data=['territory', 'Area', x_data, y_data, 'population_milions', 'Year']
    )

    template = (
        "<b>%{customdata[0]}</b><br>"
        "<i>%{customdata[1]}</i><br><br>"
        f"{x_data}: %{{customdata[2]:#.3g}}/100<br>"
        f"{y_data}: %{{customdata[3]:#.3g}}/100<br><br>"
        f"{population}: %{{customdata[4]:,.3f}} millions<br><br>"
        f"Year: %{{customdata[5]}}"
        "<extra></extra>"
    )
    fig.update_traces(hovertemplate=template)
    fig.update_layout(
        title=f"Correlation coefficient: \u03c1\u209b = {corr.loc[x_data][y_data]:#.3g}",
        legend=dict(
            orientation='h',
            yanchor="bottom",
            y=-0.3,
            xanchor="left",
            x=0.01,
            yref="container"
        ),
        margin=dict(l=20, r=20),
    )
    return fig


@app.callback(
    Output("comparison_chart", "figure"),
    Input('comp_x', 'value'),
    Input('comp_y', 'value'),
    Input('comp_pop', 'value'),
    Input('slider_year', 'value')
)
def display_comparison(x_data, y_data, population, year):
    """
    Display a comparison scatter plot for selected features.

    Args:
        x_data (str): Feature for x-axis.
        y_data (str): Feature for y-axis.
        population (str): Population metric to use for point size.
        year (int): Year for which to display data.

    Returns:
        plotly.graph_objs._figure.Figure: The comparison scatter plot.
    """
    df = data[(data['area'].notna()) & (data['year'] == year)].rename(
        columns={'year': 'Year', 'area': 'Area'}
    )
    df['population_milions'] = df[population] / 1e6
    fig = px.scatter(
        df,
        x=x_data,
        y=y_data,
        size=population,
        color='Area',
        color_discrete_sequence=SEQUENCE_COLOR,
        size_max=50,
        custom_data=['territory', 'Area', x_data, y_data, 'population_milions', 'Year']
    )
    template = (
        "<b>%{customdata[0]}</b><br>"
        "<i>%{customdata[1]}</i><br><br>"
        f"{x_data}: %{{customdata[2]:#.3g}}/100<br>"
        f"{y_data}: %{{customdata[3]:#.3g}}/100<br><br>"
        f"{population}: %{{customdata[4]:,.3f}} millions<br><br>"
        f"Year: %{{customdata[5]}}"
        "<extra></extra>"
    )
    fig.update_traces(hovertemplate=template)
    if x_data == 'GDP per capita':
        fig.update_xaxes(type='log', tickprefix='US$')
    if y_data == 'GDP per capita':
        fig.update_yaxes(type='log', tickprefix='US$')
    fig.update_layout(
        legend=dict(
            orientation='h',
            yanchor="bottom",
            y=-0.3,
            xanchor="left",
            x=0.01,
            yref="container"
        ),
        margin=dict(l=20, r=20),
    )
    return fig


@app.callback(
    Output("ranking_table", "children"),
    Input("ranking_feature", "value"),
    Input("slider_year", "value")
)
def display_ranking(feature, year):
    """
    Display a ranking table for the selected feature and year.

    Args:
        feature (str): The feature to rank.
        year (int): The year for which to display rankings.

    Returns:
        dash_bootstrap_components._components.Table: The ranking table.
    """
    df = data[data['area'].notna()].set_index('code')
    years_list = data['year'].unique()
    final = df[df['year'] == year][['territory', feature]]
    initial = df[df['year'] == years_list[0]][['territory', feature]]

    initial['Rank'] = initial[feature].rank(ascending=False, method='min')
    final['Rank'] = final[feature].rank(ascending=False, method='min')

    final[f'Score change from {years_list[0]}'] = (final[feature] - initial[feature]).apply(sig_round)
    final[f'Rank change from {years_list[0]}'] = initial['Rank'] - final['Rank']

    final = final.reset_index().rename(columns={'territory': 'Territory', feature: 'Score'}).sort_values('Rank')
    rank_change_col = f'Rank change from {years_list[0]}'
    score_change_col = f'Score change from {years_list[0]}'
    final = final.set_index(['Rank', 'Territory'], drop=True)

    rows = []
    for idx, row in final.iterrows():
        rows.append(
            html.Tr([
                html.Td(idx[0]),
                html.Td(idx[1]),
                html.Td(sig_format(row['Score']), className='number-cell'),
                html.Td(
                    html.Div([
                        get_score_change_arrow(row[score_change_col]),
                        html.Span('\u2003\u2003'),
                        html.Span(sig_format(row[score_change_col]), className='number-text'),
                    ], className='flex-container')
                ),
                html.Td(
                    html.Div([
                        get_score_change_arrow(row[rank_change_col]),
                        html.Span('\u2003'),
                        html.Span(sig_format(row[rank_change_col], precision=0), className='number-text'),
                    ], className='flex-container')
                )
            ])
        )

    table = dbc.Table(
        [html.Thead(html.Tr([html.Th(col) for col in ['Rank', 'Territory', 'Score', score_change_col, rank_change_col]]))] +
        [html.Tbody(rows)],
        bordered=False,
        hover=True,
        responsive=True,
        striped=False,
        size='sm',
        class_name='fixed-header'
    )
    return table


@app.callback(
    Output("evolution_plot", "figure"),
    Input("evolution_feature", "value"),
    Input("evolution_territory", "value")
)
def display_evolution(component, territory):
    """
    Display an evolution plot for selected features and territory.

    Args:
        component (str or list): The feature(s) to display.
        territory (str): The territory to display data for.

    Returns:
        plotly.graph_objs._figure.Figure: The evolution plot.
    """
    df = data.query("territory == @territory").rename(columns={'year': 'Year', 'territory': 'Territory'})
    if isinstance(component, list):
        component = [c.split(": ")[0] for c in component]
    else:
        component = component.split(": ")[0]
    df = pd.melt(df, id_vars=['Territory', 'Year'], value_vars=component, var_name='Component', value_name='Score')
    fig = px.line(
        df,
        x='Year',
        y='Score',
        color='Territory',
        line_dash='Component',
        markers=True,
        color_discrete_sequence=SEQUENCE_COLOR,
        custom_data=['Territory', 'Component', 'Score', 'Year']
    )
    template = (
        "<b>%{customdata[0]}</b><br><br>"
        "%{customdata[1]}: %{customdata[2]:#.3g}/100<br><br>"
        "Year: %{customdata[3]}"
        "<extra></extra>"
    )
    fig.update_traces(hovertemplate=template, marker={'size': 10})
    fig.update_layout(
        legend_title='Territory, Component',
        xaxis=dict(tickvals=df['Year'].unique()),
        yaxis=dict(title='Score'),
        legend=dict(
            orientation='h',
            yanchor="bottom",
            y=-0.3,
            xanchor="left",
            x=0.01,
            yref="container"
        ),
        margin=dict(l=20, r=20),
    )
    return fig


@app.callback(
    Output("radar_chart", "figure"),
    Input("radar_territory", "value"),
    Input("radar_year", "value")
)
def display_radar(territories, year):
    """
    Display a radar chart for selected territories and year.

    Args:
        territories (list): The territories to display.
        year (int): The year for which to display data.

    Returns:
        plotly.graph_objs._figure.Figure: The radar chart.
    """
    features = data.columns[8:23]
    df = data.query("territory == @territories and year==@year").rename(columns={'year': 'Year', 'territory': 'Territory'})
    df = pd.melt(df, id_vars=['Territory', 'Year'], value_vars=features, var_name='Dimension', value_name='Score')
    tick_labels = [f.replace(' ', '<br>') for f in features]
    fig = px.line_polar(
        df,
        theta='Dimension',
        r='Score',
        line_close=True,
        color='Territory',
        line_dash='Year',
        range_r=[0, 100],
        start_angle=90,
        color_discrete_sequence=SEQUENCE_COLOR,
        custom_data=['Territory', 'Dimension', 'Score', 'Year']
    )
    template = (
        "<b>%{customdata[0]}</b><br><br>"
        "%{customdata[1]}: %{customdata[2]:#.3g}/100<br><br>"
        "Year: %{customdata[3]}"
        "<extra></extra>"
    )
    fig.update_traces(hovertemplate=template)
    fig.update_polars(radialaxis=dict(angle=90, tickangle=90, tickfont_size=8))
    fig.update_polars(angularaxis=dict(tickvals=list(range(len(features))), ticktext=tick_labels, tickfont_size=10))
    fig.update_layout(
        legend=dict(
            orientation='h',
            yanchor="bottom",
            y=-0.3,
            xanchor="left",
            x=0.01,
            yref="container"
        ),
    )
    return fig


@app.callback(
    Output("radar_table", "children"),
    Input("radar_territory", "value"),
    Input("radar_year", "value")
)
def display_radar_table(territories, year):
    """
    Display a table of radar chart data for selected territories and year.

    Args:
        territories (list): The territories to display.
        year (int): The year for which to display data.

    Returns:
        dash_bootstrap_components._components.Table: The radar data table.
    """
    features = data.columns[8:23].to_list()
    df = data.query("territory == @territories and year==@year").rename(columns={'year': 'Year', 'territory': 'Territory'})
    df = pd.melt(df, id_vars=['Territory', 'Year'], value_vars=features, var_name='Dimension', value_name='Score')
    df = df.set_index(['Dimension', 'Territory', 'Year']).unstack(['Territory', 'Year']).loc[features]
    
    table = dbc.Table.from_dataframe(
        df,
        bordered=False,
        hover=True,
        index=True,
        responsive=True,
        striped=True,
        size='sm',
        class_name='fixed-header'
    )
    return table


@app.callback(
    [Output("indicator_num", "children"),
     Output("indicator_name", "children"),
     Output("indicator_sub", "children"),
     Output("indicator_dim", "children"),
     Output("indicator_des", "children"),
     Output("indicator_unit", "children"),
     Output("indicator_update", "children"),
     Output("indicator_source", "children"),
     Output("indicator_source", "href")],
    Input("indicator", "value")
)
def update_indicator_description(indicator):
    """
    Update the description of the selected indicator.

    Args:
        indicator (str): The selected indicator.

    Returns:
        list: A list containing the updated information for the indicator.
    """
    indicator = indicator.split(":")[0]
    data = metadata.loc[int(indicator)]
    info = [
        indicator,
        data['name'],
        data['sub-index'],
        data['dimension'],
        data['definition'],
        data['unit'],
        data['last_update'],
        data['source'],
        data['source_link']
    ]
    return info