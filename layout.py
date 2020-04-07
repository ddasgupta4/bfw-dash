import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import flask
from dash.dependencies import Input, Output

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
    brand="'Fairness' Evaluation for Facial Recognition Technology",
    brand_href="#",
    color="primary",
    dark=True
)

tabs = html.Div([
    dcc.Tabs(id="main-tabs", value='tab-overview', children=[
        dcc.Tab(label='Overview', value='tab-overview'),
    ]),
    html.Div(id='tabs-content')
])

data_tabs = html.Div([
    dcc.Tabs(id="data-tabs", value='tab-data', children=[
        dcc.Tab(label='Data Input', value='tab-input'),
        dcc.Tab(label='Data Table', value='tab-frame'),
        dcc.Tab(label='Data Summary', value='tab-summary'),
    ]),
    html.Div(id='tabs-content-data')
])

plot_tabs = html.Div([
    dcc.Tabs(id="plot-tabs", value='tab-graphs', children=[
        dcc.Tab(label='Violin Plots', value='tab-violin'),
        dcc.Tab(label='Box Plots', value='tab-box'),
        dcc.Tab(label='SDM Curves', value='tab-sdm'),
    ]),
    html.Div(id='tabs-content-plots')
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
                   "height": "500px",
                   "width": "500px",
                   "margin-top": "5px",
                   "margin-bottom": "5px",
                   "margin-left": "15px",
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

# INTERACTION
# ===========

# Your interaction goes here.


# APP LAYOUT
# ==========
# https://github.com/plotly/dash-sample-apps/blob/master/apps/dash-study-browser/app.py


app.layout = html.Div([
    html.Div(children=[
        html.Div(header),
        html.Div([
            html.Div(
                className="row",
                children=[
                    # Tabs on left, confusion matrix underneath
                    html.Div(
                        className="six columns",
                        children=[
                            html.Div(
                                children=[html.Div(
                                    tabs,
                                    style={"border": "2px black solid",
                                           "height": "500px",
                                           "width": "350px",
                                           "margin-top": "5px",
                                           "margin-bottom": "5px",
                                           "margin-left": "15px"
                                           }
                                ),
                                ]
                            )
                        ]
                    ),
                    html.Div(
                        className="six columns",
                        children=[
                            html.Div(
                                children=[html.Div(
                                    data_tabs,
                                    style={"border": "2px black solid",
                                           "height": "500px",
                                           "width": "800px",
                                           "margin-top": "5px",
                                           "margin-bottom": "5px",
                                           "margin-left": "15px"
                                           }
                                ), html.Div(
                                    className="six columns",
                                    style={"margin": "auto"},
                                    children=html.Div(
                                        plot_tabs,
                                        style={"border": "2px black solid",
                                               "height": "500px",
                                               "width": "800px",
                                               "margin-top": "5px",
                                               "margin-bottom": "5px",
                                               "margin-left": "15px"
                                               }
                                    )
                                )
                                ]
                            )
                        ]
                    ),
                ]
            )
        ]),
        # SDM Curves
        sdm_curves,
        # DET Curves
        det_curves
    ],
        style={"margin": "5px 5px 5px 5px"}
    )
])


# CALLBACKS
# Callback to generate study data


@app.callback(Output('tabs-content', 'children'),
              [Input('main-tabs', 'value')])
def render_content(tab):
    if tab == 'tab-overview':
        return html.Div([
            html.P('Brief description of tool....')
        ])


@app.callback(Output('tabs-content-plots', 'children'),
              [Input('plot-tabs', 'value')])
def render_content(tab):
    if tab == 'tab-violin':
        return html.Div([
            html.H3('Violin Plots'),
            html.P('Default: Balanced Faces in the Wild Dataset')
        ])
    elif tab == 'tab-box':
        return html.Div([
            html.H3('Box Plots'),
            html.P('Brief description of tool....')
        ])
    elif tab == 'tab-sdm':
        return html.Div([
            html.H3('SDM Curves'),
            html.P('Brief description of tool....')
        ])


@app.callback(Output('tabs-content-data', 'children'),
              [Input('data-tabs', 'value')])
def render_content(tab):
    if tab == 'tab-input':
        return html.Div([
            html.H3('Violin Plots'),
            html.P('Default: Balanced Faces in the Wild Dataset')
        ])
    elif tab == 'tab-table':
        return html.Div([
            html.H3('Box Plots'),
            html.P('Brief description of tool....')
        ])
    elif tab == 'tab-summary':
        return html.Div([
            html.H3('SDM Curves'),
            html.P('Brief description of tool....')
        ])


if __name__ == '__main__':
    app.run_server(debug=True, port=4444)
