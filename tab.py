import dash
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    html.H1('Dash Tabs Test stuff'),
    dcc.Tabs(id="tabs-example", value='tab-1-example', children=[
        dcc.Tab(label='Data', value='tab-1-example'),
        dcc.Tab(label='Dataframe', value='tab-2-example'),
        dcc.Tab(label='Overview', value='tab-3-example'),
    ]),
    html.Div(id='tabs-content-example')
])


@app.callback(Output('tabs-content-example', 'children'),
              [Input('tabs-example', 'value')])
def render_content(tab):
    if tab == 'tab-1-example':
        return html.Div(
            className="row card",
            children=[
                html.H6("Select Data"),
                # User Controls
                html.Div(
                    className="four columns card",
                    children=[
                        # data_select,
                        html.Div(
                            children=[
                                html.Div(
                                    className="padding-top-bot",
                                    children=[
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
    elif tab == 'tab-2-example':
        return html.Div([
            html.H3('Dataframe'),
            dcc.Graph(
                id='graph-2-tabs',
                figure={
                    'data': [{
                        'x': [1, 2, 3],
                        'y': [5, 10, 6],
                        'type': 'bar'
                    }]
                }
            )
        ])
    elif tab == 'tab-3-example':
        return html.Div([
            html.H3('Overview'),
            html.P('Brief description of tool....')
        ])


if __name__ == '__main__':
    app.run_server(debug=True)
