# utilis.py

import numpy as np
import pandas as pd
from dash import html

# Significant figures rounding
def sig_round(x, precision=3):
    return np.float64(f'{x:#.{precision}g}')


# Significant figure formatting
def sig_format(x, precision=3):
    if pd.isna(x):
        return "N/A"
    if precision == 0:
        return x
    return f'{np.float64(x):#.{precision}g}'


# Get correct colored arrow
def get_score_change_arrow(value, equal_buffer=1.5):
    if -equal_buffer <= value <= equal_buffer:
        return html.Span(className='arrow-right')
    elif value > equal_buffer:
        return html.Span(className='arrow-up')
    elif value < -equal_buffer:
        return html.Span(className='arrow-down')


# Get area centroid for scorecard map
def area_centroid(geodata, countries):
    selected_countries = geodata[geodata['ADM0_A3'].isin(countries)]
    combined_geometry = selected_countries.unary_union
    return {
        'lat': combined_geometry.centroid.y,
        'lon': combined_geometry.centroid.x
    }


# Get and format data
def get_value(dataframe, key, format_string, divide=1, default="N/A"):
    try:
        value = dataframe[key]
        if pd.isna(value):
            return default
        if divide != 1:
            value = value / divide
        return format_string.format(value)
    except (KeyError, TypeError, ValueError):
        return default
