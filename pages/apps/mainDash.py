
from dash_bootstrap_components._components.Row import Row
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input, State
import dash
import dash_bootstrap_components as dbc  # pip install dash-bootstrap-components
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
        dbc.Col([
            
        ], width=1),

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
                            html.Div('Kullanıcı Seçin', className='three columns'),
                            html.Div(dcc.Dropdown(id='kullanici-selector',
                                                options=[{'label':opt, 'value':opt} for opt in username_list], value="DiyanetTV"),
                                    className='nine columns')
                        ]),

                        # Select Season Dropdown
                        html.Div([
                            html.Div('Reply Hesap Seçin', className='three columns'),
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
        dbc.Col([
            
        ], width=1),
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

tabsLayout=html.Div([
    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        dbc.Container(
                        [
                            dbc.Tabs(
                                    [
                                        dbc.Tab(label="Tweetler", tab_id="tweets"),
                                        dbc.Tab(label="Alıntılar", tab_id="replies"),
                                        
                                    ],
                                    id="tabs",
                                    active_tab="tweets",
                                ),
                                html.Div(id="tab-content")
                        ])
                    ])
                ])
            ])
             , width=12
        )],
)
])

tab1_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("This is tab 1!", className="card-text"),
            dbc.Button("Click here", color="success"),
        ]
    ),
    className="mt-3",
)

tab2_content = dbc.Card(
    dbc.CardBody(
        [
            html.P("This is tab 2!", className="card-text"),
            dbc.Button("Don't click here", color="danger"),
        ]
    ),
    className="mt-3",
)
tabs = html.Div([
    dbc.Row([
        
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        dbc.Container(
                        [
                            
                            dbc.Tabs(
                                [
                                    dbc.Tab(tab1_content, label="Tab 1"),
                                    dbc.Tab(tab2_content, label="Tab 2"),
                                    dbc.Tab(
                                        "This tab's content is never seen", label="Tab 3", disabled=True
                                    ),
                                ]
                            ),
                                html.Div(id="tab-content2")
                        ])
                    ])
                ])
            ])
             , width=12
        )],
     )
])
def show_tweet(link):
    '''Display the contents of a tweet. '''
    url = 'https://publish.twitter.com/oembed?url=%s' % link
    response = requests.get(url)
    html = response.json()["html"]
    display(HTML(html))

def get_tweets_df(username, bas_tarih, bit_tarih):
    output_path=DATA_PATH+"\{} {}_{}.csv".format(username, bas_tarih, bit_tarih)
    df_tweets= pd.read_csv(output_path)
    return df_tweets

def get_replies_df(to, bas_tarih, bit_tarih):
    output_path=DATA_PATH+"\Replies {} {}_{}.csv".format(to, bas_tarih, bit_tarih)
    df_replies= pd.read_csv(output_path)
    return df_replies


layout = html.Div([
    html.Div(tabs),
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
    State('kullanici-selector', 'value'),
    State('reply-selector', 'value'),
    State('hashtag', 'value')]
)
    #,bas_tarih, bit_tarih

def update_dash(n_clicks,bas_tarih, bit_tarih, kullanici, reply, hashtag):
    date_object = date.fromisoformat(bas_tarih)
    date_bas= date_object.strftime('%B %d, %Y')

    date_object = date.fromisoformat(bit_tarih)
    date_bit= date_object.strftime('%B %d, %Y')

    print("yenileye girdim {} - {} - {} / @{}, @{}, H: {}".format(n_clicks,date_bas, date_bit,kullanici, reply, hashtag))
    
    dic_follow=get_followers_following(kullanici)
    (followers_num, followings_num)=(dic_follow["followers"], dic_follow["following"])
    nest_asyncio.apply()
    # replies
    df_replies= get_replies(bas_tarih, bit_tarih,kullanici)
    replies_num = len(df_replies)
    # tweets
    nest_asyncio.apply()
    df_list= get_tweets(bas_tarih, bit_tarih,kullanici)
    tweets_num = len(df_list)

    df_tweets = pd.DataFrame(df_list)
    
    print(type(df_tweets), df_tweets.head())
    for tw in df_tweets['nlikes'].head():
        print(tw, type(tw))
    
    #rt_links = df_tweets.sort_values(by= 'nreplies', ascending = False)['link'].values
    
    

    #,retweets_count,likes_count
    (likes_num,replies_num, retweets_num) = (sum(df_tweets['nlikes']), sum(df_tweets['nreplies']),sum(df_tweets['nretweets']))
    totals_num=likes_num+replies_num+ retweets_num
    print(followers_num, followings_num, replies_num, tweets_num, likes_num)
    #data['tweets']=df_tweets
    #data['replies']=df_replies
    print("çıkıştayım")
    return followers_num, followings_num, tweets_num, likes_num, replies_num, retweets_num, totals_num
    
    #return 'The input "{}" , clicked {} times'.format(value,n_clicks), followers_num, followings_num,5+n_clicks,6+n_clicks,7+n_clicks


@app.callback(
    Output("tab-content", "children"),
    [Input("tabs", "active_tab")],
    [State('basTarih','date'),
    State('bitTarih','date'),
    State('kullanici-selector', 'value'),
    State('reply-selector', 'value')]
)
def render_tab_content(active_tab, bas_tarih, bit_tarih, kullanici, to):
    """
    This callback takes the 'active_tab' property as input, as well as the
    stored graphs, and renders the tab content depending on what the value of
    'active_tab' is.
    """
    print("içerideyim")
    
    if active_tab:
            if active_tab == "replies":
                df_replies= get_replies_df(to, bas_tarih, bit_tarih)
                return dcc.Graph(figure=df_replies["scatter"])
            elif active_tab == "tweets":
                df_tweets= get_tweets_df(kullanici, bas_tarih, bit_tarih)
                return dash_table.DataTable(
                    id='table',
                    columns=[{"name": i, "id": i} for i in df_tweets.columns],
                    data=df_tweets.to_dict('records'),
                )
    "No tab selected"
