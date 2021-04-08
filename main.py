# Import packages for data cleaning
import numpy as np
import pandas as pd

# Uploading Files
import base64
import io
import dash

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

stud = Student()
stud_df = df.copy().iloc[0:0]  # erase all rows but keep cols: https://bit.ly/2PCF5Xi
# print(stud_df, df)
course_classes_list = [Course(c['id'], c['name'], c['credit'], c['description'], c['prereq']) for c in df_dict]

# Create the app and add extra styles
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    # external_stylesheets=[dbc.themes.LITERA],
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


def makeCollapse(i, course, style_val=None):
    # course_id = course.id.split(' ')

    # collapseList.append(f"{course_id[0]}-{course_id[1]}-collapse-toggle")
    collapseList.getList().append(f"{i}")
    return dbc.Card(
        [
            # COURSE CARD TITLE
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
                    html.H6(f"{course.credit} Credits", className="card-subtitle", style={'margin-bottom': '10px'}),
                    html.P(f"{course.desc}", className="card-text"),
                    dbc.CardFooter(f"{str(course.prereq)}"),
                ]),
                id=f"collapse-{i}",
            ),
        ],
        style=style_val if style_val is not None else style_val,
        id=f"collapse-card-{i}",
    )


'''
Column 1 - Input
'''
input_col = dbc.Col(
    [
        # FIND COURSES
        html.H4("Find Courses", style={'margin-bottom': '10px'}),
        dbc.Row(
            dbc.Input(
                id='course-search-input',
                placeholder='Type a course id, name, or description',
                type='search',
            )
            , style={'margin': '10px 0px'}),

        # COURSE ACCORDIONS
        dbc.Row(dbc.Col(
            [
                # makeCollapse(c + 1, course_class_list[c]) for c in range(len(course_class_list))
                makeCollapse(i, course_classes_list[i]) for i in range(len(df))
                # makeCollapse(1, course_class_list[3]),
                # makeCollapse(2, course_class_list[2]),
                # makeCollapse(3, course_class_list[1]),
                # makeCollapse(i) for i in course_class_list
            ],
            id='courses-results-container',
        ),

            style={'overflow': 'scroll', 'maxHeight': '50vh', 'overflowX': 'hidden'},  # style container
        ),

        # SELECT AND INPUT
        dbc.Card(
            dbc.CardBody(
                [
                    html.H4("Mark selected course(s) as:", style={'margin-bottom': '10px'}),

                    # MULTI SELECTED COURSES
                    dbc.Row(dbc.Col([
                        dcc.Dropdown(
                            id='courses-input',
                            options=[
                                {'label': c['id'], 'value': c['id'.replace(' ', '-')]} for c in df_dict
                            ],
                            placeholder='Select Courses...',
                            value=[],
                            multi=True,
                        )
                    ]),
                        style={'margin-bottom': '10px'}),

                    # COURSE STATUS RADIO BTNS
                    dbc.Row(dbc.Col([
                        dbc.RadioItems(
                            id='status-radio',
                            options=[
                                {'label': 'Completed', 'value': 'done'},
                                {'label': 'Work In Progress', 'value': 'wip'},
                                {'label': 'Planning to Take', 'value': 'planned'},
                                {'label': 'Remove from Table', 'value': 'remove'},
                            ],
                            value='done',
                            labelStyle={'display': 'block'}  # make new line option
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    dbc.Button("Add to Planner", color="primary", id='add-to-planner-btn', n_clicks=0)),
                                dbc.Col(
                                    dcc.Upload(
                                        id='upload-table',
                                        children=[
                                            dbc.Button("Import CSV", id='import-btn', color='secondary'),
                                        ]
                                    ), width='auto'
                                ),
                            ],
                            style={'margin-top': '10px'},
                            justify='between',
                        ),

                    ])),
                ]
            ),
            style={'margin': '5px 0'}
        ),

        # CHANGE VIEW BTNS
        dbc.Container([
            html.B("Change view:"),
            dbc.Row(
                [
                    dbc.Col(dbc.Button("Default", color="primary", id='view-btn-default', n_clicks=0),
                            width='auto', ),
                    dbc.Col(dbc.Button("Sunburst", color="secondary", id='view-btn-sun', n_clicks=0, disabled=True),
                            width='auto', ),
                    html.Div(id='container-button-timestamp')
                ],
                justify='start',
                style={'margin-top': '10px'},
            ),

        ]),

        # dbc.Row(dbc.Col([])),
    ],
    width=3,
)

