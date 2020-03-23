import base64
import io

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import flask
import pandas as pd
from dash.dependencies import Input, Output, State

# @author Dylan Dasgupta

external_stylesheets = ['https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css']

external_scripts = ['https://code.jquery.com/jquery-3.2.1.slim.min.js',
                    'https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js',
                    'https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js']

# Server definition

server = flask.Flask(__name__)
app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets,
                external_scripts=external_scripts,
                server=server)

default_study_data = "data/bfw-v0.1.5-datatable.csv"

# LAYOUT COMPONENTS
# ==========

# Your components go here.

header = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Page 1", href="#")),
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
    brand="BFW Dashboard",
    brand_href="#",
    color="primary",
    dark=True
)

data_input = html.Div(
    className="row card",
    children=[
        # User Controls
        html.Div(
            className="four columns card",
            style={"border": "2px black solid"},
            children=[
                # data_select,
                html.Div(
                    children=[
                        html.Div(
                            className="padding-top-bot",
                            children=[
                                html.H6("Select Data (This will go under the data tab)"),
                                dcc.Upload(
                                    id="upload-data",
                                    className="upload",
                                    children=html.Div(
                                        children=[
                                            html.P("Drag and Drop or "),
                                            html.A("Select Files"),
                                        ]
                                    ),
                                    accept=".csv",
                                ),
                            ],
                        ),
                    ],
                )
            ],
        ),
        dcc.Store(id="error", storage_type="memory"),
    ],
)

tabs = html.Div([
    dcc.Tabs(id="main-tabs", value='tab-overview', children=[
        dcc.Tab(label='Overview', value='tab-overview'),
        dcc.Tab(label='Data', value='tab-data-input'),
    ]),
    html.Div(id='tabs-content', style={"border": "2px black solid"})
])

summary_pivot = html.Div(
    className="row",
    children=[
        html.Div(
            className="row app-body",
            style={"border": "2px black solid",
                   "height": "200px",
                   "width": "800px",
                   "margin-top": "5px",
                   "margin-bottom": "5px",
                   },
            children=[
                html.Div(html.H5("Summary Pivot Table", style={"text-align": "center"})),
            ]
        )])

confusion_matrix = html.Div(
    className="row",
    children=[
        html.Div(
            className="row app-body",
            style={"border": "2px black solid",
                   "height": "200px",
                   "width": "800px",
                   "margin-top": "5px",
                   "margin-bottom": "5px",
                   },
            children=[
                html.Div(html.H5("Confusion Matrix", style={"text-align": "center"})),
            ]
        )])

violin_plots = html.Div(
    className="row",
    children=[
        # Column
        # New Column
        html.Div(
            className="row sc-group",
            children=html.Div([
                html.Div(html.H5('Violin Plot 1', style={"text-align": "center"}),
                         style={"border": "2px black solid",
                                "height": "200px",
                                "width": "800px",
                                "margin-top": "5px",
                                "margin-bottom": "5px"
                                }),
                html.Div(html.H5('Violin Plot 2', style={"text-align": "center"}),
                         style={"border": "2px black solid",
                                "height": "200px",
                                "width": "800px",
                                "margin-top": "5px",
                                "margin-bottom": "5px"
                                }),
            ])
        )
    ]
)

sdm_curves = html.Div(
    className="row",
    children=[
        # Column
        # New Column
        html.Div(
            className="row sc-group",
            children=[
                html.Div(html.H5('SDM Curve 1', style={"text-align": "center"}),
                         style={"border": "2px black solid",
                                "height": "200px",
                                "width": "400px",
                                "margin-top": "5px",
                                "margin-bottom": "5px"
                                }),
                html.Div(html.H5('SDM Curve 2', style={"text-align": "center"}),
                         style={"border": "2px black solid",
                                "height": "200px",
                                "width": "400px",
                                "margin": "5px",
                                "margin-bottom": "5px"
                                }),
            ]
        )
    ]
)

