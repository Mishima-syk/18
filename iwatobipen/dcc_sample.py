from dash import Dash, dcc, html

app = Dash(__name__)
app.layout = html.Div(children=[
    dcc.Input(id='input', placeholder='input text here'),
    html.Hr(),
    dcc.Dropdown(['one', 'two', 'three'], 'one', id='dropdown'),
    html.Hr(),
    dcc.RadioItems(['hoge', 'huga'], 'hoge'),
    html.Hr(),
    dcc.RangeSlider(0, 20, 1, value=[5,15],id='rangeslider')
])

if __name__=="__main__":
    app.run_server(debug=True)

