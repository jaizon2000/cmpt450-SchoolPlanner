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
from Student import *

# -------------------------------------------

# Get data
df = pd.read_csv('cmpt-courses-cleaned.csv')
df_dict = df.to_dict('records')
stud_df = df.copy().iloc[0:0]  # erase all rows but keep cols: https://bit.ly/2PCF5Xi
# print(stud_df, df)
course_class_list = [Course(c['id'], c['name'], c['credit'], c['description'], c['prereq']) for c in df_dict]

# Create the app and add extra styles
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)


# Helper Classes
class CollapseList:
    def __init__(self, size):
        self.list = []
        self.size = size

    def append(self, other):
        self.list.append(other)
        self.size += 1

    def getList(self):
        return self.list  # list of id string of collapse groups

    def size(self):
        return self.size


collapseList = CollapseList(len(df))


class Bools():
    """
    Bools: class to toggle course accordions
    """

    def __init__(self, bool_list):
        self.list = bool_list

    def list(self):
        return self.list

    def toggle(self, i):
        """
        toggle the boolean at given i pos
        :param i: which pos in list to toggle
        :return: return edited list
        """
        self.list[i] = not self.list[i]
        return self.list


bools = Bools([None for i in range(len(df))])


def makeCollapse(i, course):
    # course_id = course.id.split(' ')

    # collapseList.append(f"{course_id[0]}-{course_id[1]}-collapse-toggle")
    collapseList.getList().append(f"{i}")
    return dbc.Card(
        [
            # CARD TITLE
            dbc.CardHeader(
                html.H2(
                    dbc.Button(
                        f"{course.id}",
                        color="link",
                        id=f"group-{i}-toggle",
                    )
                )
            ),

            # CARD CONTENT
            dbc.Collapse(
                dbc.CardBody([
                    html.H5(f"{course.name}", className="card-title"),
                    html.H6(f"{course.credit} Credits", className="card-subtitle"),
                    html.P(f"{course.desc}", className="card-text"),
                    dbc.CardFooter(f"{str(course.prereq)}"),
                ]),
                id=f"collapse-{i}",
            ),
        ]
    )


'''
Column 1 - Input
'''
input_col = dbc.Col(
    dbc.Container([

        html.H1("Inputs"),  # Title

        html.H4("Find Courses"),
        # Course Collapse Descriptions
        dbc.Row(dbc.Col([
            # makeCollapse(c + 1, course_class_list[c]) for c in range(len(course_class_list))
            makeCollapse(i, course_class_list[i]) for i in range(len(df))
            # makeCollapse(1, course_class_list[3]),
            # makeCollapse(2, course_class_list[2]),
            # makeCollapse(3, course_class_list[1]),
            # makeCollapse(i) for i in course_class_list
        ]),
            style={'overflow': 'scroll', 'height': '50vh', 'overflowX': 'hidden'},  # style container
        ),

        html.H4("Mark selected course(s) as:"),

        # MULTI SELECTED COURSES
        dbc.Row(dbc.Col([
            dcc.Dropdown(
                id='courses-input',
                options=[
                    {'label': c['id'], 'value': c['id'.replace(' ', '-')]} for c in df_dict
                ],
                placeholder='Select Courses...',
                multi=True,
            )
        ])),

        # COURSE STATUS RADIO BTNS
        dbc.Row(dbc.Col([
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

        # CHANGE VIEW BTNS
        html.H4("Change view:"),
        dbc.Container([
            dbc.Row([
                dbc.Button("Default", color="primary", id='view-btn-default', n_clicks=0),
                dbc.Button("Sunburst", color="primary", id='view-btn-sun', n_clicks=0),
                html.Div(id='container-button-timestamp')
            ]),
        ]),

        # dbc.Row(dbc.Col([])),
    ]),
    width=3
)

'''
Column 2 - Data Tables
'''
data_col = dbc.Col(
    dbc.Container([
        html.H1('My Progress'),
        dbc.Row(dbc.Col([
            html.H2("Table"),
            # Filtering data table: https://bit.ly/31tUrjG
            # datatable basic: https://bit.ly/3fmu0EB
            dash_table.DataTable(
                id='my-table',
                # columns=[{'id': c, 'name': c.title()} for c in df.columns],
                columns=[
                    {'id': 'id', 'name': 'Course ID'},
                    {'id': 'name', 'name': 'Course Name'},
                    {'id': 'credit', 'name': 'Credits'},
                    {'id': 'prereq', 'name': 'Prerequisites'},

                ],

                data=stud_df.to_dict('records'),  # data to use
                filter_action='native',  # for filtering

                # table styling
                style_table={
                    'height': 400,
                    'overflowX': 'auto',  # scroll: https://bit.ly/3waaEII
                    'overflowY': 'auto',
                },

                # style columns
                style_data={
                    'minWidth': '25px',
                    'overflow': 'hidden',
                    'textOverflow': 'ellipsis',
                },

                # specific column styles
                style_cell_conditional=[
                    {'if': {'column_id': 'prereq'},
                     'whiteSpace': 'normal',
                     'height': 'auto'},

                    {'if': {'column_id': 'name'},

                     'width': 'auto'},
                ],
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
app.layout = html.Div(style={'backgroundColor': '#00000', 'overflowX': 'hidden'},
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
    # OUTPUTS - should come first
    # Output('container-button-timestamp', 'children'),

    [Output(f"collapse-{i}", "is_open") for i in collapseList.getList()],  # course toggles
    Output('my-table', 'data'),
    # INPUTS - comes after outputs
    # Input('view-btn-default', 'n_clicks'),
    # Input('view-btn-sun', 'n_clicks'),

    [Input(f"group-{i}-toggle", "n_clicks") for i in range(len(df))],  # course toggles
    [State(f"collapse-{i}", "is_open") for i in range(len(df))],  # course toggles
)
def update_my_table(selected_courses):
    pass


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

def toggle_accordion(n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13, n14, n15, n16, n17, n18, n19, n20, n21,
                     n22, n23, n24, n25, n26, n27, n28, n29, n30, n31, n32, n33, n34, n35, n36, n37, n38, n39,

                     is_open1, is_open2, is_open3, is_open4, is_open5, is_open6, is_open7, is_open8, is_open9,
                     is_open10, is_open11, is_open12, is_open13, is_open14, is_open15, is_open16, is_open17, is_open18,
                     is_open19, is_open20, is_open21, is_open22, is_open23, is_open24, is_open25, is_open26, is_open27,
                     is_open28, is_open29, is_open30, is_open31, is_open32, is_open33, is_open34, is_open35, is_open36,
                     is_open37, is_open38, is_open39):
    ctx = dash.callback_context

    if not ctx.triggered:
        return [False for i in range(len(df))]
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]  # group-X-toggle

    print(button_id)

    for i in range(len(df)):
        if button_id == f"group-{i}-toggle":
            bools.toggle(i)
            return bools.list
    # if button_id == "group-0-toggle" and n1:
    #     return not is_open1, False, False
    # elif button_id == "group-1-toggle" and n2:
    #     return False, not is_open2, False
    # elif button_id == "group-2-toggle" and n3:
    #     return False, False, not is_open3
    return [False for i in range(len(df))]


# Run the app
if __name__ == '__main__':
    app.run_server()
