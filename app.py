import base64
import io
import os
import uuid

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import flask
import pandas as pd
import visualizations as viz
from dash.dependencies import Input, Output, State
from flask_caching import Cache

app_dir = os.getcwd()

filecache_dir = os.path.join(app_dir, 'cache-directory')

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

# Cache definition
cache = Cache(app.server, config={
    'CACHE_TYPE': 'simple',
    # Note that filesystem cache doesn't work on systems with ephemeral
    # filesystems like Heroku.
    # 'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache-directory',

    # should be equal to maximum number of users on the app at a single time
    # higher numbers will store more data in the filesystem / redis cache
    'CACHE_THRESHOLD': 5
})

# LAYOUT COMPONENTS
# ==========

# Your components go here.


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

session_id = str(uuid.uuid4())

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

# INTERACTION
# ===========

# Your interaction goes here.


# APP LAYOUT
# ==========
# https://github.com/plotly/dash-sample-apps/blob/master/apps/dash-study-browser/app.py


app.layout = html.Div(children=[
    html.Div(header),
    html.Div(className="row",
             children=[
                 html.Div(className="six columns",
                          children=[
                              overview, other_tabs],
                          style={"width": "25%",
                                 "padding": "5px"}),
                 html.Div(className="six columns",
                          children=[
                              data_tabs,
                              plot_tabs],
                          style={"width": "75%",
                                 "padding": "5px"}
                          )],
             style={"margin": "auto",
                    "height": "800px"}),
    html.Div(session_id, id='session-id', style={'display': 'none'})
], style={"padding": "5px"})


# CALLBACKS
# Callback to generate study data
def parse_table(contents, filename):
    '''
    Parse uploaded tabular file and return dataframe.
    '''
    print('Calling parse_table')

    default_study_data = "data/bfw-v0.1.5-datatable.csv"

    try:
        if contents is None:
            study_data = pd.read_csv(default_study_data)
        else:
            content_type, content_string = contents.split(",")
            decoded = base64.b64decode(content_string)
            study_data = pd.read_csv(io.StringIO(decoded.decode("utf-8")))
    except Exception as e:
        print(e)
    try:
        study_data = viz.relabel(study_data)
    except Exception as e:
        print(e)
    return study_data


def write_dataframe(session_id, df, filename="bfw-v0.1.5-datatable.csv"):
    '''
    Write dataframe to disk, for now just as CSV
    For now do not preserve or distinguish filename;
    user has one file at once.
    '''
    if filename is None:
        filename = "bfw-v0.1.5-datatable.csv"
    filename = session_id + filename
    print('Calling write_dataframe')
    file = os.path.join(filecache_dir, session_id)
    df.to_pickle(file)


@cache.memoize()
def read_dataframe(session_id, filename="bfw-v0.1.5-datatable.csv"):
    '''
    Read dataframe from disk, for now just as CSV
    '''
    if filename is None:
        filename = "bfw-v0.1.5-datatable.csv"
    filename = session_id + filename
    print('Calling read_dataframe')
    file = os.path.join(filecache_dir, session_id)
    df = pd.read_pickle(file)
    print('** Reading data from disk **')
    return df


@app.callback(
    Output('data-table-div', 'children'),
    [Input('upload-data', 'contents'),
     Input('upload-data', 'filename')],
    [State('session-id', 'children')])
def update_table(contents, filename, session_id):
    # write contents to file
    print('Calling update table')
    try:
        df = read_dataframe(session_id, filename)
    except Exception as e:
        print(e)
        df = parse_table(contents, filename).sample(50000)
        write_dataframe(session_id, df, filename)

    try:
        df = df.sample(50)[['p1', 'p2', 'Tag', 'id1', 'id2', 'att1', 'att2', 'score', 'subgroup', 'label']]
        df['score'] = pd.Series(["{0:.2f}%".format(val * 100) for val in df['score']], index=df.index)
    except Exception as e:
        print(e)
        df = df.sample(50)

    data_table = dash_table.DataTable(
        id='table',
        style_data={
            'whiteSpace': 'normal',
            'height': 'auto'
        },
        data=df.to_dict('records'),
        columns=[{"name": i, "id": i} for i in df.columns],
        style_table={'overflowX': 'scroll', 'padding': '15px',
                     'overflowY': 'scroll', 'height': '275px'},

        style_cell={
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
            'maxWidth': 0,
            'fontSize': 10,
            'font-family': 'arial'
        },
        sort_action='native',
        filter_action='native'
    )

    return data_table


@app.callback(Output('tabs-content-plots', 'children'),
              [Input('plot-tabs', 'value'),
               Input('upload-data', 'contents'),
               Input('upload-data', 'filename')],
              [State('session-id', 'children')])
def render_dist_tabs(tab, contents, filename, session_id):
    try:
        df = read_dataframe(session_id, filename)
    except Exception as e:
        print(e)
        df = parse_table(contents, filename)
        # write_dataframe(session_id, df, filename)

    if tab == 'tab-violin':
        return html.Div([
            dcc.Graph(figure=viz.violin_plot(df))
        ])
    elif tab == 'tab-box':
        return html.Div([
            dcc.Graph(figure=viz.box_plot(df))
        ])
    elif tab == 'tab-sdm':
        return html.Div([
            dcc.Graph(figure=viz.sdm_curve(df))
        ])


@app.callback(Output('tabs-content-data', 'children'),
              [Input('data-tabs', 'value')],
              [State('session-id', 'children')])
def render_data_tabs(tab, session_id):
    if tab == 'tab-frame':
        return html.Div([
            html.Div(id='data-table-div')])
    elif tab == 'tab-summary':
        return html.Div(html.Img(src='assets/summary-pivot.png',
                                 style={
                                     "width": "75%",
                                     "padding": "5px"
                                 }))


@app.callback(Output('tabs-content-other', 'children'),
              [Input('other-tabs', 'value')],
              [State('session-id', 'children')])
def render_other_tabs(tab, session_id):
    if tab == 'tab-matrix':
        return html.Div([
            html.Img(src='assets/confusion-matrix.png',
                     style={
                         "width": "100%",
                         "padding": "5px"
                     })
        ])
    elif tab == 'tab-det':
        return html.Div([dcc.Graph(figure=viz.mock_det())])


if __name__ == '__main__':
    app.run_server(debug=True, port=5050)
    print('session ended')
    cache.clear()
