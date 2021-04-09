# Import packages for data cleaning
import numpy as np
import pandas as pd

# Todo build onboarding with modal
# Todo possibly add, col, courses you can take
# todo fix update_checklist, when stream is changed, checks my-table to make the changes
# todo add checklist column
# todo add all courses to table

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
# download a csv
from dash_extensions import Download
from dash_extensions.snippets import send_data_frame

# Bootstrap for Dash: https://bit.ly/3tKt9S3
import dash_bootstrap_components as dbc

from Course import *
from Student import *

# -------------------------------------------

# # Get data
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

            style={'overflow': 'scroll', 'maxHeight': '45vh', 'overflowX': 'hidden'},  # style container
        ),

        # SELECT AND INPUT
        dbc.Row(
            dbc.Col(dbc.Card(
                dbc.CardBody(
                    [
                        html.H4("Mark selected course(s) as:", style={'margin-bottom': '10px'}),

                        # MULTI SELECTED COURSES
                        dbc.Row(dbc.Col([
                            dcc.Dropdown(
                                id='courses-input',
                                options=[
                                            {'label': c['id'], 'value': c['id'.replace(' ', '-')]} for c in df_dict
                                        ] + [{'label': "All CMPT Courses", 'value': 'all-cmpt'}],
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
                                        dbc.Button("Update My Table", color="primary", id='add-to-planner-btn',
                                                   n_clicks=0)),
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
                style={'margin': '5px 0', }
            )),
            style={'maxHeight': '35vh', 'overflowY': 'scroll'}
        ),

        # CHANGE VIEW BTNS
        dbc.Container([
            html.B("Change view:"),
            dbc.Row(
                [
                    dbc.Col(dbc.Button("Default", color="primary", id='view-btn-default', n_clicks=0),
                            width='auto', style={'margin-right': '10px'}),
                    dbc.Col(dbc.Button("Sunburst", color="secondary", id='view-btn-sun', n_clicks=0, disabled=True),
                            width='auto', ),
                    html.Div(id='container-button-timestamp')
                ],
                justify='start',
                no_gutters=True,
                style={'margin': '5px 0'},

            ),

        ]),

        # dbc.Row(dbc.Col([])),
    ],
    width=3,
)

import_modal_content = '''
## How to Import
The supported files you can export is `.csv` and `.xls.`

You ***must*** follow this column format (this means column name is ***case sensitive*** )

The only required cell to input is `Course ID` but it’s recommended to add a status!

Columns `Course Name`, `Credits`, and `Prerequisites` are automatically filled based on the given `Course ID`


| Course ID | Course Name | Credits | Prerequisites | Status  |
| --------- | ----------- | ------- | ------------- | ------- |
| CMPT 103  | --          | --      | --            | PLANNED |

Below is the raw `.csv` file of the example table above.

```
Course ID,Course Name,Credits,Prerequisites,Status
CMPT 101,,,PLANNED,
```


'''

import_modal = dbc.Modal(
    [
        dbc.ModalHeader("How to Import"),
        dbc.ModalBody([
            dcc.Markdown(import_modal_content),
            dbc.Button(
                "Download CSV template", color='info', id='download-template-btn',
                href="https://bit.ly/3uuwDIK", target="_blank", className="mt-3"
            ),
        ]),
        dbc.ModalFooter(
            dbc.Button("Close", id="close-import", className="ml-auto", color='dark'),
            style={'margin-top': '10px'}
        ),

        dbc.Tooltip(
            "You will be link to the raw csv data. "
            "Right click on the page and Save As",
            target="download-template-btn",
        ),
    ]
    ,
    id="import-modal",
    # is_open=True,
    size="lg",
)
intro_modal_content = '''
### 🎉 Welcome to the MacEwan Computer Sci. Major Planner

##### Here's some info on how to use the application
There are **3 columns**: *Find Courses*, *My Table*, and *Checklist*

1. **Find Courses**

   Here you can search for a course’s full description quickly.
   You can search by a course id, course name and, even by a course’s description. As you search, results will update live.

   ![](https://i.imgur.com/rtAsbTD.png) 

   You can select multiple courses and set a status for them. You can also remove them from the table.
   You can choose to import a `csv` or `xls` file to put data into your table. ***Check How to Import for more details*** 

   ![](https://i.imgur.com/h6koO6e.png?1)

   In the future, you will be able to switch to a sunburst view, showing the relation of courses in your table more visually. For now we’ll have to stick with the table 😅.

2. **My Table**

   This table represents your Computer Science Major degree plan.
   Every time you make changes from the ***Mark selected courses(s) as:*** section, it will be added to you table.
   You can export your table at any point into a `.csv` fille.

   Within the table, you can filter the data. You can filter by string or number, depending on the column.

   ![](https://i.imgur.com/Q9g4VFR.png) 

   The official docs on filtering tables can be found [here](https://bit.ly/31tUrjG).

   **Text & String Filtering**

   - `United`
   - `= United`
   - `United States`
   - `"United States"`
   - `= United States`
   - `= "United States"`
   - `> United`
   - `>= United`
   - `< United`	
   - `<= United`

   **Numeric Filtering**

   - `43.828`
   - `= 43.828`
   - `> 43.828`
   - `>= 43.828`
   - `< 43.828`
   - `<= 43.828`

   Below the table, are where you can go back to this window if you ever get lost. You can also find helpful information here like ***How to Import***.

3. **Checklist**

   Finally, the checklist. The dropdown allows you to change your checklist requirements based on the stream you choose.

   The default stream is the *Gaming Stream*.

   ![](https://i.imgur.com/rXgKu7e.png) 

   In the future, any updates to your table will be able to reflect on you checklist.


'''

'''
INTRO MODAL
'''
intro_modal = dbc.Modal(
    [
        dbc.ModalHeader("Getting Started"),
        dbc.ModalBody([
            dcc.Markdown(intro_modal_content, style={'midth': '20px'}),

        ]),
        dbc.ModalFooter(
            dbc.Button("Close", id="close-intro", className="ml-auto", color='dark')
        ),
    ],
    id='intro-modal',
    size='xl',
    is_open=True,
    scrollable=True,
)

'''
Column 2 - Data Tables
'''
data_col = dbc.Col(
    [
        html.H4('My Table'),
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
                    'maxHeight': '80vh',
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
        ]),
            className='mb-3'
        ),

        # dbc.Row([
        #     html.H2("Sunburst"),
        # ])

        # HOW TO IMPORT MODAL BTN
        dbc.Button("Getting Started", id="open-intro", color='info', className='mr-2', ),
        dbc.Button("How to Import", id="open-import", outline=True, color='info'),

        # MODALS
        intro_modal,
        import_modal,

    ], width=6
)

