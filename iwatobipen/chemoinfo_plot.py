import base64
import os
import io
import numpy as np
import pandas as pd
import flask
import dash
import dash_dangerously_set_inner_html as dhtml
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
from rdkit import Chem
from rdkit.Chem import PandasTools
from rdkit.Chem import Descriptors
from rdkit.Chem import Draw
from rdkit.Chem.Draw import rdDepictor
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import useful_rdkit_utils
import dash_bootstrap_components as dbc
 
 
def smi2svg(smi):
    mol = Chem.MolFromSmiles(smi)
    rdDepictor.Compute2DCoords(mol)
    mc = Chem.Mol(mol.ToBinary())
    Chem.Kekulize(mc)
    drawer = Draw.MolDraw2DSVG(200,200)
    drawer.DrawMolecule(mc)
    drawer.FinishDrawing()
    svg = drawer.GetDrawingText().replace('svg:','')
    return svg
 
upload_style = {
    "width": "50%",
    "height": "120px",
    "lineHeight": "60px",
    "borderWidth": "1px",
    "borderStyle": "dashed",
    "borderRadius": "5px",
    "textAlign": "center",
    "margin": "10px",
    "margin": "3% auto",
}
 
#https://stackoverflow.com/questions/63459424/how-to-add-multiple-graphs-to-dash-app-on-a-single-browser-page
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
 
app.config.suppress_callback_exceptions=True
 
vals = {'PC-1':'PC-1',
        'PC-2':'PC-2',
        'TSNE-1':'TSNE-1',
        'TSNE-2': 'TSNE-2'}
 
app.layout = html.Div(children=[
    html.H1(children='Hello Chemoinfo'),
        dcc.Upload(
            id='sdf',
            children=html.Div(['upload sdf']),
            style=upload_style,
        ),
      
    html.Div(children='''
    Dash : sample plot
    '''),
  
    html.Div([dcc.Dropdown(id='x-column',
                           value='PC-1',
                           options=[{'label': key, 'value': key} for key in vals.keys()],
                           style={'width':'48%', 'display':'inline-block'}),
              dcc.Dropdown(id='y-column',
                           value='PC-2',
                           options=[{'label': key, 'value': key} for key in vals.keys()],
                           style={'width':'48%', 'display':'inline-block'}),
                           ]),
    html.Div([
        html.Div([html.Div(id="molimg")], className="two columns"),
        html.Div([dcc.Graph(id='mol_graph')], className="eight columns")
        ], 
        className="row"
        ),
     
    #html.Div([dcc.Graph(id='chemical-space')])
    ])
 
def parse_content(contents, filename):
 
    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)
    bio = io.BytesIO(decoded)
    bio.seek(0)
    try:
        df = PandasTools.LoadSDF(bio)
    except Exception as e:
        print(e)
        return html.Div([f"{filename} error occured during file reading"])
    X = [useful_rdkit_utils.mol2numpy_fp(m, 2, 1024) for m in df.ROMol]
    pca = PCA(n_components=2)
    tsne = TSNE()
    pca_res = pca.fit_transform(X)
    tsne_res = tsne.fit_transform(X)
    df['PC-1'] = pca_res[:,0]
    df['PC-2'] = pca_res[:,1]
    df['TSNE-1'] = tsne_res[:,0]
    df['TSNE-2'] = tsne_res[:,1]
    return df
 
@app.callback(
    Output('mol_graph', 'figure'),
    [Input('sdf', 'contents'),
    Input('x-column', 'value'),
    Input('y-column', 'value')],
    [State('sdf', 'filename')],
    prevent_initial_call=True
)
def drawgraph(contents,x_column_name, y_column_name ,filename):
    df = parse_content(contents, filename)
    return {'data':[go.Scatter(
        x=df[x_column_name],
        y=df[y_column_name],
        #text=['mol_{}'.format(i) for i in range(len(mols))],
        text=[Chem.MolToSmiles(mol) for mol in df.ROMol],
        mode='markers',
        marker={
            'size':15,
            'opacity':0.5
        }
    )],
    'layout':go.Layout(
        xaxis={'title':x_column_name},
        yaxis={'title':y_column_name}
    )}
 
@app.callback(
    Output('molimg', 'children'),
    [Input('mol_graph', 'hoverData'),
    ]
)
def update_img(hoverData):
    try:
        svg = smi2svg(hoverData['points'][0]['text'])
    except:
        svg = 'Select molecule'
    return dhtml.DangerouslySetInnerHTML(svg)
 
if __name__=="__main__":
 
    app.run_server(debug=True)