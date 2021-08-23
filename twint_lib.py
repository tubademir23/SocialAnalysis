from dataclasses import replace
from datetime import datetime
import twint
import nest_asyncio
import os
DATA_PATH=os.path.abspath('data')

def get_followers_following(username):
  
    dic={}
    c = twint.Config()
    c.Username = username
    c.Hide_output = True
    c.Store_object = True
    sonuc= twint.run.Lookup(c)

    fol = twint.output.users_list[:]
    dic["followers"] = fol[0].followers
    dic["following"] = fol[0].following
    return dic

def get_replies(bas_tarih, bit_tarih, to):
    nest_asyncio.apply()
    twint.output.clean_lists
    twint.storage.panda.Tweets_df=[]

    replies = twint.Config()
    #replies.Since = bas_tarih
    #replies.Until = bit_tarih
    replies.Hide_output=True
    replies.Pandas = True
    replies.To = "@"+to
    replies.Store_object = True
    replies.Store_csv = True
    replies.Pandas=True
    output_path=DATA_PATH+"\Replies {} {}_{}.csv".format(to, bas_tarih, bit_tarih)
    if os.path.exists(output_path):
        os.remove(output_path)
    replies.Output = output_path
    twint.run.Search(replies)
    df = twint.storage.panda.Tweets_df
    print(len(df))
    return df

def get_tweets(bas_tarih, bit_tarih, username):
    
    twint.output.clean_lists
    twint.storage.panda.Tweets_df=[]
    output_path= DATA_PATH+"\Tweets {} {}_{}.csv".format(username, bas_tarih, bit_tarih)
    if os.path.exists(output_path):
        os.remove(output_path)

  
    c = twint.Config()
    c.Username = username
    #c.Since = bas_tarih
    #c.Until = bit_tarih
    c.Hide_output=True
    c.Store_object = True
    c.Store_csv = True
    c.Pandas=True
    c.Output =output_path
    twint.run.Search(c)   
    #tweets = twint.output.tweets_object
    #print(len(tweets)) 
    tweets = twint.storage.panda.Tweets_df
    
    return tweets
