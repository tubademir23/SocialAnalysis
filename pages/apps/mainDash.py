
import collections
from itertools import combinations
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
import plotly.io as pio
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
graphsLayout=dbc.Container([ 
                        dbc.Row([
                            dbc.Col([
                                dcc.Graph(id='daily-likes', figure={},
                                          config={'displayModeBar':False})
                            ], width=6),
                            dbc.Col([
                                dcc.Graph(id='daily-replies', figure={},
                                          config={'displayModeBar':False})
                            ], width=6),
                        ]),
                        dbc.Row([empty_col]),
                        dbc.Row([
                            dbc.Col([
                                dcc.Graph(id='daily-retweets', figure={},
                                          config={'displayModeBar':False})
                            ], width=6),
                            dbc.Col([
                                dcc.Graph(id='daily-total', figure={},
                                          config={'displayModeBar':False})
                            ], width=6),
                        ]),
                        dbc.Row([
                            empty_col,
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardBody([
                                        dcc.Graph(id='pie-chart', figure={}, config={'displayModeBar': False}),
                                    ])
                                ]),
                            ], width=5),
                            dbc.Col([
                                dbc.Card([
                                    dbc.CardBody([
                                        dcc.Graph(id='wordcloud', figure={}, config={'displayModeBar': False}),
                                    ])
                                ]),
                            ], width=6)
                        ])], fluid=True)

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
def get_fig(table, y_, title_):
    return px.line( table, x='date', y=y_, title=title_+' ' +'Grafiği').update_layout(yaxis=dict(
                                             title="",
                                             showgrid=True,
                                             showticklabels=True
                                             ),
                                             xaxis=dict(
                                             title='Tarih',
                                             showgrid=True,
                                             showticklabels=True
                                             ))
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
    df_filter= df_tweets[df_tweets.tweet.str.contains(text,case=False)  ]
    return df_filter

def get_replies_df(username, bas_tarih, bit_tarih,to,text):
    file= get_newestFile("Replies","csv")
    df_replies= pd.read_csv(file)
    df_replies= df_replies[df_replies.username.str.contains('|'.join(xstr(to)))]    
    df_filter= df_replies[df_replies.tweet.str.contains(xstr(text),case=False) ]
    
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
    html.Div(graphsLayout),
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

def update_dash(n_clicks,bas_tarih, bit_tarih, username, reply, hashtag):
    date_object = date.fromisoformat(bas_tarih)
    date_bas= date_object.strftime('%B %d, %Y')

    date_object = date.fromisoformat(bit_tarih)
    date_bit= date_object.strftime('%B %d, %Y')

    #print("States: {} - {} - {} / @{}, @{}, H: {}".format(n_clicks,date_bas, date_bit,username, reply, hashtag))
    
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
  
    return followers_num, followings_num, tweets_num, likes_num, replies_num, retweets_num, totals_num
    

get_method_dict={"replies":get_replies_df,"repliesUsers":get_repliesUsers_df, "tweets":get_tweets_df,"mentions":get_mentions_df, "hashtags":get_hashtags_df}
get_column_dict={"replies":["username","tweet", "date", "link","conversion_id", "hashtags","mentions"],
                "repliesUsers":["Adı","Hashtag","Sayısı"], 
                "tweets":["tweet", "date", "link","conversion_id", "hashtags","mentions"],
                "mentions":["Adı","Sayısı"], "hashtags":["Adı","Hashtag","Sayısı"]}
        
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
    if active_tab:
        run=get_method_dict[active_tab]
        df=run(username, bas_tarih, bit_tarih,xstr(to), xstr(text))
        return fn_datatable(df.to_dict('records'), get_column_dict[active_tab], 'table')

        
