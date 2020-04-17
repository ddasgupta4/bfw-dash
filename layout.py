import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html

upload_data = html.Div([dcc.Upload(
    id='upload-data',
    children=html.Div([
        'Drag and Drop or ',
        html.A('Select File'),
        html.P("default: bfw-v0.1.5-datatable",
               style={
                   "fontSize": "10px"
               })
    ]),
    style={
        'borderWidth': '1px',
        'borderStyle': 'dashed',
        'borderRadius': '5px',
        'textAlign': 'center',
        'margin': 'auto',
        'margin-top': '5px',
        'padding': '5px',
        'width': '90%',
        'height': '60px'
    },
    multiple=False
),
    html.Div(id='data-table-div', style={'display': 'none'})
    , ])

overview = html.Div(children=[html.Img(src='assets/bfw-logo.png',
                                       style={
                                           "width": "75%"
                                       }),
                              html.Div(children=[
                                  html.Div(upload_data, style={"margin-top": "30px"})
                              ],
                                  style={
                                      "height": "40%",
                                      "width": "90%",
                                      "background-color": "#F3F4F9",
                                      "margin": "auto",
                                      "padding": "10px",
                                  })
                              ],
                    style={"height": "360px",
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
    dcc.Tabs(id="data-tabs", value='tab-data', children=[
        dcc.Tab(label='Data Table', value='tab-frame'),
        dcc.Tab(label='Data Summary', value='tab-summary'),
    ]),
    html.Div(id='tabs-content-data', style={"height": "300px"})
])

other_tabs = html.Div([
    dcc.Tabs(id="other-tabs", value='tab-other', children=[
        dcc.Tab(label='Confusion Matrix', value='tab-matrix'),
        dcc.Tab(label='DET Curves', value='tab-det'),
    ]),
    html.Div(id='tabs-content-other', style={"height": "300px"})
], style={"margin-top": "5px"})

plot_tabs = html.Div([
    dcc.Tabs(id="plot-tabs", value='tab-graphs', children=[
        dcc.Tab(label='Violin Plots', value='tab-violin'),
        dcc.Tab(label='Box Plots', value='tab-box'),
        dcc.Tab(label='SDM Curves', value='tab-sdm'),
    ]),
    html.Div(id='tabs-content-plots', style={"height": "300px"})
])
