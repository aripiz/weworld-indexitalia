import dash_bootstrap_components as dbc
from dash import dcc, html
import plotly.express as px
import plotly.io as pio
import pandas as pd
from dash_bootstrap_templates import load_figure_template
from index import data, geodata
from configuration import (
    FIGURE_TEMPLATE,
    GEO_KEY,
    INDEX_KEY,
    TIER_COLORS,
    TIER_BINS,
    TIER_LABELS,
    OCEAN_COLOR,
    BRAND_LINK,
    SEQUENCE_COLOR
)

# Load figure template
load_figure_template(FIGURE_TEMPLATE)
pio.templates.default = FIGURE_TEMPLATE

# Home map
def display_map():
    year = 2023
    feature = INDEX_KEY
    df = data[(data['area'].notna()) & (data['year'] == year)].rename(columns={'year': 'Year', 'area': 'Area'})
    df['Tier'] = pd.cut(df[feature], bins=TIER_BINS, labels=TIER_LABELS, right=False).cat.remove_unused_categories()

    fig = px.choropleth(
        df,
        locations='code',
        geojson=geodata,
        featureidkey=GEO_KEY,
        fitbounds="locations",
        color='Tier',
        color_discrete_map=dict(zip(TIER_LABELS, TIER_COLORS)),
        category_orders={'Tier': TIER_LABELS},
        custom_data=['territory', 'Area', feature, 'Tier', 'Year'],
    )

    fig.update_layout(
        legend=dict(
            title_text="Human Rights Implementation",
            xanchor='right',
            yanchor='top',
            x=0.95,
            y=0.92
        ),
        coloraxis_colorbar=dict(
            title="Score",
            x=0.92
        ),
        showlegend=False,
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

    template = (
        "<b>%{customdata[0]}</b><br>"
        + "<i>%{customdata[1]}</i><br><br>"
        + f"{feature}: " + "%{customdata[2]:#.3g}/100<br>"
        + "Human Rights Implementation: %{customdata[3]}<br><br>"
        + "Year: %{customdata[4]}"
        + "<extra></extra>"
    )
    fig.update_traces(hovertemplate=template)

    return fig

# Text
opening_text = '''
The **ChildFund Alliance World Index 2024 Edition** is a flagship report by **ChildFund Alliance**. It is a tool designed to **measure the living conditions of women and children worldwide** by assessing the promotion, exercise, and violation of their rights.
'''

description_text = '''
ChildFund Alliance World Index is formerly known as the WeWorld Index and published annually since 2015 by WeWorld, the Italian member of ChildFund Alliance. The Index ranks **157 countries** from 2015 to 2023 combining **30 different indicators.** For each territory, an absolute 0-100 score is computed, aiming to inquire the implementation of human rights for children and women at the country, regional area, and world level.

Explore the dashboard for more details:

- **[Scorecards](/scorecards):** Country scorecards showing scores and rankings based on various indicators.
- **[Data](/data):** Access detailed data that make up the Index, with the ability to view interactive maps and charts.
- **[Methodology](/methodology):** Description of the methodology used to collect and analyze data.

Navigate through these sections to better understand the impact of the ChildFund Alliance World Index and discover how the rights of women and children are promoted, exercised, and violated in different countries. All resources, including full reports and datasets, are available to download.
'''

about_text = f'''
[ChildFund Alliance]({BRAND_LINK}) is a global network of 11 child-focused development and humanitarian organizations reaching nearly 30 million children and family members in more than 70 countries. 
Members work to end violence and exploitation against children; provide expertise in emergencies and disasters to ease the harmful impact on children and their communities; and engage children, families and communities to create lasting change. With more than 80 years of collective experience, our commitment, resources, innovation and expertise serve as a powerful force to help children and families around the world transform their lives. 
'''

# Structure
home = dbc.Container(
    children=[
        dbc.Row(
            dbc.Col(
                children=[
                    html.H1("ChildFund Alliance World Index"),
                    dcc.Markdown(opening_text, className='my-4'),
                    html.P("Click on the map to access country scorecards.", style={"text-align": "center"}),
                    dcc.Loading(
                        dcc.Graph(
                            figure=display_map(),
                            config={'displayModeBar': False, 'editable': False},
                            id='map_home'
                        ),
                        color=SEQUENCE_COLOR[0]
                    ),
                    dcc.Markdown(description_text, className='my-4'),
                ],
                lg=12,
                xs=12
            ),
            className='mt-2',
            justify='around'
        ),
        dbc.Row(
            dbc.Col(
                children=[
                    html.H4("About ChildFund Alliance"),
                    dcc.Markdown(about_text)
                ],
                lg=12,
                xs=12
            ),
            className='mt-4',
            justify='around'
        ),
    ]
)
