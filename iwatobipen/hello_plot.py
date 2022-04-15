from dash import Dash, html, dcc
import plotly.express as px
import pandas as pd
from sklearn.datasets import load_iris

data = load_iris()
targets = [data.target_names[i] for i in data.target]
df = pd.DataFrame(data.data, columns=data.feature_names)
df['target'] = targets

fig = px.scatter(df, 
                x=data.feature_names[0], 
                y=data.feature_names[1],
                color='target'
                )

app = Dash(__name__)
app.layout = html.Div(children=[
    html.H1(children='Iris!!!'),
    html.Div(children="Divtag!"),
    dcc.Graph(
        id="iris!",
        figure=fig
    )
])

if __name__=="__main__":
    app.run_server(debug=True)