'''
Column 3 - Checklist
'''
checklist_col = dbc.Col([
    html.H4('Checklist'),
    html.H5("Computer Science Major", style={'margin-bottom': '10px'}),

    dcc.Dropdown(
        id='major-stream-input',
        options=[
            {'label': 'General Stream', 'value': 'general-stream'},
            {'label': 'Databases and Interactive', 'value': 'database-stream'},
            {'label': 'Systems and Information Security', 'value': 'sys-info-stream'},
            {'label': 'Gaming ', 'value': 'gaming-stream'},
        ],
        placeholder="Choose a Stream",
        searchable=False,
    ),

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
            dbc.Row(
                id='major-stream-checklist',
                children=dbc.Col(
                    [
                        html.H6('Gaming Stream', style={'margin': '10px 0'}),
                        dbc.Checklist(
                            id='checklist-input-2',
                            options=[
                                {'label': 'CMPT 230', 'value': 10},
                                {'label': 'CMPT 291', 'value': 11},
                                {'label': 'CRWR 295', 'value': 12},
                                {'label': 'CMPT 330', 'value': 13},
                                {'label': 'CMPT 370', 'value': 14},
                                {'label': 'CMPT 250 OR CMPT 280 OR CMPT 355', 'value': 15},
                                # 16, 17for sys-info-stream
                            ],
                            value=[],
                        )
                    ])),

            # CREDIT CHECKLIST
            dbc.Row(dbc.Col([
                html.H6('Credits', style={'margin': '10px 0'}),
                dbc.Checklist(
                    options=[
                        {'label': '12 Credits in CMPT 300-level or CMPT 400-level', 'value': 18},
                        {'label': '72 Credits in Science Courses', 'value': 19},
                        {'label': 'Junior (100 Level) Courses < 48 Credits OR MATH 125', 'value': 20},
                        {'label': 'Transfer Credit < 60 Credits', 'value': 21},
                        {'label': '60 Credits max in one course category', 'value': 22},
                        {'label': '120 Credits in Total', 'value': 23},
                    ],
                    id='checklist-input-3',
                    value=[],

                )
            ], ), ),
        ],
        style={'maxHeight': '80vh', 'overflowY': 'auto', 'padding': '0 15px'},
    )],
    width=3,

)

