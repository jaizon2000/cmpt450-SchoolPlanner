# Import packages for data cleaning
import numpy as np
import pandas as pd

# Import Ploty Dash
import dash
import dash_html_components as html
import dash_core_components as dcc

# Bootstrap for Dash: https://bit.ly/3tKt9S3
import dash_bootstrap_components as dbc

# -------------------------------------------

# Get data
df = pd.read_csv('cmpt-courses-cleaned.csv')

# Create the app
app = dash.Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)

# Column 1 - Input
input_col = dbc.Col(
    dbc.Container([
        html.H1("Inputs"),  # Title
        dcc.Dropdown(
            options=[
                {'label': 'Edmonton', 'value': 'YEG'},
                {'label': '', 'value': ''}
            ],
            value='YEG'
        )
    ]), width={"size": 2}
)

# Column 2 - Data Tables
data_col = dbc.Col(
    dbc.Container([
        html.H1('Data Tables'),
        dbc.Row(
            html.H2("Table")
        ),
        dbc.Row(
            html.H2("Sunburst")
        )
    ]), width={"size": 6}
)

# Column 3 - Checklist
checklist_col = dbc.Col(
    dbc.Container([
        html.H1('Checklist'),
        dbc.Row(dcc.Checklist(
            options=[
                {'label': 'CMPT 101', 'value': 'check1'},
                {'label': 'MATH 114', 'value': 'check2'},
                {'label': 'MATH 120 OR MATH 125', 'value': 'check3'},
                {'label': 'STAT 151', 'value': 'check4'},
            ], value=['check1']
        ))
    ]), width=3
)

# Add content
app.layout = html.Div(
    [
        dbc.Row(
            [
                # Column 1 - Input
                input_col,

                # Column 2 - Data
                data_col,

                # Column 3 - Checklist
                checklist_col,

            ]
        ),
    ],
)

# Run the app
if __name__ == '__main__':
    app.run_server()
