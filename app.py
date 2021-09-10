import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from flask import Flask
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash
# Connect to your app pages
#from apps import databaseOps, reports,mainDash

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

#app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# meta_tags are required for the app layout to be mobile responsive
app = dash.Dash(__name__, suppress_callback_exceptions=True,external_stylesheets=[dbc.themes.MATERIA, external_stylesheets],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )
server = app.server