'''
MAIN: APP LAYOUT
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


@app.callback(
    Output("import-modal", "is_open"),
    [Input("open-import", "n_clicks"), Input("close-import", "n_clicks")],
    [State("import-modal", "is_open")],
)
def toggle_import_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


@app.callback(
    Output("intro-modal", "is_open"),

    [Input("open-intro", "n_clicks"), Input("close-intro", "n_clicks")],

    [State("intro-modal", "is_open")],
)
def toggle_intro_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open


# FOR IMPORTING
def parse_contents(contents, filename):
    # Uploading file to data table: https://bit.ly/3mq82SK
    # print(contents, filename)

    content_type, content_string = contents.replace('"', '').split(',')
    decoded = base64.b64decode(content_string)

    if 'csv' in filename:
        # Assume that the user uploaded a CSV file
        return pd.read_csv(
            io.StringIO(decoded.decode('utf-8')))

    elif 'xls' in filename:
        # Assume that the user uploaded an excel file
        return pd.read_excel(io.BytesIO(decoded))


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
                # print(search_value)
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
                    file_contents, filename,
                    selected_courses, radio_select
                    ):
    ctx = dash.callback_context  # seek the component where user clicks
    if not ctx.triggered:
        return stud.getdf_dict()
    else:
        button_id = ctx.triggered[0]["prop_id"].split(".")[0]
        print(button_id)

    # CHECK BUTTON ID
    if button_id != "add-to-planner-btn":
        # if file & no selected courses
        if file_contents is None and selected_courses is None:
            return None

        # save into Student dataframe
        elif file_contents is not None:
            stud.set(parse_contents(file_contents, filename))
            return stud.getdf_dict()

    # MULTISELECT DROPDOWN INPUT
    if selected_courses is not None:
        if radio_select == 'remove':
            [stud.remove(c) for c in selected_courses]

        else:
            if "all-cmpt" in selected_courses:
                [stud.add(c.id, radio_select.upper()) for c in course_classes_list]

            else:
                [stud.add(c, radio_select.upper()) for c in selected_courses]

    return stud.getdf_dict()


# CHANGING STREAM CHECKLIST
@app.callback(
    Output('major-stream-checklist', 'children'),
    Input('major-stream-input', 'value'),
)
def update_stream_checklist(stream, ):
    general = [
        {'label': "(6 Credits) CMPT 204 OR CMPT 229 OR CMPT 250 OR CMPT 280 OR CMPT 291", 'value': 10},
        {
            'label': "(6 Credits) CMPT 305 OR CMPT 306 OR CMPT 315 OR CMPT 330 OR "
                     "CMPT 355 OR CMPT 360 OR CMPT 361 OR CMPT 370 OR CMPT 380 OR CMPT 391",
            'value': 11},
        {'label': "(15 to 33 Credits)", 'value': 12},

    ]

    database = [
        {'label': "CMPT 250 ", 'value': 10},
        {'label': "CMPT 270", 'value': 11},
        {'label': "CMPT 291", 'value': 12},
        {'label': "(12 Credits) CMPT 315 OR CMPT 351 OR CMPT 391 OR CMPT 450 OR CMPT 491", 'value': 13},
        {'label': "(6 to 24 Credits)", 'value': 14},
    ]

    system_info = [
        {'label': "CMPT 229 ", 'value': 10},
        {'label': "CMPT 280", 'value': 11},
        {'label': "CMPT 360", 'value': 12},
        {'label': "CMPT 361", 'value': 13},
        {'label': "CMPT 380", 'value': 14},
        {'label': "CMPT 464", 'value': 15},
        {'label': "CMPT 480", 'value': 16},
        {'label': "(6 to 24 Credits)", 'value': 17},
    ]

    gaming = [
        {'label': 'CMPT 230', 'value': 10},
        {'label': 'CMPT 291', 'value': 11},
        {'label': 'CRWR 295', 'value': 12},
        {'label': 'CMPT 330', 'value': 13},
        {'label': 'CMPT 370', 'value': 14},
        {'label': '(3 Credits) CMPT 250 OR CMPT 280 OR CMPT 355', 'value': 15},
        {'label': "9 to 27 More Credits In CMPT", 'value': 16},
    ]

    stream_to_put = []
    stream_title = "Gaming"
    # print(stream)

    if stream == "general-stream":
        stream_to_put = general
        stream_title = "General"
    elif stream == "database-stream":
        stream_to_put = database
        stream_title = "Databases and Interactive Visualization"
    elif stream == "sys-info-stream":
        stream_to_put = system_info
        stream_title = "Systems and Information Security"
    else: # default gaming stream
        stream_to_put = gaming
        stream_title = "Gaming"

    return dbc.Col([
        html.H6(f'{stream_title} Stream', style={'margin': '10px 0'}),
        dbc.Checklist(
            id='checklist-input-2',
            options=stream_to_put,  # put stream here
            value=[],
        )
    ])


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

    if len(stud) > 0:
        for c in data_table:
            value = []
            # for courses in data table, get the checklist value for it
            # print(c['id'], c['status'])
            # print(c)
            # print(stud.df_dict)
            [value.append(labels[label]) for label in labels.keys() if label == c['id'] and c['status'] == ""]
            checked_values += value

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
