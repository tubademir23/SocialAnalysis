
from dash_bootstrap_components._components.Row import Row
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input, State
import dash
import dash_bootstrap_components as dbc
from numpy import dtype  # pip install dash-bootstrap-components
import plotly.express as px              # pip install plotly
import pandas as pd                      # pip install pandas
from datetime import datetime, timedelta
from wordcloud import WordCloud          # pip install wordcloud
import sys, os
sys.path.insert(0, os.path.abspath('...'))
from jupyter_dash import JupyterDash 
from twint_lib import get_tweets, get_followers_following, get_replies
from app import app
from datetime import date
import nest_asyncio
import dash_table
from IPython.display import HTML, display
import requests
import os.path
import glob
# csv oku **************************************
DATA_PATH=os.path.abspath('data')
df_cnt = pd.read_csv(DATA_PATH+"\DiyanetTV.csv")
df_cnt["date"] = pd.to_datetime(df_cnt["date"])
df_cnt["day"] = df_cnt["date"].dt.day
df_cnt["month"] = df_cnt["date"].dt.month

"""
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', dbc.themes.BOOTSTRAP]
app.css.append_css({"external_url": external_stylesheets})
"""
reply_list=["DiyanetTV","DikenComTr","gazetesozcu", "diyanethbr","memurlarnet", "tgrthabertv", "TwiterSonSakika","vatan","stargazete","timeturk","hurhaber1","habervakti"]
username_list= ["Diyanet","DiyanetTV","DR_FatihKurt"]

def fn_datatable(_data, _columns, id_):
    #print(_columns)
    return html.Div([
        dash_table.DataTable(
            id=id_,
            data=_data,
            columns=[
                {"name": i, "id": i, "deletable": False, "selectable": False} for i in _columns
            ],
            editable=False,
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            row_selectable="multi",
            row_deletable=False,
            selected_rows=[],
            page_action="native",
            page_current= 0,
            page_size= 6,
            # page_action='none',
            # style_cell={
            # 'whiteSpace': 'normal'
            # },
            # fixed_rows={ 'headers': True, 'data': 0 },
            # virtualization=False,
            style_cell_conditional=[
                {'if': {'column_id': 'username'},
                 'width': '40%', 'textAlign': 'left'}
            ],
        ),
    ],className='row')
empty_col=dbc.Col([
            
        ], width=1)

graphsLayout=html.Div([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='line-chart', figure={}, config={'displayModeBar': False}),
                ])
            ]),
        ], width=6),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='bar-chart', figure={}, config={'displayModeBar': False}),
                ])
            ]),
        ], width=6),
    ],className='mb-2'),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='TBD', figure={}),
                ])
            ]),
        ], width=4),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='pie-chart', figure={}, config={'displayModeBar': False}),
                ])
            ]),
        ], width=4),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dcc.Graph(id='wordcloud', figure={}, config={'displayModeBar': False}),
                ])
            ]),
        ], width=4),
    ],className='mb-2')
])
filterLayout=html.Div([dbc.Row([
        empty_col,

        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.Div([
                            html.Div('Tarih Aralığı', className='three columns'),
                            html.Div([
                                dcc.DatePickerSingle(
                                    id='basTarih',
                                    date=datetime.today().date() - timedelta(days=15),
                                    className='ml-5'
                                ),dcc.DatePickerSingle(
                                    id='bitTarih',
                                    date=datetime.today().date(),
                                    className='mb-2 ml-2'
                                ),
                            ],className='nine columns' ),
                        ]),
                        html.Div([
                            html.Div('Hashtag', className='three columns'),
                            html.Div(dcc.Input(id="hashtag", type="text", placeholder="",className='ml-5'),className='nine columns')
                        ]),
                    ]),
                ])
            ],  color="light"),
        ], width=3), 
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        # Select Division Dropdown
                        html.Div([
                            html.Div('Kullanıcı', className='three columns'),
                            html.Div(dcc.Dropdown(id='username-selector',
                                                options=[{'label':opt, 'value':opt} for opt in username_list], value="DiyanetTV"),
                                    className='nine columns')
                        ]),

                        # Select Season Dropdown
                        html.Div([
                            html.Div('Alıntı Hesap', className='three columns'),
                            html.Div(dcc.Dropdown(id='reply-selector', 
                            options=[{'label':opt, 'value':opt} for opt in reply_list], placeholder="Seçiniz", multi=True),
                                    className='nine columns')
                        ]),
                    ]),
                ])
            ])
        ], width=4), 
        dbc.Col([
            dbc.Card([
                dbc.CardBody([                    
                        html.Div([                        
                            dbc.Button(
                                ("Tweet'den Çek"),
                                color="primary",
                                block=True,
                                id="btnYenile",
                                className="mr-1"
                            )
                        ], style={'textAlign':'center', 'textSize':'10px'}),
                ])
            ])
        ], width=2),
    ],className='mb-2 mt-2'),
    dbc.Row([
        dbc.Col([dbc.Card([
                dbc.CardBody([                    
                        html.Div([    ]) ])])], width=12)],className='mb-2 mt-2'),
])

