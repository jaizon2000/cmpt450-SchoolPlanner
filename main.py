# Import packages for data cleaning
import numpy as np
import pandas as pd

# Import Ploty Dash
import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table

# App Callback for Dash
from dash.dependencies import Input, Output, State

# Bootstrap for Dash: https://bit.ly/3tKt9S3
import dash_bootstrap_components as dbc

from Course import *

# -------------------------------------------

# Get data
df = pd.read_csv('cmpt-courses-cleaned.csv')

# Create the app and add extra styles
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)


class CollapseList:
    def __init__(self):
        self.list = []

    def append(self, other):
        self.list.append(other)

    def getList(self):
        return self.list  # list of id string of collapse groups


collapseList = CollapseList()


def makeCollapse(i):
    # course_id = course.id.split(' ')

    # collapseList.append(f"{course_id[0]}-{course_id[1]}-collapse-toggle")

    return dbc.Card(
        [
            dbc.CardHeader(
                html.H2(
                    dbc.Button(
                        f"Collapsible group #{i}",
                        color="link",
                        id=f"group-{i}-toggle",
                    )
                )
            ),
            dbc.Collapse(
                dbc.CardBody(f"This is the content of group {i}..."),
                id=f"collapse-{i}",
            ),
        ]
    )


cmpt103 = Course("CMPT 103", "Introduction to Computing II", 3,
                 "This course continues the overview of computing science concepts that was started in CMPT 101. Topics include representation of compound data using abstraction, programming languages, and modularity; algorithms that use these data structures; and networks with the TCP/IP model and client/server architecture. Students continue with the syntax of a high-level programming language: functions, arrays, and user-defined data types.",
                 ())

'''
Column 1 - Input
'''
input_col = dbc.Col(
    dbc.Container([

        html.H1("Inputs"),  # Title

        dbc.Row(dbc.Col([
            html.B("Courses"),
            dcc.Dropdown(
                options=[
                    {'label': 'Edmonton', 'value': 'YEG'},
                    {'label': '', 'value': ''}
                ],
                value='YEG'
            )
        ])),

        dbc.Row(dbc.Col([
            makeCollapse(1),
            makeCollapse(2),
            makeCollapse(3),
        ])),

        dbc.Row(dbc.Col([
            html.B("Mark selected course(s) as:"),
            dcc.RadioItems(
                options=[
                    {'label': 'Completed', 'value': 'done'},
                    {'label': 'Work In Progress', 'value': 'wip'},
                    {'label': 'Planning to Take', 'value': 'planned'}
                ],
                value='done',
                labelStyle={'display': 'block'}  # make new line option
            ),
            dbc.Button("Add to Planner", color="primary", id='add-to-planner', n_clicks=0),

        ])),

        dbc.Container([
            dbc.Row(html.B("Change view:")),
            dbc.Row([
                dbc.Button("Default", color="primary", id='view-btn-default', n_clicks=0),
                dbc.Button("Sunburst", color="primary", id='view-btn-sun', n_clicks=0),
                html.Div(id='container-button-timestamp')
            ]),
        ]),

        # dbc.Row(dbc.Col([])),
    ]), width=3
)

print(' '.join(map(str, collapseList.getList())))
'''
Column 2 - Data Tables
'''
data_col = dbc.Col(
    dbc.Container([
        html.H1('Data Tables'),
        dbc.Row(dbc.Col([
            html.H2("Table"),
            dash_table.DataTable(id='table',
                                 columns=[
                                     {'name': 'Course ID', 'id': 'course-id', 'type': 'numeric'},
                                     {'name': 'Title', 'id': 'title', 'type': 'text'},
                                     {'name': 'Prerequisites', 'id': 'prereq', 'type': 'numeric'},
                                 ],
                                 data=df.to_dict('records'),
                                 filter_action='native',
                                 ),
        ])),
        dbc.Row([
            html.H2("Sunburst"),
        ])
    ]), width=6
)

'''
Column 3 - Checklist
'''
checklist_col = dbc.Col(
    dbc.Container([
        html.H1('Computer Science Major Checklist'),

        # Declaring Computer Science
        dbc.Row(dbc.Col([
            html.B('Declaring Computer Science'),
            dcc.Checklist(
                options=[
                    {'label': 'CMPT 101', 'value': 'check1'},
                    {'label': 'MATH 114', 'value': 'check2'},
                    {'label': 'MATH 120 OR MATH 125', 'value': 'check3'},
                    {'label': 'STAT 151', 'value': 'check4'},
                ],
                value=['check1'],
                labelStyle={'display': 'block'}
            )
        ])),

        # Computer Science Major
        dbc.Row(dbc.Col([
            html.B('Computer Science Major'),
            dcc.Checklist(
                options=[
                    {'label': 'CMPT 101', 'value': 'check1'},
                    {'label': 'MATH 114', 'value': 'check2'},
                    {'label': 'MATH 120 OR MATH 125', 'value': 'check3'},
                    {'label': 'STAT 151', 'value': 'check4'},
                ],
                value=['check1'],
                labelStyle={'display': 'block'}
            )
        ])),

        # Gaming Stream
        dbc.Row(dbc.Col([
            html.B('Gaming Stream'),
            dcc.Checklist(
                options=[
                    {'label': 'CMPT 101', 'value': 'check1'},
                    {'label': 'MATH 114', 'value': 'check2'},
                    {'label': 'MATH 120 OR MATH 125', 'value': 'check3'},
                    {'label': 'STAT 151', 'value': 'check4'},
                ],
                value=['check1'],
                labelStyle={'display': 'block'}
            )
        ])),

        dbc.Row(dbc.Col([
            html.B('Credits'),
            dcc.Checklist(
                options=[
                    {'label': 'CMPT 101', 'value': 'check1'},
                    {'label': 'MATH 114', 'value': 'check2'},
                    {'label': 'MATH 120 OR MATH 125', 'value': 'check3'},
                    {'label': 'STAT 151', 'value': 'check4'},
                ],
                value=['check1'],
                labelStyle={'display': 'block'}  # make new line per check list
            )
        ])),

    ]), width=3
)

'''
MAIN: Add content
'''
app.layout = html.Div(style={'backgroundColor': '#00000'},
                      children=[

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


@app.callback(
    # Output('container-button-timestamp', 'children'),

    [Output(f"collapse-{i}", "is_open") for i in range(1, 4)],

    # Input('view-btn-default', 'n_clicks'),
    # Input('view-btn-sun', 'n_clicks'),

    [Input(f"group-{i}-toggle", "n_clicks") for i in range(1, 4)],
    [State(f"collapse-{i}", "is_open") for i in range(1, 4)],
)
# def displayClick(btn1, btn2):
#     print(btn1)
#     changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
#     # print(changed_id)
#     if 'view-btn-default' in changed_id:
#         msg = 'Button 1 was most recently clicked'
#         changed_id
#     elif 'view-btn-sun' in changed_id:
#         msg = 'Button 2 was most recently clicked'
#     return html.Div(msg)

def toggle_accordion(n1, n2, n3, is_open1, is_open2, is_open3):
    ctx = dash.callback_context

    if not ctx.triggered:
        return False, False, False
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]

    if button_id == "group-1-toggle" and n1:
        return not is_open1, False, False
    elif button_id == "group-2-toggle" and n2:
        return False, not is_open2, False
    elif button_id == "group-3-toggle" and n3:
        return False, False, not is_open3
    return False, False, False


# Run the app
if __name__ == '__main__':
    app.run_server()
