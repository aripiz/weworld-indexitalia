# render_data.py

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
    TIER_LABELS,
    GEO_KEY
)
from index import app, data, metadata, geodata
from utilis import get_score_change_arrow, sig_format, sig_round

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
    df = data[(data['area'].notna()) & (data['year'] == year)].copy()

    df['tier'] = pd.cut(
        df[feature],
        bins=TIER_BINS,
        labels=TIER_LABELS,
        right=False
    ).cat.remove_unused_categories()

    fig = px.choropleth(
        df,
        locations='code',
        geojson=geodata,
        featureidkey=GEO_KEY,
        fitbounds="locations",
        color='tier',
        color_discrete_map=dict(zip(TIER_LABELS, TIER_COLORS)),
        category_orders={'tier': TIER_LABELS},
        custom_data=['territory', 'area', feature, 'tier', 'year']
    )

    fig.update_layout(
        legend=dict(title_text="Livello<br>di implementazione<br>dei diritti umani"),
        margin=dict(l=20, r=20),
        #margin={"r": 0, "t": 0, "l": 0, "b": 0},
        geo=dict(
            projection_type='natural earth',
            showland=False,
            showocean=False,
            oceancolor=OCEAN_COLOR,
            showlakes=False,
            lakecolor=OCEAN_COLOR,
            showrivers=False,
            projection_scale=1.0,
            #scope='europe',
            visible=False  # Questo nasconde tutto lo sfondo
        ),
    )

    template = (
        "<b>%{customdata[0]}</b><br>"
        "<i>%{customdata[1]}</i><br><br>"
        f"{feature}: %{{customdata[2]:#.3g}}/100<br>"
        f"Livello di implementazione dei diritti umani: %{{customdata[3]}}<br><br>"
        f"Anno: %{{customdata[4]}}"
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
            yref="container",
            traceorder="normal",  # Mantiene l'ordine degli elementi
            itemsizing="constant",  # Mantiene la dimensione costante
            itemwidth=70  # Imposta la larghezza massima degli elementi della legenda
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

    df = data.loc[data['year'] == year].copy()
    
    if kind == 'Dato':
        unit = metadata.loc[int(indicator)]['unit']
        col = f'Indicatore {int(indicator)} (dato)'
        fig = px.choropleth(
            df,
            locations='code',
            geojson=geodata,
            featureidkey=GEO_KEY,
            fitbounds="locations",
            color=col,
            range_color=limits_scale,
            color_continuous_scale=colors,
            custom_data=['territory', 'area', col, 'year']
        )
        template = (
            "<b>%{customdata[0]}</b><br>"
            "<i>%{customdata[1]}</i><br><br>"
            f"{name}: %{{customdata[2]:#.3g}} {unit}<br><br>"
            f"Anno: %{{customdata[3]}}"
            "<extra></extra>"
        )
    elif kind == 'Punteggio':
        unit = 'Punteggio'
        col = f'Indicatore {int(indicator)}'
        fig = px.choropleth(
            df,
            locations='code',
            geojson=geodata,
            featureidkey=GEO_KEY,
            fitbounds="locations",
            color=col,
            range_color=[0, 100],
            color_continuous_scale=TIER_COLORS,
            custom_data=['territory', 'area', col, 'year']
        )
        template = (
            "<b>%{customdata[0]}</b><br>"
            "<i>%{customdata[1]}</i><br><br>"
            f"{col}: %{{customdata[2]:#.3g}}/100<br><br>"
            f"Anno: %{{customdata[3]}}"
            "<extra></extra>"
        )

    fig.update_traces(hovertemplate=template)
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        geo=dict(
            projection_type='natural earth',
            showland=False,
            showocean=False,
            oceancolor=OCEAN_COLOR,
            showlakes=False,
            lakecolor=OCEAN_COLOR,
            showrivers=False,
            projection_scale=1.0,
            #scope='europe',
            visible=False  # Questo nasconde tutto lo sfondo
        ),
    )
    fig.update_layout(coloraxis_colorbar=dict(title=unit, x=0.92,  len=0.5,))
    # fig.update_layout(
    #     coloraxis_colorbar=dict(
    #         len=0.5,
    #         title=unit,
    #         orientation='h',
    #         yanchor="bottom",
    #         y=-0.3,
    #         xanchor="center",
    #         x=0.5,
    #         yref="paper"
    #     ),
    # )
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
    df = data[(data['area'].notna()) & (data['year'] == year)].copy()
    
    x_data = x_data.split(":")[0]
    y_data = y_data.split(":")[0]
    corr = df.corr('spearman', numeric_only=True)
    formatted_corr = f"{ corr.loc[x_data, y_data]:#.3g}" if pd.notna(corr.loc[x_data, y_data]) else "N/A"
    df['population_milions'] = df[population] / 1e6

    fig = px.scatter(
        df,
        x=x_data,
        y=y_data,
        size=population,
        color='area',
        color_discrete_sequence=SEQUENCE_COLOR,
        size_max=50,
        custom_data=['territory', 'area', x_data, y_data, 'population_milions', 'year']
    )

    template = (
        "<b>%{customdata[0]}</b><br>"
        "<i>%{customdata[1]}</i><br><br>"
        f"{x_data}: %{{customdata[2]:#.3g}}/100<br>"
        f"{y_data}: %{{customdata[3]:#.3g}}/100<br><br>"
        f"{population}: %{{customdata[4]:.3f}} milioni<br><br>"
        f"Anno: %{{customdata[5]}}"
        "<extra></extra>"
    )
    fig.update_traces(hovertemplate=template)
    fig.update_layout(
        #xaxis=dict(scaleanchor="y"),
        title=f"Coefficiente di correlazione : \u03c1\u209b = {formatted_corr}",
        legend=dict(
            title = 'Area',
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
    df = data[(data['area'].notna()) & (data['year'] == year)].copy()

    corr = df.corr('spearman', numeric_only=True)
    formatted_corr = f"{ corr.loc[x_data, y_data]:#.3g}" if pd.notna(corr.loc[x_data, y_data]) else "N/A"
    df['population_milions'] = df[population] / 1e6
    fig = px.scatter(
        df,
        x=x_data,
        y=y_data,
        size=population,
        color='area',
        color_discrete_sequence=SEQUENCE_COLOR,
        size_max=50,
        custom_data=['territory', 'area', x_data, y_data, 'population_milions', 'year']
    )
    template = (
        "<b>%{customdata[0]}</b><br>"
        "<i>%{customdata[1]}</i><br><br>"
        f"{x_data}: %{{customdata[2]:#.3g}}<br>"
        f"{y_data}: %{{customdata[3]:#.3g}}<br><br>"
        f"{population}: %{{customdata[4]:.3f}} milioni<br><br>"
        f"Anno: %{{customdata[5]}}"
        "<extra></extra>"
    )
    fig.update_traces(hovertemplate=template)
    if x_data == 'PIL per abitante':
        fig.update_xaxes(type='log', tickprefix='€')
    if y_data == 'PIL per abitante':
        fig.update_yaxes(type='log', tickprefix='€')
    
    x_source = metadata.query("name == @x_data")['source'].values[0] if metadata.query("name == @x_data")['source'].any() else "WeWorld"
    y_source = metadata.query("name == @y_data")['source'].values[0] if metadata.query("name == @y_data")['source'].any() else "WeWorld"
    sources_text = f"Fonti: {x_source}, {y_source}"
    fig.add_annotation(
            showarrow=False,
            text=sources_text,
            font=dict(size=10), 
            xref='x domain',
            x=0.5,
            yref='y domain',
            y=-0.2
        )
    fig.update_layout(
        title=f"Coefficiente di correlazione: \u03c1\u209b = {formatted_corr}",
        legend=dict(
            title = 'Area',
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

    initial['Posizione'] = initial[feature].rank(ascending=False, method='min')
    final['Posizione'] = final[feature].rank(ascending=False, method='min')

    final[f'Variazione di punteggio dal {years_list[0]}'] = (final[feature] - initial[feature]).apply(sig_round)
    final[f'Varizione di posizione dal {years_list[0]}'] = initial['Posizione'] - final['Posizione']

    final = final.reset_index().rename(columns={'territory': 'Territorio', feature: 'Punteggio'}).sort_values('Posizione')
    rank_change_col = f'Varizione di posizione dal {years_list[0]}'
    score_change_col = f'Variazione di punteggio dal {years_list[0]}'
    final = final.set_index(['Posizione', 'Territorio'], drop=True)

    rows = []
    for idx, row in final.iterrows():
        rows.append(
            html.Tr([
                html.Td(idx[0]),
                html.Td(idx[1]),
                html.Td(sig_format(row['Punteggio']), className='number-cell'),
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
        [html.Thead(html.Tr([html.Th(col) for col in ['Posizione', 'Territorio', 'Punteggio', score_change_col, rank_change_col]]))] +
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
    df = data.query("territory == @territory").copy()
    if isinstance(component, list):
        component = [c.split("Indicatore: ")[0] for c in component]
    else:
        component = component.split(": ")[0]
    df = pd.melt(df, id_vars=['territory', 'year'], value_vars=component, var_name='component', value_name='score')
    fig = px.line(
        df,
        x='year',
        y='score',
        color='territory',
        line_dash='component',
        markers=True,
        color_discrete_sequence=SEQUENCE_COLOR,
        custom_data=['territory', 'component', 'score', 'year']
    )
    template = (
        "<b>%{customdata[0]}</b><br><br>"
        "%{customdata[1]}: %{customdata[2]:#.3g}/100<br><br>"
        "Anno: %{customdata[3]}"
        "<extra></extra>"
    )
    fig.update_traces(hovertemplate=template, marker={'size': 10})
    fig.update_layout(
        legend_title='Territorio, Componente',
        xaxis=dict(tickvals=df['year'].unique()),
        yaxis=dict(title='Punteggio'),
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
    df = data.query("territory == @territories and year==@year").copy()
    df = pd.melt(df, id_vars=['territory', 'year'], value_vars=features, var_name='dimension', value_name='score')
    tick_labels = [f.replace(' ', '<br>') for f in features]
    fig = px.line_polar(
        df,
        theta='dimension',
        r='score',
        line_close=True,
        color='territory',
        line_dash='year',
        range_r=[0, 100],
        start_angle=90,
        color_discrete_sequence=SEQUENCE_COLOR,
        custom_data=['territory', 'dimension', 'score', 'year']
    )
    template = (
        "<b>%{customdata[0]}</b><br><br>"
        "%{customdata[1]}: %{customdata[2]:#.3g}/100<br><br>"
        "Anno: %{customdata[3]}"
        "<extra></extra>"
    )
    fig.update_traces(hovertemplate=template)
    fig.update_polars(radialaxis=dict(angle=90, tickangle=90, tickfont_size=8))
    fig.update_polars(angularaxis=dict(tickvals=list(range(len(features))), ticktext=tick_labels, tickfont_size=10))
    fig.update_layout(
        legend=dict(
            title='Territorio, Dimensione',
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