summaryLayout=html.Div([
dbc.Row([
        empty_col,
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Takipçi Bilgileri"),
                
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("Takipçi"),
                            dbc.CardBody([
                                html.H2(id='followers', children="000")
                            ], style={'textAlign':'center'})
                        ]),
                    ], width=6),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("Takip Edilen"),
                            dbc.CardBody([
                                html.H2(id='followings', children="000")
                            ], style={'textAlign':'center'})
                        ]),
                    ], width=6),
                ]),
            ], style={'textAlign':'center'}),
        ], width=2),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Tweets"),
                
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("___"),
                            dbc.CardBody([
                                html.H2(id='tweets', children="000")
                            ], style={'textAlign':'center'})
                        ]),
                    ], width=12),
                ]),
            ], style={'textAlign':'center'}),
        ], width=2),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Etkileşim Bilgileri"),
                
                dbc.Row([
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("Beğeni"),
                            dbc.CardBody([
                                html.H2(id='likes', children="000")
                            ], style={'textAlign':'center'})
                        ]),
                    ], width=3),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("Retweets"),
                            dbc.CardBody([
                                html.H2(id='retweets', children="000")
                            ], style={'textAlign':'center'})
                        ]),
                    ], width=3),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("Alıntı"),
                            dbc.CardBody([
                                html.H2(id='replies', children="000")
                            ], style={'textAlign':'center'})
                        ]),
                    ], width=3),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("Toplam Etkileşim"),
                            dbc.CardBody([
                                html.H2(id='totals', children="000")
                            ], style={'textAlign':'center'})
                        ]),
                    ], width=3),
                ]),
            ], style={'textAlign':'center'}),
            
        ], width=4),
    ],className='mb-2')])

tabsLayout=html.Div([dbc.Row([
        empty_col,
        dbc.Col([dbc.Tabs(
                                    [
                                        dbc.Tab(label="Tweetler", tab_id="tweets"),
                                        dbc.Tab(label="Alıntılar",tab_id="replies"),
                                        dbc.Tab(label="Mentions", tab_id="mentions"),
                                        dbc.Tab(label="Hashtags", tab_id="hashtags"),
                                    ],
                                    id="tabs",
                                    active_tab="tweets",
                                ),
                                html.Div(id="tab-content")
                        ], width=6)
                    ],className='mb-2')])

def get_bestFile(start_suffix,bas_tarih, bit_tarih, suffix):
    for file in os.listdir(DATA_PATH):
        if file.endswith(suffix) and file.startswith(start_suffix):
            name=os.path.splitext(file)
            (sf_bas_tarih, sf_bit_tarih)= name[0].split()[2].split("_")
            if sf_bas_tarih<=bas_tarih and sf_bit_tarih>= bit_tarih:
                return file
    
def get_newestFile(start_suffix, suffix):
    files = glob.glob(DATA_PATH+"\*"+start_suffix+"*"+ suffix)
    max_file = max(files, key=os.path.getctime)         
    return max_file

def show_tweet(link):
    '''Display the contents of a tweet. '''
    url = 'https://publish.twitter.com/oembed?url=%s' % link
    response = requests.get(url)
    html = response.json()["html"]
    display(HTML(html))

def get_tweets_df(username, bas_tarih, bit_tarih):
    file= get_newestFile("Tweets","csv")
    df_tweets= pd.read_csv(file)
    return df_tweets

def get_replies_df(to, bas_tarih, bit_tarih):
    file= get_newestFile("Replies","csv")
    df_replies= pd.read_csv(file)
    return df_replies

