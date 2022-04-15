from dash import Dash, html, dcc

app = Dash(__name__)

app.layout = html.Div(
    children=[html.H1("Hello Dash!")]
)

if __name__=="__main__":
    app.run_server(debug=True)