dic_figs={"likes_count":["Beğeni",'red'], "replies_count":["Alıntı",'blue'], 'retweets_count':["Retweets",'green'],  'toplam_etkilesim':["Etkileşim",'purple']}
exclude_words = ['Şimdi','gelmek','demek','إِنْ','إِنَّ','لَـمْ','لَــمَّا','إِنَّ','لِماَ','Bu','Şu','Hep','Hiç','etmek','Etmek','Kim',
'Gelmek','demek','bilmek','Bilmek','dilemek','Dilemek','Şu','Bunlar','Şunlar','Gibi','Öyle ki','içinde',
'Önce','Onlar','-e, -a','dan','-dan',"-den",'den','-den -dan','Bazı','Ya da','değil',"Değil",'Söylemek',
'Öyle ki','Dek','Veya','ve','Ya','Ya Da',"olmak", "etmek",'veya','İçin','Eğer','önce','Ey','Sen','Ben','Biz','siz',
'biz','ben','O','için','öyle','gel','-de','sen','ey','bu','şu','o','bunlar','şunlar','onlar','Hani','İçinde','kez',
'az','Az','çok','Çok','en','ki','içinde','Eğer','üzerine','Öyle','yapmak','Fakat','Ama','Lakin','ancak','Ancak',
'ile','İle','-ki','bir','Başka','önce','sonra','arasında','Çok','Az','Sonra','söylemek','görmek','belki','https','http',"\"",'a','e','ı','i','o','ö','u','ü']
@app.callback(
    [Output('daily-likes', 'figure'),
    Output('daily-replies', 'figure'),
    Output('daily-retweets', 'figure'),
    Output('daily-total', 'figure'),
    Output('pie-chart','figure'),
    Output('wordcloud','figure')],
    Input('basTarih','date'),
    Input('bitTarih','date'),
    [State('hashtag', 'value'),
    State('reply-selector', 'value'),
    State('username-selector', 'value')],
)
def update_line(basTarih, bitTarih, text, to, username):
    file= get_newestFile("Tweets","csv")    
    dff= pd.read_csv(file)
    dff['date_time']= dff['date']+ ' '+dff['time']
    dff['date']=pd.to_datetime(dff["date"])
    dff=dff[dff['date']>=basTarih]
    dff['month']=dff['date'].dt.month
    dff['toplam_etkilesim']=dff['likes_count']+dff['replies_count']+ dff['retweets_count']
    dff = dff.iloc[::-1]    
    table = dff.groupby('date', as_index=False)[['likes_count','replies_count', 'retweets_count','toplam_etkilesim']].sum()
    
    table.set_index('date')
    figs=[]
    for key in dic_figs:
        fig=get_fig(table,key,dic_figs[key][0] )
        figs.append(fig.update_traces(line={'color':dic_figs[key][1] }))
    
    dff_replies= get_replies_df(username,basTarih,bitTarih,to,text)
    df_group =dff_replies.groupby('username', as_index=False)['id'].count()
    df_group.set_index('username')    
    df_group.loc[df_group.shape[0]] = ['Diğer[1]', len(df_group[df_group['id']==1])]
    df_group.drop(df_group[df_group['id']==1].index, inplace = True)
    df_group.rename(columns={'id':'Sayı','username':'Kullanıcı Adı'}, inplace = True)
    fig_pie = px.pie(df_group, names=df_group['Kullanıcı Adı'], values=df_group['Sayı'], title='Alıntı yapan kullanıcı dağılımı',
             
             color_discrete_sequence= px.colors.sequential.Blues)
                     
    fig_pie.update_layout(margin=dict(l=20, r=20, t=30, b=20))
    figs.append(fig_pie)

    dff_str = dff.tweet.astype(str)
    for val in dff_str: 
        val=str(val)
        tokens = val.split()
    for i in range(len(tokens)): 
        tokens[i] = tokens[i].lower() 
    comment_words=''
    for words in tokens: 
        comment_words = comment_words + words + ' '
    my_wordcloud = WordCloud(
        stopwords='./stopwords.txt',
        background_color='white',
        #height=275
    ).generate(comment_words)
    
    fig_wordcloud = px.imshow(my_wordcloud, template='ggplot2',
                              title="Kelime Bulutu")
    fig_wordcloud.update_layout(margin=dict(l=10, r=10, t=25, b=10))
    fig_wordcloud.update_xaxes(visible=False)
    fig_wordcloud.update_yaxes(visible=False)

    figs.append(fig_wordcloud)
    return figs
    