#dash in flask
from dash import Dash
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from werkzeug.serving import run_simple
import flask
 
from flask import Flask
from dash import html
server = Flask(__name__)
 
 
dash_app1 = Dash(__name__, server = server, url_base_pathname='/dashboard/' )
dash_app2 = Dash(__name__, server = server, url_base_pathname='/reports/')
dash_app1.layout = html.Div([html.H1('Hi there, I am app1 for dashboards')])
dash_app2.layout = html.Div([html.H1('Hi there, I am app2 for reports')])

@server.route('/')
def top():
    return '<H1>hello world</H1>'

@server.route('/dashboard/')
def render_dashboard():
    return flask.redirect('/dash1')
 
 
@server.route('/reports/')
def render_reports():
    return flask.redirect('/dash2')
 
app = DispatcherMiddleware(server, {
    '/dash1': dash_app1.server,
    '/dash2': dash_app2.server,
})
 
run_simple('localhost', 8080, app, use_reloader=True, use_debugger=True)