def get_hashtags_df(username, bas_tarih, bit_tarih):
    import ast
    hashtags={}
    tweets=get_tweets_df(username, bas_tarih, bit_tarih)
    df_hash_tweets= pd.DataFrame(tweets)
    df_hashcount=[]
    for index, t in df_hash_tweets.iterrows(): 
       for h in ast.literal_eval(t["hashtags"]):
            if(t["username"] in hashtags):
                if(h in hashtags[t.username]):
                    hashtags[t.username][h] += 1
                else:
                    hashtags[t.username][h]=1
            else:
                hashtags[t.username]={h:1}
    
    for user in hashtags:
        for h in hashtags[user]:
            df_hashcount.append([user, h, hashtags[user][h]])
    print(df_hashcount)
    return pd.DataFrame(df_hashcount, columns=["username","hashtag","count"])
    
    #return pd.DataFrame(hashtags, columns=["username,hashtag,count"])

layout = html.Div([
    html.Div(filterLayout),
    html.Div(summaryLayout),
    html.Div(tabsLayout),

    html.Div(graphsLayout)
]#, fluid=True
)

@app.callback(
    Output('followers','children'),
    Output('followings','children'),
    Output('tweets','children'),
    Output('likes','children'),
    Output('replies','children'), 
    Output('retweets','children'),   
    Output('totals','children'),
    [Input('btnYenile', 'n_clicks')],
    [State('basTarih','date'),
    State('bitTarih','date'),
    State('username-selector', 'value'),
    State('reply-selector', 'value'),
    State('hashtag', 'value')]
)
    #,bas_tarih, bit_tarih

def update_dash(n_clicks,bas_tarih, bit_tarih, username, reply, hashtag):
    date_object = date.fromisoformat(bas_tarih)
    date_bas= date_object.strftime('%B %d, %Y')

    date_object = date.fromisoformat(bit_tarih)
    date_bit= date_object.strftime('%B %d, %Y')

    print("States: {} - {} - {} / @{}, @{}, H: {}".format(n_clicks,date_bas, date_bit,username, reply, hashtag))
    
    dic_follow=get_followers_following(username)
    (followers_num, followings_num)=(dic_follow["followers"], dic_follow["following"])
    nest_asyncio.apply()
    # replies
    df_replies= get_replies(bas_tarih, bit_tarih,username)
    replies_num = len(df_replies)
    # tweets
    nest_asyncio.apply()
    df_list= get_tweets(bas_tarih, bit_tarih,username)
    tweets_num = len(df_list)

    df_tweets = pd.DataFrame(df_list)
    
    (likes_num,replies_num, retweets_num) = (sum(df_tweets['nlikes']), sum(df_tweets['nreplies']),sum(df_tweets['nretweets']))
    totals_num=likes_num+replies_num+ retweets_num
    print("return")
    return followers_num, followings_num, tweets_num, likes_num, replies_num, retweets_num, totals_num
    
    #return 'The input "{}" , clicked {} times'.format(value,n_clicks), followers_num, followings_num,5+n_clicks,6+n_clicks,7+n_clicks


@app.callback(
    Output("tab-content", "children"),
    [Input("tabs", "active_tab")],
    [State('basTarih','date'),
    State('bitTarih','date'),
    State('username-selector', 'value'),
    State('reply-selector', 'value')]
)
def render_tab_content(active_tab, bas_tarih, bit_tarih, username, to):
  
    print("içerideyim", active_tab)
    
    if active_tab:
            if active_tab == "replies":
                df_replies= get_replies_df(username, bas_tarih, bit_tarih)
                return fn_datatable(df_replies.to_dict('records'), df_replies.columns, 'table')
            elif active_tab == "tweets":
                df_tweets= get_tweets_df(username, bas_tarih, bit_tarih)
                return fn_datatable(df_tweets.to_dict('records'), df_tweets.columns, 'table')
            elif active_tab == "mentions":
                df_tweets= get_tweets_df(username, bas_tarih, bit_tarih)
                return fn_datatable(df_tweets.to_dict('records'), df_tweets.columns, 'table')
            elif active_tab == "hashtags":
                dic_hashtags= get_hashtags_df(username, bas_tarih, bit_tarih)
                return fn_datatable(dic_hashtags.to_dict('records'), dic_hashtags.columns, 'table')
    return "No tab selected"
