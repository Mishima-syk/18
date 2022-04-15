from dash import Dash, html, dcc
from dash import Output, Input
import plotly.express as px
import pandas as pd
from sklearn.datasets import load_iris

data = load_iris()
targets = [data.target_names[i] for i in data.target]
df = pd.DataFrame(data.data, columns=data.feature_names)
df['target'] = targets



app = Dash(__name__)
app.layout = html.Div(children=[
    html.H1(children='Iris!!!'),
    dcc.Dropdown(data.feature_names, id='x-axis'),
    dcc.Dropdown(data.feature_names, id='y-axis'),
    dcc.Graph(
        id="iris"
    )
])

@app.callback(Output('iris', 'figure'),
              Input('x-axis', 'value'),
              Input('y-axis', 'value')
              )
def updatefig(xval, yval):
    fig = px.scatter(df, 
                x=xval, 
                y=yval,
                color='target'
                )
    return fig

if __name__=="__main__":
    app.run_server(debug=True)