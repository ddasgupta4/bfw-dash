import datetime

import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

# import tooltips

now = str(datetime.datetime.now())

header = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Dashboard", href="#")),
        dbc.DropdownMenu(
            children=[
                dbc.DropdownMenuItem("Additional Resources", header=True),
                dbc.DropdownMenuItem("README", href="#"),
                dbc.DropdownMenuItem("Report", href="#"),
                dbc.DropdownMenuItem("GitHub", href="https://github.com/ddasgupta4/bfw-dash")
            ],
            nav=True,
            in_navbar=True,
            label="More",
        ),
    ],
    brand="'Fairness' Evaluation for Facial Recognition Technology",
    brand_href="#",
    color="primary",
    dark=True,
    brand_style={"text-align": "left"}
)

# LEFT PANEL

upload_data = html.Div([dcc.Upload(
    id='upload-data',
    children=html.Div([
        'Drag and Drop or ',
        html.A('Select File'),
        html.Div(id='output-data-upload', style={"fontSize": "10px"})
    ]),
    style={
        'borderWidth': '1px',
        'borderStyle': 'solid',
        'borderRadius': '5px',
        'textAlign': 'center',
        'margin': 'auto',
        'margin-top': '20px',
        'padding': '5px',
        'width': '90%',
        'height': '50px'
    },
    multiple=False
),
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
    multi=True,
    style={"margin-bottom": "5px",
           "height": "20%"})

gender_filter = dcc.Dropdown(
    id="gender-filter",
    options=[
        {'label': 'Male', 'value': 'M'},
        {'label': 'Female', 'value': 'F'}
    ],
    value=['M', 'F'],
    multi=True,
    style={"margin-bottom": "5px",
           "height": "20%"})

score_filter = dcc.Dropdown(
    id="score-filter",
    options=[
        {'label': 'senet50', 'value': 'senet50'},
        {'label': 'resnet50', 'value': 'resnet50'},
        {'label': 'vgg16', 'value': 'vgg16'}
    ],
    value='senet50',
    multi=False,
    style={"margin-bottom": "5px",
           "height": "20%"})

ethnicity_label = html.Div("Ethnicity", style={"text-align": "left"})

gender_label = html.Div("Gender", style={"text-align": "left"})

score_label = html.Div("Scoring Metric", style={"text-align": "left"})

overview = html.Div(children=[html.Img(src='assets/bfw-logo.png',
                                       style={
                                           "height": "35%"
                                       }),
                              html.Div(children=[
                                  html.Div(upload_data)
                              ]),
                              html.Div(children=[
                                  ethnicity_label,
                                  ethnicity_filter,
                                  gender_label,
                                  gender_filter,
                                  score_label,
                                  score_filter
                              ],
                                  style={
                                      "height": "45%",
                                      "width": "90%",
                                      "background-color": "#F3F4F9",
                                      "margin": "auto",
                                      "margin-top": "5px",
                                      "margin-bottom": "5px",
                                      "padding": "10px",
                                  }),
                              ],
                    style={"height": "500px",
                           "backgroundColor": "white",
                           "padding": "5px",
                           "border": "1px solid #f8f9fa",
                           "text-align": "center",
                           "margin-top": "1px"})

# TABS

data_tabs = html.Div([
    dcc.Tabs(id="data-tabs", value='tab-frame', children=[
        dcc.Tab(label='Data Table', value='tab-frame', id='tab-frame'),
        dcc.Tab(label='Data Summary', value='tab-summary', id='tab-summary'),
    ], style={"margin-top": "5px"}),
    dbc.Tooltip(
        "Preview of uploaded dataset",
        target="tab-frame",
        placement="top",
        delay={"show": "500"}
    ),
    dbc.Tooltip(
        "Summary statistics of uploaded dataset",
        target="tab-summary",
        placement="top",
        delay={"show": "500"}
    ),
    html.Div(id='tabs-content-data')])

error_tabs = html.Div([
    dcc.Tabs(id="error-tabs", value='tab-error', children=[
        dcc.Tab(label='Detection Error Tradeoff (DET) Curves', value='tab-det', id='tab-det'),
        dcc.Tab(label='ROC Curves', value='tab-roc', id='tab-roc'),
        dcc.Tab(label='Confusion Matrix', value='tab-matrix', id='tab-matrix'),
    ]),
    dbc.Tooltip(
        "Explain what confusion matrix is",
        target="tab-matrix",
        placement="top",
        delay={"show": "500"}
    ),
    dbc.Tooltip(
        "Explain what DET Curve is",
        target="tab-det",
        placement="top",
        delay={"show": "500"}
    ),
    dbc.Tooltip(
        "Explain what ROC Curve is",
        target="tab-roc",
        placement="top",
        delay={"show": "500"}
    ),
    html.Div(id='tabs-content-error',
             style={"width": "100%"})
])

dist_tabs = html.Div([
    dcc.Tabs(id="dist-tabs", value='tab-graphs', children=[
        dcc.Tab(label='Violin Plots', value='tab-violin', id='tab-violin'),
        dcc.Tab(label='Box Plots', value='tab-box', id='tab-box'),
        dcc.Tab(label='SDM Curves', value='tab-sdm', id='tab-sdm'),
    ]),
    dbc.Tooltip(
        "Explain what violin plot is",
        target="tab-violin",
        placement="top",
        delay={"show": "500"}
    ),
    dbc.Tooltip(
        "Explain what box plot is",
        target="tab-box",
        placement="top",
        delay={"show": "500"}
    ),
    dbc.Tooltip(
        "Explain what SDM curve is",
        target="tab-sdm",
        placement="top",
        delay={"show": "500"}
    ),
    html.Div(id='tabs-content-dist')
])

# SHOW/HIDE ELEMENTS

hidden_dist = html.Div(
    children=[
        html.Details(
            [html.Summary("Score Distribution Plots"),
             dist_tabs]
        )
    ], style={"width": "100%"})

hidden_error = html.Div(
    children=[
        html.Details(
            [html.Summary("Error Evaluation Plots"),
             error_tabs]
        ),
    ],
    style={"width": "100%"})
