import twint
import schedule
import time

def DiyanetJob():
	c = twint.Config()
	c.Username = 'DiyanetTV'
	c.Search="15 temmuz"
	c.Since = "2016-3-3"
	c.Limit = 5000
	c.Store_object = True
	c.Store_csv = True
	c.Custom = ["date", "time", "username", "tweet", "link", "likes", "retweets", "replies", "mentions", "hashtags"]
	c.Output = "temmuz.csv"
	twint.run.Search(c)
	tweets = twint.output.tweets_list

# you can change the name of each "job" after "def" if you'd like.
def jobone():
	print ("Fetching Tweets")
	c = twint.Config()
	# choose username (optional)
	c.Username = "DiyanetTV"
	# choose search term (optional)
	c.Search = "namaz"
	# choose beginning time (narrow results)
	c.Since = "2018-01-01"
	# set limit on total tweets
	c.Limit = 1000
	# no idea, but makes the csv format properly
	c.Store_csv = True
	# format of the csv
	c.Custom = ["date", "time", "username", "tweet", "link", "likes", "retweets", "replies", "mentions", "hashtags"]
	# change the name of the csv file
	c.Output = "namaz.csv"
	twint.run.Search(c)

def jobtwo():
	print ("DiyanetTV")
	c = twint.Config()
	# choose username (optional)
	c.Username = "DiyanetTV"
	# choose search term (optional)
	c.Search = "15 Temmuz"
	# choose beginning time (narrow results)
	c.Since = "2018-01-01"
	# set limit on total tweets
	c.Limit = 1000
	# no idea, but makes the csv format properly
	c.Store_csv = True
	# format of the csv
	c.Custom = ["date", "time", "username", "tweet", "link", "likes", "retweets", "replies", "mentions", "hashtags"]
	# change the name of the csv file
	c.Output = "Temmuz.csv"
	twint.run.Search(c)

# run once when you start the program

DiyanetJob()

# run every minute(s), hour, day at, day of the week, day of the week and time. Use "#" to block out which ones you don't want to use.  Remove it to active. Also, replace "jobone" and "jobtwo" with your new function names (if applicable)

# schedule.every(1).minutes.do(jobone)
schedule.every(5).minutes.do(DiyanetJob)
# schedule.every().day.at("10:30").do(jobone)
# schedule.every().monday.do(jobone)
# schedule.every().wednesday.at("13:15").do(jobone)

# schedule.every(1).minutes.do(jobtwo)
# schedule.every().day.at("16:15").do(jobtwo)
# schedule.every().day.at("10:30").do(jobtwo)
# schedule.every().monday.do(jobtwo)
# schedule.every().wednesday.at("13:15").do(jobtwo)

while True:
  schedule.run_pending()
  time.sleep(1)