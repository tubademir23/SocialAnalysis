import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app
from app import server
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash
# Connect to your app pages
from apps import databaseOps, reports,mainDash

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', dbc.themes.BOOTSTRAP]
app.css.append_css({"external_url": external_stylesheets})

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink('Anasayfa ', href='./index',external_link=True)),
        dbc.NavItem(dbc.NavLink('Dash ', href='/apps/mainDash',external_link=True)),
        dbc.NavItem(dbc.NavLink('Veritabanı İşlemleri ', href='/apps/databaseOps',external_link=True)),
        dbc.NavItem(dbc.NavLink('Sorgulamalar ', href='/apps/reports',external_link=True)),
        dbc.NavItem(dbc.NavLink('Instagram ', href='/apps/instagramScrabing',external_link=True)),
        dbc.NavItem(dbc.NavLink('Facebook ', href='/apps/facebookScrabing',external_link=True)),
    ],
    brand=" DiyanetTV - Sosyal Medya Analizi ",
    brand_href="https://www.diyanet.tv/",
    color="primary",
    dark=True,
    expand='lg',
    sticky="top",
)
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(navbar),
    html.Div(id='page-content', children=[])
])

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/databaseOps':
        return databaseOps.layout
    if pathname == '/apps/mainDash':
        return mainDash.layout
    if pathname == '/apps/reports':
        return reports.layout
    
    else:
        return "404 Page Error! Please choose a link"


if __name__ == '__main__':
    app.run_server(debug=True, threaded=True)