det_curves = html.Div(
    className="row",
    children=[
        html.Div(
            className="row app-body",
            style={"border": "2px black solid",
                   "height": "200px",
                   "width": "800px",
                   "margin-top": "5px",
                   "margin-bottom": "5px",
                   },
            children=[
                html.Div(html.H5("DET Curve 1", style={"text-align": "center"})),
            ]
        ),
        # Column
        # New Column
        html.Div(
            className="row sc-group",
            children=[
                html.Div(html.H5('DET Curve 2', style={"text-align": "center"}),
                         style={"border": "2px black solid",
                                "height": "200px",
                                "width": "400px",
                                "margin-top": "5px",
                                "margin-bottom": "5px"
                                }),
                html.Div(html.H5('DET Curve 3', style={"text-align": "center"}),
                         style={"border": "2px black solid",
                                "height": "200px",
                                "width": "400px",
                                "margin": "5px",
                                "margin-bottom": "5px"
                                }),
            ]
        )
    ]
)

dataframe_print = html.Div(
    className="row app-body",
    style={"border": "2px black solid"},
    children=[
        html.Div(
            className="row chart",
            id='figure'
        )
    ]
)

# INTERACTION
# ===========

# Your interaction goes here.


# APP LAYOUT
# ==========
# https://github.com/plotly/dash-sample-apps/blob/master/apps/dash-study-browser/app.py


app.layout = html.Div([
    html.Div(children=[
        html.Div(header),
        tabs,
        data_input,
        # Dataframe
        html.Details([
            html.Summary('Dataframe',
                         style={
                             "text-align": "center"
                         }),
            html.Div(dataframe_print)
        ]),
        # Summary Pivot
        html.Details([
            html.Summary('Summary Pivot Table',
                         style={
                             "text-align": "center"
                         }),
            html.Div(summary_pivot)
        ]),
        # Confusion Matrix
        html.Details([
            html.Summary('Confusion Matrix',
                         style={
                             "text-align": "center"
                         }),
            html.Div(confusion_matrix)
        ]),
        # Violin Plots
        html.Details([
            html.Summary('Violin Plots',
                         style={
                             "text-align": "center"
                         }),
            html.Div(violin_plots)
        ]),
        # SDM Curves
        html.Details([
            html.Summary('SDM Curves',
                         style={
                             "text-align": "center"
                         }),
            html.Div(sdm_curves)
        ]),
        # DET Curves
        html.Details([
            html.Summary('DET Curves',
                         style={
                             "text-align": "center"
                         }),
            html.Div(det_curves)
        ])],
        style={"margin": "5px 5px 5px 5px"}
    )
])


# CALLBACKS
# Callback to generate study data
@app.callback(
    Output("figure", "children"),
    [Input('upload-data', 'contents')],
    [State("error", "data")],
)
def update_output(contents, error):
    default_study_data = "data/bfw-v0.1.5-datatable.csv"

    if error or not contents:
        study_data = pd.read_csv(default_study_data)
    else:
        content_type, content_string = contents.split(",")
        decoded = base64.b64decode(content_string)
        study_data = pd.read_csv(io.StringIO(decoded.decode("utf-8")))

    df = study_data.head()

    data_table = dash_table.DataTable(
        id='table',
        columns=[{"name": i, "id": i} for i in df.columns],
        data=df.to_dict('records'),
        style_table={
            'overflowX': 'scroll',
            'overflowY': 'scroll',
            'margin-left': 'auto',
            'margin-right': 'auto',
            'padding': '4px'
        },
    )
    return data_table


@app.callback(Output('tabs-content', 'children'),
              [Input('main-tabs', 'value')])
def render_content(tab):
    if tab == 'tab-data-input':
        return html.Div([
            html.H3('Data Input'),
            html.P('Upload data context error when you put it in a tab....')
        ])
    elif tab == 'tab-overview':
        return html.Div([
            html.H3('Overview'),
            html.P('Brief description of tool....')
        ])


if __name__ == '__main__':
    app.run_server(debug=True)