'''
Column 2 - Data Tables
'''
data_col = dbc.Col(
    [
        html.H4('My Progress'),
        dbc.Row(dbc.Col([
            # html.H2("Table"),
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
                    {'id': 'status', 'name': 'Status'},
                ],
                # DATA TABLE SETTINGS
                data=stud.getdf().to_dict('records'),  # data to use
                filter_action='native',  # for filtering
                row_deletable=True,

                # table styling
                style_table={
                    'maxHeight': '100vh',
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

                export_format='csv',
                export_headers='display',
            ),
        ])),

        # dbc.Row([
        #     html.H2("Sunburst"),
        # ])
    ], width=6
)

'''
Column 3 - Checklist
'''
checklist_col = dbc.Col([
    html.H4('Checklist'),
    html.H5("Computer Science Major", style={'margin-bottom': '10px'}),

    dbc.FormGroup(
        id='checklist',
        children=
        [
            # Declaring Computer Science
            dbc.Row(dbc.Col([
                html.H6('Declaring Computer Science', style={'margin': '10px 0'}),
                dbc.Checklist(
                    options=[
                        {'label': 'CMPT 101', 'value': 1},
                        {'label': 'MATH 114', 'value': 2},
                        {'label': 'MATH 120 OR MATH 125', 'value': 3},
                        {'label': 'STAT 151', 'value': 4},
                    ],
                    value=[],
                    id='checklist-input-0',
                )
            ])),

            # Computer Science Major
            dbc.Row(dbc.Col([
                html.H6('Computer Science Major', style={'margin': '10px 0'}),
                dbc.Checklist(
                    id='checklist-input-1',
                    options=[
                        {'label': 'CMPT 103', 'value': 5},
                        {'label': 'CMPT 200', 'value': 6},
                        {'label': 'CMPT 201', 'value': 7},
                        {'label': 'CMPT 395', 'value': 8},
                        {'label': 'CMPT 496', 'value': 9},
                    ],
                    value=[],
                )
            ])),

            # Gaming Stream
            dbc.Row(dbc.Col([
                html.H6('Gaming Stream', style={'margin': '10px 0'}),
                dbc.Checklist(
                    id='checklist-input-2',
                    options=[
                        {'label': 'CMPT 230', 'value': '10'},
                        {'label': 'CMPT 291', 'value': '11'},
                        {'label': 'CRWR 295', 'value': '12'},
                        {'label': 'CMPT 330', 'value': '13'},
                        {'label': 'CMPT 370', 'value': '14'},
                        {'label': 'CMPT 250 OR CMPT 280 OR CMPT 355', 'value': '15'},
                    ],
                    value=[10],
                )
            ])),

            # CREDIT CHECKLIST
            dbc.Row(dbc.Col([
                html.H6('Credits', style={'margin': '10px 0'}),
                dbc.Checklist(
                    id='checklist-input-3',
                    options=[
                        {'label': '12 Credits in CMPT 300-level or CMPT 400-level', 'value': 15},
                        {'label': '72 Credits in Science Courses', 'value': 16},
                        {'label': 'Junior (100 Level) Courses < 48 Credits OR MATH 125', 'value': 17},
                        {'label': 'Transfer Credit < 60 Credits', 'value': 18},
                        {'label': '60 Credits max in one course category', 'value': 19},
                        {'label': '120 Credits in Total', 'value': 20},
                    ],
                    value=[1],
                )
            ])),
        ])],
    width=3,
)

'''
MAIN: Add content
'''
app.layout = dbc.Container(
    style={'backgroundColor': '#00000', 'overflowX': 'hidden', 'margin-top': '10px'},
    children=
    [
        dbc.Row(
            [
                # Column 1 - Input
                input_col,

                # Column 2 - Data
                data_col,

                # Column 3 - Checklist
                checklist_col,

            ],
        ),

    ],
    fluid=True
)


def parse_contents(contents, filename):
    # Uploading file to data table: https://bit.ly/3mq82SK

    content_type, content_string = contents.replace('"', '').split(',')
    decoded = base64.b64decode(content_string)

    if 'csv' in filename:
        # Assume that the user uploaded a CSV file
        df = pd.read_csv(
            io.StringIO(decoded.decode('utf-8')))
        return df

    elif 'xls' in filename:
        # Assume that the user uploaded an excel file
        return pd.read_excel(io.BytesIO(decoded))


