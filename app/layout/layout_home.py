# layout_home.py

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
    df = data[(data['area'].notna()) & (data['year'] == year)].copy()
    df['tier'] = pd.cut(df[feature], bins=TIER_BINS, labels=TIER_LABELS, right=False).cat.remove_unused_categories()

    fig = px.choropleth(
        df,
        locations='code',
        geojson=geodata,
        featureidkey=GEO_KEY,
        fitbounds="locations",
        color='tier',
        color_discrete_map=dict(zip(TIER_LABELS, TIER_COLORS)),
        category_orders={'tier': TIER_LABELS},
        custom_data=['territory', 'area', feature, 'tier', 'year'],
    )

    fig.update_layout(
        dragmode=False,
        showlegend=False,
        autosize=True,
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        geo=dict(
            projection_type='natural earth',
            showland=False,
            showocean=False,
            showlakes=False,
            showrivers=False,
            #scope='europe',
            visible=False 
        ),
    )

    template = (
        "<b>%{customdata[0]}</b><br>"
        + "<i>%{customdata[1]}</i><br><br>"
        + f"{feature}: " + "%{customdata[2]:#.3g}/100<br>"
        + "Livello di implementazione dei diritti umani: %{customdata[3]}<br><br>"
        #+ "Anno: %{customdata[4]}"
        + "<extra></extra>"
    )
    fig.update_traces(hovertemplate=template)

    return fig

# Text
opening_text = f'''
Il **WeWorld Index Italia 2025** è un rapporto originale di [WeWorld]({BRAND_LINK}) che, giunto alla sua quarta edizione, fornisce un'istantanea delle condizioni di vita di donne, bambini, bambine e adolescenti in Italia.
'''

description_text = '''
Il WeWorld Index Italia classifica le 21 regioni italiane combinando 30 diversi indicatori con dati dal 2018 al 2023. 
Per ogni territorio viene calcolato un punteggio assoluto da 0 a 100, con l'obiettivo di indagare l'implementazione dei diritti umani per donne e minori a livello locale, regionale e nazionale.

Esplora la dashboard per maggiori dettagli:
- **[Schede di valutazione](/scorecards):** Le schede di valutazione delle 21 regioni italiane offrono una panoramica dei punteggi e delle classifiche specifiche per ciascuna regione, analizzando le performance degli indicatori e permettendo una visione dettagliata della situazione a livello territoriale.
- **[Dati](/data):** Accedi ai dati completi che costituiscono l'Indice, con la possibilità di esplorare mappe interattive e grafici dinamici per un'analisi approfondita e chiara.
- **[Metodologia](/methodology):** Scopri la metodologia utilizzata per raccogliere e analizzare i dati, comprendendo i criteri e i processi che guidano la costruzione dell'Indice.

Naviga attraverso queste sezioni per comprendere appieno l'impatto del WeWorld Index Italia 2025 e per esplorare come i diritti delle donne e dei minori vengano implementati o violati nel territorio italiano. 
Tutte le informazioni e i dataset sono disponibili per il download, offrendoti un accesso diretto alle risorse.
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
                    html.H1("WeWorld Index Italia 2025", className='text-center'),
                    dcc.Markdown(opening_text, className='my-4'),
                ],
                lg=12,
                xs=12,
            ),
            className='mt-2',
            justify='around'
        ),
        dbc.Row(
            [
            dbc.Col(
                children=[
                    dcc.Markdown("### Esplora l'Indice", className='my-4'),
                    dcc.Markdown(description_text, className='my-4'),

                ],
                lg=5,
                xs=12
            ),
            dbc.Col(
                children=[
                    dcc.Loading(
                        dcc.Graph(
                            figure=display_map(),
                            config={'displayModeBar': False, 'editable': False,},
                            id='map_home',
                            #style={'width': '100%', 'height': '80vh'},
                            className="d-flex justify-content-center" 
                        ),
                        color=SEQUENCE_COLOR[0]
                    ),
                    dcc.Markdown("_Clicca su una regione per accedere alla sua scheda di valutazione._", style={"text-align": "center"})

                ],
                lg=7,
                xs=12
            ),],
            className='mt-4',
            justify='around'
        ),
        # dbc.Row(
        #     dbc.Col(
        #         children=[
        #             html.H4("About ChildFund Alliance"),
        #             dcc.Markdown(about_text)
        #         ],
        #         lg=12,
        #         xs=12
        #     ),
        #     className='mt-4',
        #     justify='around'
        # ),
    ],
)
