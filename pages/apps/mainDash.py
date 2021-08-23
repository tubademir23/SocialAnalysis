
from threading import local
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
from collections import Counter
import plotly.graph_objects as go

from alpha_vantage.timeseries import TimeSeries
# csv oku **************************************
DATA_PATH=os.path.abspath('data')

reply_list=["DiyanetTV","dibalierbas","DikenComTr","gazetesozcu", "diyanethbr","memurlarnet", "tgrthabertv", "TwiterSonSakika","vatan","stargazete","timeturk","hurhaber1","habervakti"]
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
            #row_selectable="multi",
            row_deletable=False,
            selected_rows=[],
            page_action="native",
            page_current= 0,
            page_size= 15,
             style_cell_conditional=[
            {
                'if': {'column_id': c},
                'textAlign': 'left'
            } for c in ['tweet', 'mentions','username',"Adı","hashtags"]]
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
                                    display_format='D/M/Y',
                                    placeholder='D/M/Y',
                                    date=datetime.today().date() - timedelta(days=30),
                                    className='ml-5',
                                ),dcc.DatePickerSingle(
                                    display_format='D/M/Y',
                                    placeholder='D/M/Y',
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
                    ], lang="tr"),
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
                    ], width=8),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("Takip Edilen"),
                            dbc.CardBody([
                                html.H2(id='followings', children="000")
                            ], style={'textAlign':'center'})
                        ]),
                    ], width=4),
                ]),
            ], style={'textAlign':'center'}),
        ], width=3),
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
                    ], width=2),
                    dbc.Col([
                        dbc.Card([
                            dbc.CardHeader("Toplam Etkileşim"),
                            dbc.CardBody([
                                html.H2(id='totals', children="000")
                            ], style={'textAlign':'center'})
                        ]),
                    ], width=4),
                ]),
            ], style={'textAlign':'center'}),
            
        ], width=5),
    ],className='mb-2')])
graphsLayout_=dbc.Container([ 
                        dbc.Row([
                            dbc.Col([
                                dcc.Graph(id='daily-likes', figure={},
                                          config={'displayModeBar':False})
                            ], width=4)
                        ]),], fluid=True)

tabsLayout=html.Div([dbc.Row([
        empty_col,
        dbc.Col([dbc.Tabs(
                                    [
                                        dbc.Tab(label="Tweetler", tab_id="tweets"),
                                        dbc.Tab(label="Alıntılar",tab_id="replies"),
                                        #dbc.Tab(label="Alıntılayanlar",tab_id="repliesUsers"),
                                        dbc.Tab(label="Mentions", tab_id="mentions"),
                                        dbc.Tab(label="Hashtags", tab_id="hashtags"),
                                    ],
                                    id="tabs",
                                    active_tab="tweets",
                                ),
                                html.Div(id="tab-content")
                        ], width=6)
                    ],className='mb-2')])
xstr = lambda s: s or ""
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

def get_tweets_df(username, bas_tarih, bit_tarih,to,text):
    file= get_newestFile("Tweets","csv")
    df_tweets= pd.read_csv(file)
 
    print("3: ",len(df_tweets[df_tweets["username"]==username]))
 
    df_filter= df_tweets[df_tweets.tweet.str.contains(text,case=False)  ]
    return df_filter

def get_replies_df(username, bas_tarih, bit_tarih,to,text):
    file= get_newestFile("Replies","csv")
    df_replies= pd.read_csv(file)

    df_replies= df_replies[df_replies.username.str.contains('|'.join(to))]
    
    df_filter= df_replies[df_replies.tweet.str.contains(text,case=False) ]

    return df_filter


def get_repliesUsers_df(username, bas_tarih, bit_tarih,to,text):
    df=get_replies_df(username, bas_tarih, bit_tarih,to,text)
    Replies = {x:y for x,y in zip(df['conversation_id'],df['replies_count'])}
    fetchedReplies =Counter(df['conversation_id'])
    df_repliesUsersCount=[]
    for tweet in Replies:
        df_repliesUsersCount.append([Replies[tweet],fetchedReplies[tweet]])

    return pd.DataFrame(df_repliesUsersCount, columns=["adı","count"])