'''
INTRO MODAL
'''
intro_modal = html.Div(
    [
        dbc.Modal(
            [
                dbc.ModalHeader("Computer"),
                dbc.ModalBody([

                ]),
                dbc.ModalFooter(
                    dbc.Button("Close", id="close", className="ml-auto")
                ),
            ],
            size='xl',
        )
    ]
)


# FILTER COURSES - SEARCH
@app.callback(
    [Output(f'collapse-card-{i}', 'style') for i in range(len(df))],
    Input('course-search-input', 'value'),
    [State(f"collapse-{i}", "is_open") for i in range(len(df))],  # course toggles

)
def update_course_results(search_value, *args):
    collapse_ids = []  # store num id of those to show

    # If search is none, show all
    if search_value is None:
        collapse_ids = [i for i in range(len(df))]

    i = 0
    if search_value is not None:
        search_value = search_value.upper()

        # Find
        for course in course_classes_list:  # For each Course class
            if search_value in course.id \
                    or search_value in course.desc.upper() \
                    or search_value in course.name.upper():
                print(search_value)
                collapse_ids.append(i)
            i += 1

    return [{'display': 'block' if toggle in collapse_ids else 'none'} for toggle in range(len(df))]


# COURSE ACCORDIONS
@app.callback(
    # OUTPUTS - should come first
    [Output(f"collapse-{i}", "is_open") for i in collapseList.getList()],  # course toggles

    # INPUTS - comes after outputs
    [Input(f"group-{i}-toggle", "n_clicks") for i in range(len(df))],  # course toggles

    [State(f"collapse-{i}", "is_open") for i in range(len(df))],  # course toggles
)
def toggle_accordion(*args):
    # advanced callbacks: https://bit.ly/3wbTYAB
    ctx = dash.callback_context  # seek the component where user clicks

    if not ctx.triggered:
        return [False for i in range(len(df))]
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]  # group-X-toggle

    print(button_id)

    for i in range(len(df)):
        if button_id == f"group-{i}-toggle":
            bools.toggle(i)
            return bools.list
    return [False for i in range(len(df))]


# COURSE SELECTIONS DROPDOWN MULTISELECT
@app.callback(
    # OUTPUT
    Output("my-table", "data"),

    # INPUT
    Input('add-to-planner-btn', 'n_clicks'),

    # [Input(f'checklist-input-{i}', 'value') for i in range(4)],

    # STATE
    # [State(f'checklist-input-{i}', 'options') for i in range(4)],
    Input('upload-table', 'contents'),
    State('upload-table', 'filename'),

    State('courses-input', 'value'),
    State('status-radio', 'value'),
)
def update_my_table(n_clicks0,
                    contents, filename,
                    selected_courses, radio_select
                    ):
    # print("CONTENTS", parse_contents(contents, filename))
    if contents is None and selected_courses is None:
        return None

    # save into Student dataframe
    elif contents is not None:
        stud.set(parse_contents(contents, filename))
        return stud.getdf_dict()

    # MULTISELECT DROPDOWN INPUT
    if selected_courses is not None:
        if radio_select == 'remove':
            [stud.remove(c) for c in selected_courses]

        else:
            [stud.add(c, radio_select.upper()) for c in selected_courses]

    return stud.getdf_dict()


# UPDATE CHECKLIST
@app.callback(
    # [Output(f'checklist-input-{i}', 'value') for i in range(4)],
    # Output('container-button-timestamp', 'children'),
    [Output(f'checklist-input-{i}', 'value') for i in range(4)],

    # Output(f'checklist-input-{1}', 'value'),
    # Output(f'checklist-input-{1}', 'options'),

    Input('my-table', 'data'),
    [Input(f'checklist-input-{i}', 'options') for i in range(4)],

)
def update_checklist(
        data_table,
        check_opt0, check_opt1, check_opt2, check_opt3,
):
    # get current ctx triggered
    # if button clicked value id is == to that id, change value of that id triggere
    checked_values = []
    labels = {check['label']: check['value'] for check in check_opt0 + check_opt1 + check_opt2 + check_opt3}

    for c in data_table:
        value = []
        # for courses in data table, get the checklist value for it
        # print(c['id'], c['status'])
        # print(c)
        # [value.append(labels[label]) for label in labels.keys() if label == c['id'] and c['status'] == ""]
        # checked_values += value

    return [checked_values for i in range(4)]


# CHANGE VIEW
# @app.callback(
#     Output('container-button-timestamp', 'children'),
#
#     Input('view-btn-default', 'n_clicks'),
#     Input('view-btn-sun', 'n_clicks'),
# )
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

# Run the app


if __name__ == '__main__':
    app.run_server()
