# render_scorecards.py

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.io as pio

import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
from dash import Input, Output, html

from index import app, data, geodata, metadata
from configuration import (
    OCEAN_COLOR, 
    SEQUENCE_COLOR, 
    TIER_LABELS, 
    TIER_BINS,
    FIGURE_TEMPLATE, 
    LAND_COLOR
)
from utilis import (
    sig_round, 
    get_score_change_arrow, 
    sig_format, 
    area_centroid,
    get_value
)

# Load Plotly figure template
load_figure_template(FIGURE_TEMPLATE)
pio.templates.default = FIGURE_TEMPLATE

# Create area to code mappings and centroids
areas = {area: data[data['area'] == area]['code'].dropna().unique().tolist()
         for area in data['area'].dropna().unique()}
areas['World'] = data['code'].unique().tolist()

centroids = {
    row['ADM0_A3']: {
        'lat': row['geometry'].centroid.y,
        'lon': row['geometry'].centroid.x
    }
    for _, row in geodata.iterrows()
}
centroids.update({k: area_centroid(geodata, v) for k, v in areas.items()})


# Callback to update the scorecard title based on the selected territory
@app.callback(
    Output("scorecard_header", "children"),
    Input('scorecard_territory', 'value')
)
def update_scorecard_title(territory):
    return territory


# Callback to update the scorecard map based on the selected territory
@app.callback(
    Output("scorecard_map", "figure"),
    Input('scorecard_territory', 'value')
)
def update_scorecard_map(territory):
    if territory in areas:
        df = data[(data['area'] == territory)].rename(columns={'year': 'Year', 'area': 'Area'})
        lat, lon = centroids[territory].values()
    else:
        df = data[(data['territory'] == territory)].rename(columns={'year': 'Year', 'area': 'Area'})
        lat, lon = centroids[df['code'].values[0]].values()

    fig = px.choropleth(
        df,
        locations='code',
        color_discrete_sequence=[LAND_COLOR],
        hover_name='territory',
        hover_data={
            'code': False,
            'Year': False,
            'Area': False
        }
    )
    fig.update_layout(
        showlegend=False,
        margin={
            "r": 0,
            "t": 0,
            "l": 0,
            "b": 0
        },
        geo=dict(
            projection_type='orthographic',
            projection_scale=1.0,
            showland=True,
            showocean=True,
            oceancolor=OCEAN_COLOR,
            showlakes=True,
            lakecolor=OCEAN_COLOR,
            showrivers=False,
            scope='world'
        )
    )
    if territory == 'World':
        fig.update_layout(
            geo=dict(
                center=dict(lat=0, lon=0),
                projection_rotation=dict(lat=0, lon=0),
                landcolor=LAND_COLOR
            )
        )
    else:
        fig.update_layout(
            geo=dict(
                center=dict(lat=lat, lon=lon),
                projection_rotation=dict(lat=lat, lon=lon)
            )
        )
    return fig


# Callback to update the scorecard summary based on the selected territory
@app.callback(
    Output("scorecard_area", "children"),
    Output("scorecard_pop", "children"),
    Output("scorecard_gdp", "children"),
    Output("scorecard_score", "children"),
    Output("scorecard_rank", "children"),
    Output("scorecard_group", "children"),
    Input('scorecard_territory', 'value')
)
def update_scorecard_summary(territory):
    df_territory = data[data['year'] == 2023].set_index('territory').loc[territory]
    df_all = data[(data['area'].notna()) & (data['year'] == 2023)].set_index('territory')
    df_territory['tier'] = pd.cut(
        pd.Series(df_territory['CFA World Index']),
        bins=TIER_BINS,
        labels=TIER_LABELS,
        right=False
    ).iloc[0]
    try:
        df_territory['rank'] = df_all['CFA World Index'].rank(
            ascending=False,
            method='min'
        ).loc[territory]
    except KeyError:
        df_territory['rank'] = np.nan

    values = [
        get_value(df_territory, 'area', "{}"),
        get_value(df_territory, 'Population, total', "{:,.3f} millions", divide=1e6),
        get_value(df_territory, 'GDP per capita', "US${:,.0f}"),
        get_value(df_territory, 'CFA World Index', "{}/100"),
        get_value(df_territory, 'rank', "{:.0f}/157"),
        get_value(df_territory, 'tier', "{}"),
    ]
    return values


