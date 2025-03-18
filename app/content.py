# content.py

from index import app
from dash import dcc, html, page_container
import dash_bootstrap_components as dbc

from layout.callbacks import (
    render_data,
    navigation,
    render_scorecards,
    download
)
from configuration import (
    BRAND_LINK,
    NOTES_FILE,
    REPORT_FILE,
    CREDITS_LINK,
)
from layout.layout_download import modal_data_download

# Navbar
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(
            dbc.NavLink("Home", active='exact', href='/')
        ),
        dbc.NavItem(
            dbc.NavLink("Schede", active='exact', href='/scorecards')
        ),
        dbc.NavItem(
            dbc.NavLink("Dati", active='exact', href="/data")
        ),
        dbc.NavItem(
            dbc.NavLink("Metodologia", active='exact', href="/methodology")
        ),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Rapporto", href=REPORT_FILE),
                dbc.DropdownMenuItem("Metodologia", href=NOTES_FILE),
                dbc.DropdownMenuItem("Dati", id='open_download', n_clicks=0),
                modal_data_download
            ],
            nav=True,
            label="Download",
            in_navbar=True,
            class_name='dbc'
        ),
    ],
    brand=[
        html.Img(src="assets/logo_weworld_neg.png", height='30px'),
        "\u200a\u200a\u200a\u200a",
        html.Span("Index Italia") 
    ],
    brand_href=BRAND_LINK,
    fixed='top',
    color='primary',
    dark=True
)

# Footer
footer = dbc.Navbar(
    dbc.Container(
        children=[
            html.P(
                "© 2025 WeWorld Onlus",
                style={'font-size': 'x-small'},
                className='mb-0'
            ),
            html.P(
                children=[
                    "credits: ",
                    html.A("aripiz", href=CREDITS_LINK, className='link')
                ],
                style={'font-size': 'x-small'},
                className='mb-0'
            )
        ]
    ),
    style={
        "display": "flex",
        'justify-content': 'space-between',
        'flex': '1',
        'height': '20px',
    },
    fixed='bottom',
    color="white",

)

# Page
content = dbc.Container(
    children=[
        dcc.Location(id='url', refresh='callback-nav'),
        page_container
    ],
    class_name='mt-4',
    style={'padding-top': '40px', 'padding-bottom': '120px'}
)

# Main layout
app.layout = dbc.Container(
    children=[
        navbar,
        content,
        footer
    ],
    fluid=True,
    className="dbc dbc-ag-grid",

    # style={"display": "flex", "flex-direction": "column"}
)
