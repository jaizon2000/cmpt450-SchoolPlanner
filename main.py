# Import packages for data cleaning
import numpy as np
import pandas as pd

# IMport Ploty Dash
import dash
import dash_html_components as html
import dash_core_components as dcc

# Get data
df = pd.read_csv('cmpt-courses-cleaned.csv')

# Create the app
app = dash.Dash()

# Add content
app.layout = html.Div([
    html.Label('Select a city:'),
    dcc.Dropdown(
        options=[
            {'label': 'Edmonton', 'value': 'YEG'},
            {'label': '', 'value': ''}
        ],
        value='YEG'
    )
])

# Run the app
# if __name__ == '__main__':
#     app.run_server()
