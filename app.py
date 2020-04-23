import base64
import datetime
import glob
import io
import os

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
    'CACHE_THRESHOLD': 5
})

# LAYOUT COMPONENTS
# ==========

# Your components go here.


header = layout.header

upload_data = layout.upload_data

now = str(datetime.datetime.now())

overview = layout.overview

data_tabs = layout.data_tabs

hidden_error = layout.hidden_error

hidden_dist = layout.hidden_dist

# APP LAYOUT
app.layout = html.Div(
    children=[
        html.Div(header),

        html.Div(className="row",
                 children=[
                     html.Div(children=[
                         overview,
                         data_tabs],
                         style={"width": "30%",
                                "padding": "5px"}),
                     html.Div(children=[
                         hidden_dist,
                         hidden_error],
                         style={"width": "70%",
                                "padding": "5px"}
                     )],
                 style={"margin": "auto"}),

        html.Div(now, id='session-id', style={'display': 'none'})

    ], style={"padding": "5px"})


# CALLBACKS
def parse_table(contents):
    '''
    Parse uploaded tabular file and return dataframe.
    Reads uploaded data to dataframe
    If no data is uploaded the default dataset is read
    '''

    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    study_data = pd.read_csv(io.StringIO(decoded.decode("utf-8")))

    try:
        study_data = viz.relabel(study_data)
    except Exception as e:
        print("Invalid data format")

    return study_data


@cache.memoize()
def write_dataframe(df, filename):
    print('Calling write_dataframe')
    file = os.path.join(filecache_dir, filename)
    print('New cache located at', file)
    df.to_pickle(file)


def read_dataframe(filename, gender=['M', 'F'], ethnicity=['A', 'B', 'I', 'W']):
    '''
    Read dataframe from disk as PKL
    Takes values from filters to read only whats selected
    This function is called every time the data is read
        i.e graphs, data table
    '''
    file = os.path.join(filecache_dir, filename)
    df = pd.read_pickle(file)

    # if statement prevents error when user deselects all options
    if len(ethnicity) > 0:
        df = df[df.e1.isin(ethnicity)]
    if len(gender) > 0:
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

    if contents is None:  # initializes dashboard with default data if it has just been opened
        file = "default"
        filename = "bfw-v0.1.5-datatable.csv"
    else:
        file = now + os.path.splitext(filename)[0]

    print('Uploaded file:', file)

    try:
        # Checks to see if file has already been uploaded
        read_dataframe(file)
        # print('Read existing cache', file)
    except:
        write_dataframe(parse_table(contents).sample(5000), file)

    return filename


# 'refresh-button'

@app.callback(
    Output('data-table-div', 'children'),
    [Input('gender-filter', 'value'),
     Input('ethnicity-filter', 'value'),
     Input('score-filter', 'value'),
     Input('column-filter', 'value'),
     Input('upload-data', 'contents')],
    [State('upload-data', 'last_modified')])
def print_table(gender, ethnicity, score, columns, contents, last_modified):
    if contents is None:
        file = "default"
    else:
        cache_files = glob.glob(filecache_dir + '/*')  # gets all files from cache-directory
        file = max(cache_files, key=os.path.getctime)  # calls most recent cache to be read

    print("Data Table Data:", file)

    df = read_dataframe(file, gender, ethnicity)
    df['score'] = pd.Series(["{0:.2f}%".format(val * 100) for val in df[score]], index=df.index)
    df = df.sample(50, random_state=1)[columns]

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
        sort_action='native'
    )

    return data_table


@app.callback(Output('tabs-content-dist', 'children'),
              [Input('dist-tabs', 'value'),
               Input('gender-filter', 'value'),
               Input('ethnicity-filter', 'value'),
               Input('score-filter', 'value'),
               Input('upload-data', 'contents')],
              [State('upload-data', 'last_modified')])
def render_dist_tabs(tab, gender, ethnicity, score, contents, last_modified):
    if contents is None:
        file = "default"
    else:
        cache_files = glob.glob(filecache_dir + '/*')  # gets all files from cache-directory
        file = max(cache_files, key=os.path.getctime)  # calls most recent cache to be read

    print("Distribution Plots Data:", file)

    df = read_dataframe(file, gender, ethnicity)

    if tab == 'tab-violin':
        return html.Div([
            dcc.Graph(figure=viz.violin_plot(df, score))
        ])
    elif tab == 'tab-box':
        return html.Div([
            dcc.Graph(figure=viz.box_plot(df, score))
        ])
    elif tab == 'tab-sdm':
        return html.Div([
            dcc.Graph(figure=viz.sdm_curve(df, score))
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
              [Input('error-tabs', 'value'),
               Input('gender-filter', 'value'),
               Input('ethnicity-filter', 'value'),
               Input('score-filter', 'value'),
               Input('upload-data', 'contents')],
              [State('upload-data', 'last_modified')])
def render_error_tabs(tab, gender, ethnicity, score, contents, last_modified):
    if contents is None:
        file = "default"
    else:
        cache_files = glob.glob(filecache_dir + '/*')  # gets all files from cache-directory
        file = max(cache_files, key=os.path.getctime)  # calls most recent cache to be read

    print("Error Plots Data:", file)

    df = read_dataframe(file, gender, ethnicity)

    if tab == 'tab-matrix':
        return html.Div()
    elif tab == 'tab-det':
        return html.Div(
            [
                html.Div([
                    dcc.Graph(figure=viz.det_ethnicity(df, score),
                              style={"display": "inline-block", "width": "50%"}),
                    dcc.Graph(figure=viz.det_gender(df, score),
                              style={"display": "inline-block", "width": "50%"})
                ]),
                dcc.Graph(figure=viz.det_subgroup(df, score))
            ], style={"margin": "0px",
                      "padding": "0px"}
        )
    elif tab == 'tab-roc':
        return html.Div(
            [
                html.Div([
                    dcc.Graph(figure=viz.roc_ethnicity(df, score),
                              style={"display": "inline-block", "width": "50%"}),
                    dcc.Graph(figure=viz.roc_gender(df, score),
                              style={"display": "inline-block", "width": "50%"})
                ]),
                dcc.Graph(figure=viz.roc_subgroup(df, score))
            ], style={"margin": "0px",
                      "padding": "0px"}
        )


if __name__ == '__main__':
    app.run_server(debug=True, port=5050)
    print('session ended')