# Callback to display scorecard progress as a line chart
@app.callback(
    Output("scorecard_progress", "figure"),
    Input("scorecard_territory", "value")
)
def display_evolution(territory):
    area = data.query("territory == @territory")['area'].to_list()[0]
    if territory != "World":
        territory = [territory, area, 'World']

    df = data.query("territory == @territory").rename(
        columns={'year': 'Year', 'territory': 'Territory'}
    )
    fig = px.line(
        df,
        x='Year',
        y='CFA World Index',
        color='Territory',
        color_discrete_sequence=SEQUENCE_COLOR,
        markers=True,
        custom_data=['Territory', 'CFA World Index', 'Year']
    )
    fig.update_traces(marker={'size': 10})
    template = (
        "<b>%{customdata[0]}</b><br><br>" +
        "CFA World Index: " + "%{customdata[1]:#.3g}/100<br><br>" +
        "Year: " + "%{customdata[2]}" +
        "<extra></extra>"
    )
    fig.update_traces(hovertemplate=template)
    fig.update_layout(
        legend_title='Territory',
        xaxis=dict(tickvals=df['Year'].unique()),
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


# Callback to display scorecard radar chart
@app.callback(
    Output("scorecard_radar", "figure"),
    Input("scorecard_territory", "value")
)
def display_radar(territory):
    features = data.columns[8:23]
    area = data.query("territory == @territory")['area'].to_list()[0]
    if territory != "World":
        territory = [territory, area, 'World']

    df = data.query("territory == @territory and year == 2023").rename(
        columns={'territory': 'Territory'}
    )
    df = pd.melt(
        df,
        id_vars=['Territory'],
        value_vars=features,
        var_name='Dimension',
        value_name='Score'
    )
    tick_labels = [f.replace(' ', '<br>') for f in features]
    fig = px.line_polar(
        df,
        theta='Dimension',
        r='Score',
        line_close=True,
        color='Territory',
        range_r=[0, 100],
        start_angle=90,
        custom_data=['Territory', 'Dimension', 'Score']
    )
    template = (
        "<b>%{customdata[0]}</b><br><br>" +
        "%{customdata[1]}: " + "%{customdata[2]:#.3g}/100<br><br>" +
        "<extra></extra>"
    )
    fig.update_traces(hovertemplate=template)
    fig.update_polars(
        radialaxis=dict(
            angle=90,
            tickangle=90,
            tickfont_size=8
        ),
        angularaxis=dict(
            tickvals=list(range(len(features))),
            ticktext=tick_labels,
            tickfont_size=10
        )
    )
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


# Callback to display the scorecard table
@app.callback(
    Output("scorecard_table", "children"),
    Input("scorecard_territory", "value")
)
def display_table(territory):
    features = data.columns[4:53]
    area = data.query("territory == @territory")['area'].to_list()[0]
    world = "World"

    if territory == world:
        territory_list = [territory]
    else:
        if pd.isna(area):
            territory_list = [territory, world]
        else:
            territory_list = [territory, area, world]

    df = data.query("territory == @territory_list and year == 2023").rename(
        columns={'territory': 'Territory'}
    )

    # Get data for the specific territory, area, and world
    df_territory = df[df['Territory'] == territory]
    df_area = df[df['Territory'] == area]
    df_world = df[df['Territory'] == world]

    rows = []
    for feature in features:
        component_name = (
            feature + ": " +
            metadata.loc[int(feature.split('Indicator ')[1])]['name']
            if 'Indicator ' in feature else feature
        )
        score = df_territory[feature].values[0]

        if territory == world:
            score_change_from_area = np.nan
            score_change_from_world = np.nan
        elif territory in areas:
            score_change_from_area = np.nan
            score_change_from_world = sig_round(score - df_world[feature].values[0])
        else:
            score_change_from_area = sig_round(score - df_area[feature].values[0])
            score_change_from_world = sig_round(score - df_world[feature].values[0])

        if pd.isna(score):
            score_change_from_area = np.nan
            score_change_from_world = np.nan

        rows.append(
            html.Tr([
                html.Td(component_name),
                html.Td(sig_format(score), className='number-cell'),
                html.Td(
                    html.Div([
                        get_score_change_arrow(score_change_from_area),
                        html.Span('\u2003\u2003'),
                        html.Span(sig_format(score_change_from_area), className='number-text'),
                    ], className='flex-container')
                ),
                html.Td(
                    html.Div([
                        get_score_change_arrow(score_change_from_world),
                        html.Span('\u2003'),
                        html.Span(sig_format(score_change_from_world), className='number-text'),
                    ], className='flex-container')
                )
            ])
        )

    # Create table with header
    table = dbc.Table(
        [html.Thead(html.Tr([html.Th(col) for col in [
            'Component', 'Score', 'Difference from Area', 'Difference from World'
        ]]))] +
        [html.Tbody(rows)],
        bordered=False,
        hover=True,
        responsive=True,
        striped=False,
        size='sm',
        class_name='fixed-header'
    )

    return table