def get_mentions_df(username, bas_tarih, bit_tarih, to,text):
    import ast
    mentions={}
    tweets=get_tweets_df(username, bas_tarih, bit_tarih, to,text)
    df_mentions_tweets= pd.DataFrame(tweets)
    for index, t in df_mentions_tweets.iterrows(): 
        for m in ast.literal_eval(t["mentions"]):
            if(m['screen_name'] in mentions):
                mentions[m['screen_name']]+=1
            else:
                mentions[m['screen_name']]=1
    mentions_df= pd.DataFrame(mentions.items(), columns=['Adı', 'Sayısı'])
    return mentions_df

def get_hashtags_df(username, bas_tarih, bit_tarih, to,text):
    import ast
    hashtags={}
    tweets=get_tweets_df(username, bas_tarih, bit_tarih, to,text)
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
    
    return pd.DataFrame(df_hashcount, columns=["Adı","Hashtag","Sayısı"])
 

layout = html.Div([
    html.Div(filterLayout),
    html.Div(summaryLayout),
    html.Div(tabsLayout),
    html.Div(graphsLayout_),
    #html.Div(graphsLayout)
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

get_method_dict={"replies":get_replies_df,"repliesUsers":get_repliesUsers_df, "tweets":get_tweets_df,"mentions":get_mentions_df, "hashtags":get_hashtags_df}
get_column_dict={"replies":["username","tweet", "date", "link","conversion_id", "hashtags","mentions"],
                "repliesUsers":["Adı","Hashtag","Sayısı"], 
                "tweets":["tweet", "date", "link","conversion_id", "hashtags","mentions"],
                "mentions":["Adı","Sayısı"], "hashtags":["Adı","Hashtag","Sayısı"]}


@app.callback(
    Output('daily-likes', 'figure'),
    Input('basTarih','date'),
    Input('bitTarih','date'),
)
def update_graph(basTarih, bitTarih):
    file= get_newestFile("Tweets","csv")
    print("update_graph",file)
    dff= pd.read_csv(file)
    #dff=dff[dff['date']<=bitTarih & dff['date']>=basTarih]
    dff['date_time']= dff['date']+ ' '+dff['time']
    dff_rv = dff.iloc[::-1]
    fig = px.line(dff_rv, x='date_time', y='likes_count', title="Beğeni Grafiği",
                   range_y=[dff_rv['likes_count'].min(), dff_rv['likes_count'].max()],
                   height=120).update_layout(margin=dict(t=0, r=0, l=0, b=20),
                                             paper_bgcolor='rgba(0,0,0,0)',
                                             plot_bgcolor='rgba(0,0,0,0)',
                                             yaxis=dict(
                                             title=None,
                                             showgrid=False,
                                             showticklabels=False
                                             ),
                                             xaxis=dict(
                                             title=None,
                                             showgrid=False,
                                             showticklabels=False
                                             ))
    return fig.update_traces(fill='tozeroy',line={'color':'green'})
    """
    day_start = dff_rv[dff_rv['date_time'] == dff_rv['date_time'].min()]['likes_count'].values[0]
    day_end = dff_rv[dff_rv['date_time'] == dff_rv['date_time'].max()]['likes_count'].values[0]

    if day_end >= day_start:
        return fig.update_traces(fill='tozeroy',line={'color':'green'})
    elif day_end < day_start:
        return fig.update_traces(fill='tozeroy',
                             line={'color': 'red'})
    """
@app.callback(
    Output("tab-content", "children"),
    [Input("tabs", "active_tab"),
    Input('hashtag', 'value'),
    Input('reply-selector', 'value')],
    [State('basTarih','date'),
    State('bitTarih','date'),
    State('username-selector', 'value')
    ]
)
def render_tab_content(active_tab, text, to, bas_tarih, bit_tarih, username):
      
    print("içerideyim", active_tab)
    
    if active_tab:
        run=get_method_dict[active_tab]
        df=run(username, bas_tarih, bit_tarih,xstr(to), xstr(text))
        return fn_datatable(df.to_dict('records'), get_column_dict[active_tab], 'table')
        