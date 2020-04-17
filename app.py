import base64
import datetime
import io
import os
import uuid

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import flask
import layout
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
    'CACHE_DIR': 'cache-directory',
    # should be equal to maximum number of users on the app at a single time
    # higher numbers will store more data in the filesystem / redis cache
    'CACHE_THRESHOLD': 5
})

# LAYOUT COMPONENTS
# ==========

# Your components go here.


header = layout.header

upload_data = layout.upload_data

session_id = str(uuid.uuid4())

now = str(datetime.datetime.now())

overview = layout.overview

data_tabs = layout.data_tabs

other_tabs = layout.other_tabs

plot_tabs = layout.plot_tabs

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

    if contents is None:
        study_data = pd.read_csv(default_study_data)
    else:
        content_type, content_string = contents.split(",")
        decoded = base64.b64decode(content_string)
        study_data = pd.read_csv(io.StringIO(decoded.decode("utf-8")))

    try:
        study_data = viz.relabel(study_data)
    except Exception as e:
        print("Invalid data format")

    return study_data


def write_dataframe(session_id, df, filename="bfw-v0.1.5-datatable.csv"):
    '''
    Write dataframe to disk, for now just as CSV
    For now do not preserve or distinguish filename;
    user has one file at once.
    '''

    # filename = session_id + filename
    print('Calling write_dataframe')
    file = os.path.join(filecache_dir, now)
    df.to_pickle(file)


@cache.memoize()
def read_dataframe(now):
    '''
    Read dataframe from disk, for now just as CSV
    '''

    print('Calling read_dataframe')
    file = os.path.join(filecache_dir, now)
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
        df = read_dataframe(now)
    except Exception as e:
        print(e)
        df = parse_table(contents, filename).sample(5000)
        write_dataframe(session_id, df, filename)

    df = df.sample(50)[['p1', 'p2', 'Tag', 'id1', 'id2', 'att1', 'att2', 'score', 'subgroup', 'label']]
    df['score'] = pd.Series(["{0:.2f}%".format(val * 100) for val in df['score']], index=df.index)

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
        df = read_dataframe(now)
    except Exception as e:
        print(e)

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
