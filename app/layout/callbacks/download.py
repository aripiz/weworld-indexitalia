# download.py

#from fileinput import filename
from dash import Input, Output, State, dcc, callback_context
import pandas as pd
import io

from index import app, metadata, data


# Set the index name for metadata
metadata.index.name = 'indicator'

# Toggle the modal open/close state based on button clicks.
@app.callback(
    Output("modal", "is_open"),
    [Input("open_download", "n_clicks"), Input("close_download", "n_clicks")],
    [State("modal", "is_open")],
)
def toggle_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


# Generate and download an Excel file with selected data and metadata.
@app.callback(
    Output("download_file", "data"),
    [
        Input("download_button", "n_clicks"),
        Input('download_indicator', 'value'),
        Input('download_territory', 'value')
    ],
    prevent_initial_call=True,
)
def download_excel(n_clicks, features, territories):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    
    if 'download_button' in changed_id:
        # Define columns to include in metadata sheet
        meta_columns = [
            'sub-index', 'dimension', 'name', 'unit', 'definition', 
            'last_update', 'source', 'source_link'
        ]
        df_meta = metadata[meta_columns]

        # Prepare data for export
        df_data = data.set_index(['territory', 'year'])
        
        if features is not None:
            df_data = df_data[features]
        if territories is not None:
            df_data = df_data.loc[territories]

        # Create a buffer to hold the Excel file content
        buffer = io.BytesIO()
        
        with pd.ExcelWriter(buffer) as writer:
            df_meta.to_excel(writer, sheet_name='indicators_metadata')
            df_data.to_excel(writer, sheet_name='data', float_format='%#.3g')
        
        return dcc.send_bytes(buffer.getvalue(), filename="weworld-indexitalia-2025_data.xlsx")
    
    return None
