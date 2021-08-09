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
    replies = twint.Config()
    replies.Since = bas_tarih
    replies.Until = bit_tarih
    replies.Hide_output=True
    replies.Pandas = True
    replies.To = "@"+to
    replies.Store_object = True
    replies.Store_csv = True
    replies.Pandas=True
    replies.Output = DATA_PATH+"\Replies {} {}_{}.csv".format(to, bas_tarih, bit_tarih)
    twint.run.Search(replies)
    df = twint.storage.panda.Tweets_df
    return df

def get_tweets(bas_tarih, bit_tarih, username):
    nest_asyncio.apply()
    tweets=[]
    c = twint.Config()
    c.Username = username
    c.Since = bas_tarih
    c.Until = bit_tarih
    c.Store_object = True
    c.Store_csv = True
    c.Pandas=True
    c.Output = DATA_PATH+"{} {}_{}.csv".format(username, bas_tarih, bit_tarih)
    c.Hide_output=True
    twint.run.Search(c)
    tweets = twint.output.tweets_list
    return tweets

def get_hello():
    return "hi"