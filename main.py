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

# Add content
app.layout = html.Div(
    [
        dbc.Row(
            [
                # Column 1 - Input
                dbc.Col(
                    html.Div(
                        [
                            html.H1("Inputs"),  # Title
                            dcc.Dropdown(
                                options=[
                                    {'label': 'Edmonton', 'value': 'YEG'},
                                    {'label': '', 'value': ''}
                                ],
                                value='YEG'
                            )
                        ]
                    ),
                    width={"size": 3},
                ),

                # Column 2 - Data
                dbc.Col(
                    html.Div('Data'),
                    width={"size": 3},

                ),

                # Column 3 - Checklist
                dbc.Col(
                    html.Div('Checklist'),
                    width={"size": 3},

                ),

            ]
        ),
    ]
)

# Run the app
if __name__ == '__main__':
    app.run_server()
