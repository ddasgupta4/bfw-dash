import datetime

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

now = str(datetime.datetime.now())

upload_data = html.Div([dcc.Upload(
    id='upload-data',
    children=html.Div([
        'Drag and Drop or ',
        html.A('Select File'),
        html.Div(id='output-data-upload',
                 style={
                     "fontSize": "10px"
                 })
    ]),
    style={
        'borderWidth': '1px',
        'borderStyle': 'solid',
        'borderRadius': '5px',
        'textAlign': 'center',
        'margin': 'auto',
        'margin-top': '18px',
        'padding': '5px',
        'width': '90%',
        'height': '50px'
    },
    multiple=False
),
    # html.Div(id='output-data-upload'),
])

column_filter = dcc.Dropdown(
    id="column-filter",
    options=[
        {'label': 'Fold', 'value': 'fold'},
        {'label': 'p1', 'value': 'p1'},
        {'label': 'p2', 'value': 'p2'},
        {'label': 'Label', 'value': 'label'},
        {'label': 'id1', 'value': 'id1'},
        {'label': 'id2', 'value': 'id2'},
        {'label': 'att1', 'value': 'att1'},
        {'label': 'att2', 'value': 'att2'},
        {'label': 'vgg16', 'value': 'vgg16'},
        {'label': 'resnet50', 'value': 'resnet50'},
        {'label': 'senet50', 'value': 'senet50'},
        {'label': 'a1', 'value': 'a1'},
        {'label': 'a2', 'value': 'a2'},
        {'label': 'g1', 'value': 'g1'},
        {'label': 'g2', 'value': 'g2'},
        {'label': 'e1', 'value': 'e1'},
        {'label': 'e2', 'value': 'e2'},
        {'label': 'Score', 'value': 'score'},
        {'label': 'Subgroup', 'value': 'subgroup'},
        {'label': 'Tag', 'value': 'Tag'}
    ],
    value=['id1', 'id2', 'att1', 'att2', 'Tag', 'score', 'subgroup'],
    multi=True)

ethnicity_filter = dcc.Dropdown(
    id="ethnicity-filter",
    options=[
        {'label': 'Asian', 'value': 'A'},
        {'label': 'Black', 'value': 'B'},
        {'label': 'Indian', 'value': 'I'},
        {'label': 'White', 'value': 'W'}
    ],
    value=['A', 'B', 'I', 'W'],
    multi=True)

gender_filter = dcc.Dropdown(
    id="gender-filter",
    options=[
        {'label': 'Male', 'value': 'M'},
        {'label': 'Female', 'value': 'F'}
    ],
    value=['M', 'F'],
    multi=True)

overview = html.Div(children=[html.Img(src='assets/bfw-logo.png',
                                       style={
                                           "width": "75%"
                                       }),
                              html.Div(children=[
                                  html.Div(upload_data)
                              ],
                                  style={
                                      "height": "25%",
                                      "width": "90%",
                                      "background-color": "#F3F4F9",
                                      "margin": "auto",
                                      "margin-top": "5px",
                                      "margin-bottom": "5px",
                                      "padding": "10px",
                                  }),
                              html.Div(ethnicity_filter, style={
                                  "width": "90%",
                                  "margin": "auto",
                                  "margin-top": "5px",
                                  "margin-bottom": "5px"
                              }),
                              html.Div(gender_filter, style={
                                  "width": "90%",
                                  "margin": "auto",
                                  "margin-top": "5px",
                                  "margin-bottom": "5px"
                              })
                              ],
                    style={"height": "400px",
                           "backgroundColor": "white",
                           "padding": "5px",
                           "border": "1px solid #f8f9fa",
                           "text-align": "center",
                           "margin-top": "1px"})

header = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Dashboard", href="#")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("More pages", header=True),
                dbc.DropdownMenuItem("Documentation (Create new webpage for it)", href="#"),
                dbc.DropdownMenuItem("Report (Embed Link)", href="#"),
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    brand="'Fairness' Evaluation for Facial Recognition Technology",
    brand_href="#",
    color="primary",
    dark=True
)

data_tabs = html.Div([
    dcc.Tabs(id="data-tabs", value='tab-frame', children=[
        dcc.Tab(label='Data Table', value='tab-frame'),
        dcc.Tab(label='Data Summary', value='tab-summary'),
    ], style={"margin-top": "5px"}),
    html.Div(id='tabs-content-data')])

error_tabs = html.Div([
    dcc.Tabs(id="error-tabs", value='tab-error', children=[
        dcc.Tab(label='Confusion Matrix', value='tab-matrix'),
        dcc.Tab(label='DET Curves', value='tab-det'),
    ]),
    html.Div(id='tabs-content-error',
             style={"width": "100%"})
])

dist_tabs = html.Div([
    dcc.Tabs(id="dist-tabs", value='tab-graphs', children=[
        dcc.Tab(label='Violin Plots', value='tab-violin'),
        dcc.Tab(label='Box Plots', value='tab-box'),
        dcc.Tab(label='SDM Curves', value='tab-sdm'),
    ]),
    html.Div(id='tabs-content-dist')
])
