import base64
import datetime
import glob
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

app.config.suppress_callback_exceptions = True

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

error_tabs = layout.error_tabs

dist_tabs = layout.dist_tabs

hidden_error = html.Div(
    children=[
        html.Details(
            [html.Summary("Error Plots"),
             error_tabs]
        )
    ], style={"width": "100%"})

hidden_dist = html.Div(
    children=[
        html.Details(
            [html.Summary("Score Distribution Plots"),
             dist_tabs]
        )
    ], style={"width": "100%"})

# APP LAYOUT

app.layout = html.Div(
    children=[
        html.Div(header),

        html.Div(className="row",
                 children=[
                     html.Div(children=[
                         overview,
                         data_tabs],
                         style={"width": "25%",
                                "padding": "5px"}),
                     html.Div(children=[
                         hidden_dist,
                         hidden_error],
                         style={"width": "75%",
                                "padding": "5px"}
                     )],
                 style={"margin": "auto"}),

        html.Div(now, id='session-id', style={'display': 'none'})

    ], style={"padding": "5px"})


# CALLBACKS
# Callback to generate study data
def parse_table(contents, filename):
    '''
    Parse uploaded tabular file and return dataframe.
    '''

    print('Calling parse_table')

    default_study_data = "data/bfw-v0.1.5-datatable.csv"
    # print(contents)
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


def write_dataframe(df, filename):
    '''
    Write dataframe to disk, for now just as CSV
    Filename is simply the time the data is intialized
    '''
    print('Calling write_dataframe')

    file = os.path.join(filecache_dir, filename)

    print('New cache located at', file)
    df.to_pickle(file)


@cache.memoize()
def read_dataframe(filename, gender=['M', 'F'], ethnicity=['A', 'B', 'I', 'W']):
    '''
    Read dataframe from disk as PKL
    Takes values from filters to read only whats selected
    This function is called everytime the data is read
        i.e graphs, data table
    '''

    print('Calling read_dataframe')
    file = os.path.join(filecache_dir, filename)
    df = pd.read_pickle(file)
    df = df[df.e1.isin(ethnicity)]
    df = df[df.g1.isin(gender)]
    return df


@app.callback(
    Output('output-data-upload', 'children'),
    [Input('upload-data', 'contents')],
    [State('upload-data', 'filename'),
     State('upload-data', 'last_modified')])
def update_table(contents, filename, last_modified):
    """
    This is the first function called when the dashboard opens
    Takes in data from upload or uses default
    Creates pkl file of DF to be accessed
    Also takes in values from filters

    Need to adjust this so if the user uploads a new file it recognizes and gets a new timestamp or overwrites
    """
    print('Calling update table')
    # print('last modified', last_modified)

    print('Read file', filename)

    if filename is None:
        filename = "bfw-v0.1.5-datatable.csv"

    print(os.path.splitext(filename))

    file = now + os.path.splitext(filename)[0]

    print('Uploaded file', file)

    try:
        read_dataframe(file)
        print('Read existing cache', file)
    except:
        write_dataframe(parse_table(contents, filename).sample(5000), file)

    return filename


@app.callback(
    Output('data-table-div', 'children'),
    [Input('gender-filter', 'value'),
     Input('ethnicity-filter', 'value'),
     Input('column-filter', 'value')])
def print_table(gender, ethnicity, columns):
    cache_files = glob.glob(filecache_dir + '/*')  # gets all files from cache-directory
    latest_file = max(cache_files, key=os.path.getctime)  # calls most recent cache to be read
    print('Data table file:', latest_file)
    try:
        df = read_dataframe(latest_file, gender, ethnicity)
    except Exception as e:
        print('Uploading data...')

    df = df.sample(50, random_state=1)[columns]
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
                     'overflowY': 'scroll', 'height': '300px'},
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


@app.callback(Output('tabs-content-dist', 'children'),
              [Input('dist-tabs', 'value'),
               Input('gender-filter', 'value'),
               Input('ethnicity-filter', 'value')],
              [State('session-id', 'children')])
def render_dist_tabs(tab, gender, ethnicity, session_id):
    cache_files = glob.glob(filecache_dir + '/*')  # gets all files from cache-directory
    latest_file = max(cache_files, key=os.path.getctime)  # calls most recent cache to be read
    print('Dist plots file:', latest_file)

    df = read_dataframe(latest_file, gender, ethnicity)

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
        return html.Div([layout.column_filter,
                         html.Div(id='data-table-div')])
    elif tab == 'tab-summary':
        return html.Div()


@app.callback(Output('tabs-content-error', 'children'),
              [Input('error-tabs', 'value')],
              [State('session-id', 'children')])
def render_error_tabs(tab, session_id):
    if tab == 'tab-matrix':
        return html.Div()
    elif tab == 'tab-det':
        return html.Div([dcc.Graph(figure=viz.mock_det())])


if __name__ == '__main__':
    app.run_server(debug=True, port=5050)
    print('session ended')
    cache.clear()
