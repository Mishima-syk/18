import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html
import pandas as pd
import plotly.express as px

from sklearn.datasets import load_iris
data = load_iris()
targets = [data.target_names[i] for i in data.target]
df = pd.DataFrame(data.data, columns=data.feature_names)
df['target'] = targets

fig1 = px.scatter(df, x=data.feature_names[0], y=data.feature_names[1], color='target')
fig2 = px.scatter(df, x=data.feature_names[1], y=data.feature_names[2], color='target')
fig3 = px.bar(df, x='target')

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Sidebar", className="display-4"),
        html.Hr(),
        html.P(
            "A simple sidebar layout with navigation links", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Page 1", href="/page-1", active="exact"),
                dbc.NavLink("Page 2", href="/page-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)


content = html.Div(
    [
        dbc.Row(
            [
                dbc.Col([html.P('scatter plot1'),dcc.Graph(id='fig1',figure=fig1)], width=6), 
                dbc.Col([html.P('scatter plot2'),dcc.Graph(id='fig2', figure=fig2)], width=6)
            ]
        ),
        dbc.Row(
            [
                dbc.Col(dcc.Graph(id='fig3', figure=fig3))
            ]
        ),
    ]
, style=CONTENT_STYLE)
app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


if __name__ == "__main__":
    app.run_server(debug=True)