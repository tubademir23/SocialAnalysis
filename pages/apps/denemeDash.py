import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State, MATCH, ALL
import pandas as pd
from datetime import date
import calendar
from dash.exceptions import PreventUpdate
import sys, os
sys.path.insert(0, os.path.abspath('.'))
from app import app
external_stylesheets = [dbc.themes.BOOTSTRAP]

def idFunction(ind, indexList, i, days, weekDay):
  if ind==0 and days[weekDay][ind] not in [1,2,3,4,5,6]:
    m_id=date(2021, i-1, days[weekDay][ind])
  elif ind==indexList[-1] and days[weekDay][ind] not in [24,25,26,27,28,29, 30,31]:
    m_id=date(2021, i+1, days[weekDay][ind])
  else:
    m_id=date(2021, i, days[weekDay][ind])

  return m_id
my_calendar = html.Div([
    dbc.Row(
        dbc.Col(
            dcc.Dropdown(
                id="month",
                options=[{
                    "label": x,
                    "value": x
                } for x in calendar.month_name],
                value=calendar.month_name[date.today().month],
                clearable=False,
            ))),
    html.Br(),
    #dbc.Row(html.P(id="dbc-button")),
])

layout = html.Div([
                    html.Div(my_calendar, id='monthChoice'),
                    dbc.Row([
                        dbc.Col(
                            [html.Div("Monday"),
                             html.Div(id='monday')]),
                        dbc.Col([html.Div("Tuesday"),
                             html.Div(id='tuesday')]),
                        dbc.Col([html.Div("Wednesday"),
                             html.Div(id='wednesday')]),
                        dbc.Col([html.Div("Thursday"),
                             html.Div(id='thursday')]),
                        dbc.Col([html.Div("Friday"),
                             html.Div(id='friday')]),
                        dbc.Col([html.Div("Saturday"),
                             html.Div(id='saturday')]),
                        dbc.Col([html.Div("Sunday"),
                             html.Div(id='sunday')])
                    ], no_gutters=True),
                    html.Div(id="output"), 
                    html.Div(id="output2"),
                    dbc.Row(html.Div(id='Training-level')),
])
@app.callback([Output("monday", "children"),Output("tuesday", "children"), Output("wednesday", "children"), Output("thursday", "children"), Output("friday", "children"), Output("saturday", "children"), Output("sunday", "children"), Output("output", "children") ], [Input("month", "value")])
def table(value):
    df = [
        "January", "February", "March", "April", "May", "June", "July",
        "August", "September", "October", "November", "December"
    ]
    data1 = [
        'Preparative', 'Organizational', 'Maintenance', 'Thresold', 'Fitness',
        'Game', 'Recovery'
    ]
    print((value))
    for i, month in enumerate(df):
        if month == value:
            break
    i = i + 1
    days = calendar.monthcalendar(2021, i)
    previousMonth=calendar.monthcalendar(2021, i-1)
    nextMonth=calendar.monthcalendar(2021, i+1)
    a=0
    for j in days[0]:
      if j ==0:
        days[0][a]=previousMonth[-1][a]
      a+=1
    a=0
    for j in days[-1]:
      if j ==0:
        days[-1][a]=nextMonth[0][a]
      a+=1
    monday = []
    tuesday=[]
    wednesday=[]
    thursday=[]
    friday=[]
    saturday=[]
    sunday=[]
    data1 = [
        'Preparative', 'Organizational', 'Maintenance', 'Thresold', 'Fitness',
        'Game', 'Recovery', 'OFF'
    ]
    j = days
    days = pd.DataFrame(days)
    days.columns = [
        'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday',
        'Sunday'
    ]
    for ind in days.index:
        m_id=str(idFunction(ind, days.index, i, days, 'Monday'))
        t_id=str(idFunction(ind, days.index, i, days, 'Tuesday'))
        w_id=str(idFunction(ind, days.index, i, days, 'Wednesday'))
        th_id=str(idFunction(ind, days.index, i, days, 'Thursday'))
        f_id=str(idFunction(ind, days.index, i, days, 'Friday'))
        s_id=str(idFunction(ind, days.index, i, days, 'Saturday'))
        su_id=str(idFunction(ind, days.index, i, days, 'Sunday'))
        print("Here")
        if days['Monday'][ind] != 0:
            monday.append(
                dbc.Card(
                    dbc.CardBody([
                        html.Div(
                            dbc.Button(children=days['Monday'][ind],
                                       id={
                                           'type': 'date-button',
                                           'index': m_id
                                       },
                                       color="link")),
                        html.Div(id={
                'type': 'dropdown',
                'index': m_id}),
                                
                                       
                    ])))
        if days['Tuesday'][ind] != 0:
            tuesday.append(
                dbc.Card(
                    dbc.CardBody([
                        html.Div(
                            dbc.Button(children=days['Tuesday'][ind],
                                       id={
                                           'type': 'date-button',
                                           'index': t_id
                                       },
                                       color="link")),
                                      html.Div(id={
                'type': 'dropdown',
                'index': t_id})
                              
                    ])))
        if days['Wednesday'][ind] != 0:
            wednesday.append(
                dbc.Card(
                    dbc.CardBody([
                        html.Div(
                            dbc.Button(children=days['Wednesday'][ind],
                                       id={
                                           'type': 'date-button',
                                           'index': w_id
                                       },
                                       color="link")),
                                       html.Div(id={
                'type': 'dropdown',
                'index': w_id})
                    ])))
        if days['Thursday'][ind] != 0:
            thursday.append(
                dbc.Card(
                    dbc.CardBody([
                        html.Div(
                            dbc.Button(children=days['Thursday'][ind],
                                       id={
                                           'type': 'date-button',
                                           'index': th_id
                                       },
                                       color="link")),
                                       html.Div(id={
                'type': 'dropdown',
                'index': th_id})
                                      ])))
        if days['Friday'][ind] != 0:
            friday.append(
                dbc.Card(
                    dbc.CardBody([
                        html.Div(
                            dbc.Button(children=days['Friday'][ind],
                                       id={
                                           'type': 'date-button',
                                           'index': f_id
                                       },
                                       color="link")),
                                       html.Div(id={
                'type': 'dropdown',
                'index':f_id})
                                      ])))
        if days['Saturday'][ind] != 0:
            saturday.append(
                dbc.Card(
                    dbc.CardBody([
                        html.Div(
                            dbc.Button(children=days['Saturday'][ind],
                                       id={
                                           'type': 'date-button',
                                           'index': s_id
                                       },
                                       color="link")),
                                      html.Div(id={
                'type': 'dropdown',
                'index': s_id})
                                      ])))
        if days['Sunday'][ind] != 0:
            sunday.append(
                dbc.Card(
                    dbc.CardBody([
                        html.Div(
                            dbc.Button(children=days['Sunday'][ind],
                                       id={
                                           'type': 'date-button',
                                           'index': su_id
                                       },
                                       color="link")),
                                       html.Div(id={
                'type': 'dropdown',
                'index': su_id})
                                      ])))
    trap=html.Div("Hello")
    return monday,tuesday, wednesday, thursday, friday, saturday, sunday, trap
@app.callback(
    Output({
                'type': 'dropdown',
                'index': MATCH}, 'children'),
    Input({
                'type': 'date-button',
                'index': MATCH}, 'id'))
def update(id):
  print(id)
  value=id['index']
  data1 = [
        'Preparative', 'Organizational', 'Maintenance', 'Thresold', 'Fitness',
        'Game', 'Recovery', 'OFF'
    ]
  return dcc.Dropdown(
                                    id={
                'type': 'dropdown2',
                'index': value },
                                    options=[{
                                        "label": x,
                                        "value": x
                                    } for x in data1],
                                    value=data1[7],
                                    clearable=False,
                                )

@app.callback(Output('output2', 'children'),
    [dash.dependencies.Input({
                'type': 'dropdown2',
                'index': ALL }, 'value')])
def update_output(value):
    print("yenile")
    return html.Div(value)