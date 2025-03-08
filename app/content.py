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
    BRAND_COLOR
)
from layout.layout_download import modal_data_download

# Navbar
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(
            dbc.NavLink("Home", active='exact', href='/')
        ),
        dbc.NavItem(
            dbc.NavLink("Scorecards", active='exact', href='/scorecards')
        ),
        dbc.NavItem(
            dbc.NavLink("Data", active='exact', href="/data")
        ),
        dbc.NavItem(
            dbc.NavLink("Methodology", active='exact', href="/methodology")
        ),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Report", href=REPORT_FILE),
                dbc.DropdownMenuItem("Technical Notes", href=NOTES_FILE),
                dbc.DropdownMenuItem("Data", id='open_download', n_clicks=0),
                modal_data_download
            ],
            nav=True,
            label="Download",
            in_navbar=True,
            class_name='dbc'
        ),
    ],
    brand=[
        html.Img(src="assets/logo_childfund.svg", height='30px'),
        "\u200a",
        html.Span("World Index", style={"font-size": "14px"}) 
    ],
    brand_href=BRAND_LINK,
    fixed='top',
    color=BRAND_COLOR,  # 'primary',
    dark=True
)

# Footer
footer = dbc.Navbar(
    dbc.Container(
        children=[
            html.P(
                "© 2024 ChildFund Alliance",
                style={'font-size': 'xx-small'},
                className='mb-0'
            ),
            html.P(
                children=[
                    "credits: ",
                    html.A("aripiz", href=CREDITS_LINK, className='link')
                ],
                style={'font-size': 'xx-small'},
                className='mb-0'
            )
        ]
    ),
    style={
        "display": "flex",
        'justify-content': 'space-between',
        'flex': '1',
        'height': '15px'
    },
    fixed='bottom',
)

# Page
content = dbc.Container(
    children=[
        dcc.Location(id='url', refresh='callback-nav'),
        page_container
    ],
    class_name='mt-4',
    style={'padding-top': '80px', 'padding-bottom': '60px'}
)

# Main layout
app.layout = dbc.Container(
    children=[
        navbar,
        content,
        footer
    ],
    fluid=False,
    className="dbc dbc-ag-grid",
    # style={"display": "flex", "flex-direction": "column"}
)
