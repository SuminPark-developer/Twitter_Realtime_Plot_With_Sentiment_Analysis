import pandas_datareader.data as web
import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# https://pythonprogramming.net/dynamic-data-visualization-application-dash-python-tutorial/?completed=/interactive-interface-data-visualization-application-dash-python-tutorial/

app = dash.Dash()

# stock = 'TSLA'
# start = datetime.datetime(2015, 1, 1)
# end = datetime.datetime.now()
# df = web.DataReader(stock, 'yahoo', start, end)
# df.reset_index(inplace=True)
# df.set_index("Date", inplace=True)
#
# print(df.head())

app.layout = html.Div(children=[
    html.Div(children='''
        Symbol to graph:
    '''),
    dcc.Input(id='input', value='', type='text'),
    html.Div(id='output-graph'),
])

@app.callback(
    Output(component_id='output-graph', component_property='children'),
    [Input(component_id='input', component_property='value')]
)
def update_value(input_data):
    start = datetime.datetime(2015, 1, 1)
    end = datetime.datetime.now()
    df = web.DataReader(input_data, 'yahoo', start, end)
    df.reset_index(inplace=True)
    df.set_index("Date", inplace=True)

    return dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': df.index, 'y': df.Close, 'type': 'line', 'name': input_data},
            ],
            'layout': {
                'title': input_data
            }
        }
    )

if __name__ == '__main__':
    app.run_server(debug=True)

# 애플 symbol : AAPL | 테슬라 : TSLA