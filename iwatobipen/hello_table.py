from dash import Dash, html, dcc
from dash import dash_table
import pandas as pd
from sklearn.datasets import load_iris

data = load_iris()
targets = [data.target_names[i] for i in data.target]
df = pd.DataFrame(data.data, columns=data.feature_names)
df['target'] = targets

app = Dash(__name__)
app.layout = html.Div(children=[
    html.H1(children='Iris!!!'),
    html.Div(children="Divtag!"),
    dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns])
    ])

if __name__=="__main__":
    app.run_server(debug=True)