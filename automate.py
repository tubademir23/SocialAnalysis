import twint
import schedule
import time

<<<<<<< HEAD
=======
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

>>>>>>> 1e68c3156fde1b3e6c26ae01a504100ba59cdeec
# you can change the name of each "job" after "def" if you'd like.
def jobone():
	print ("Fetching Tweets")
	c = twint.Config()
	# choose username (optional)
<<<<<<< HEAD
	c.Username = "insert username here"
	# choose search term (optional)
	c.Search = "insert search term here"
=======
	c.Username = "DiyanetTV"
	# choose search term (optional)
	c.Search = "namaz"
>>>>>>> 1e68c3156fde1b3e6c26ae01a504100ba59cdeec
	# choose beginning time (narrow results)
	c.Since = "2018-01-01"
	# set limit on total tweets
	c.Limit = 1000
	# no idea, but makes the csv format properly
	c.Store_csv = True
	# format of the csv
	c.Custom = ["date", "time", "username", "tweet", "link", "likes", "retweets", "replies", "mentions", "hashtags"]
	# change the name of the csv file
<<<<<<< HEAD
	c.Output = "filename.csv"
	twint.run.Search(c)

def jobtwo():
	print ("Fetching Tweets")
	c = twint.Config()
	# choose username (optional)
	c.Username = "insert username here"
	# choose search term (optional)
	c.Search = "insert search term here"
=======
	c.Output = "namaz.csv"
	twint.run.Search(c)

def jobtwo():
	print ("DiyanetTV")
	c = twint.Config()
	# choose username (optional)
	c.Username = "DiyanetTV"
	# choose search term (optional)
	c.Search = "15 Temmuz"
>>>>>>> 1e68c3156fde1b3e6c26ae01a504100ba59cdeec
	# choose beginning time (narrow results)
	c.Since = "2018-01-01"
	# set limit on total tweets
	c.Limit = 1000
	# no idea, but makes the csv format properly
	c.Store_csv = True
	# format of the csv
	c.Custom = ["date", "time", "username", "tweet", "link", "likes", "retweets", "replies", "mentions", "hashtags"]
	# change the name of the csv file
<<<<<<< HEAD
	c.Output = "filename2.csv"
=======
	c.Output = "Temmuz.csv"
>>>>>>> 1e68c3156fde1b3e6c26ae01a504100ba59cdeec
	twint.run.Search(c)

# run once when you start the program

<<<<<<< HEAD
jobone()
jobtwo()
=======
DiyanetJob()
>>>>>>> 1e68c3156fde1b3e6c26ae01a504100ba59cdeec

# run every minute(s), hour, day at, day of the week, day of the week and time. Use "#" to block out which ones you don't want to use.  Remove it to active. Also, replace "jobone" and "jobtwo" with your new function names (if applicable)

# schedule.every(1).minutes.do(jobone)
<<<<<<< HEAD
schedule.every().hour.do(jobone)
=======
schedule.every(5).minutes.do(DiyanetJob)
>>>>>>> 1e68c3156fde1b3e6c26ae01a504100ba59cdeec
# schedule.every().day.at("10:30").do(jobone)
# schedule.every().monday.do(jobone)
# schedule.every().wednesday.at("13:15").do(jobone)

# schedule.every(1).minutes.do(jobtwo)
<<<<<<< HEAD
schedule.every().hour.do(jobtwo)
=======
# schedule.every().day.at("16:15").do(jobtwo)
>>>>>>> 1e68c3156fde1b3e6c26ae01a504100ba59cdeec
# schedule.every().day.at("10:30").do(jobtwo)
# schedule.every().monday.do(jobtwo)
# schedule.every().wednesday.at("13:15").do(jobtwo)

while True:
  schedule.run_pending()
  time.sleep(1)
