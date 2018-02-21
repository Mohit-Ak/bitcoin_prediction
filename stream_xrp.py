#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from textblob import TextBlob
import tweepy
import re 
import json
import datetime
import traceback
import sys 

import argparse

parser = argparse.ArgumentParser()

parser.add_argument("outputfile", nargs='?', default="tweets_xrp_final.json")
parser.add_argument("errorfile", nargs='?', default="tweets_xrp_error_final.txt")


args = parser.parse_args()

#Variables that contains the user credentials to access Twitter API 
access_token = "773354492196687872-1e1rvhhcvZPPmY9sW04hpusDX7LUAKv"
access_token_secret = "MqlZaIFnoR0tapkeu5YGYLK8Rnw4vnotyuOVyMwMM6HAe"
consumer_key = "h3W8XRBVvD0D8Xm0rokfPctOo"
consumer_secret = "koGrQ4o45BUQZO4TM9Xpl55xG2biWFlx6t3TODfQjOwp1htjzJ"
tweet_count = 0
i = 1

class Tweet:
    def __init__(self, text, retweet_count, sentiment_text, polarity, created_at):
        self.text = text
        self.retweet_count = retweet_count
        self.sentiment_text = sentiment_text
        self.polarity = polarity
        self.created_at = created_at

    def __str__(self):
        return 'Sentiment: {} {} \nText: {}\nCreated_At: {}\n'.format(self.sentiment_text, self.polarity, self.text, self.created_at)

class MyStreamListener(tweepy.StreamListener):

	def __init__(self):
		self.mylist = []

	def on_data(self, data):
		tweet = json.loads(data)
		try:
			if 'retweeted_status' in tweet:
				if 'extended_tweet' in tweet['retweeted_status']:
					tweet_text = tweet['retweeted_status']['extended_tweet']['full_text']
				else:
					tweet_text = tweet['retweeted_status']['text']
			else:
				if 'extended_tweet' in tweet:
					tweet_text = tweet['extended_tweet']['full_text']
				else:
					tweet_text = tweet['text']
			count = tweet['retweet_count']
			tweet_sentiment, polarity = self.get_tweet_sentiment(tweet_text)     
			'''if str(tweet['user']['verified']) == str("False"):
				print("no")'''
			newTweetObj = Tweet(text=tweet_text, 
								retweet_count = count,
                                sentiment_text=tweet_sentiment, 
                                polarity=polarity, 
                                created_at= datetime.datetime.strptime(tweet['created_at'],'%a %b %d %H:%M:%S %z %Y').strftime('%Y-%m-%d-%H-%M-%S'))
			global tweet_count 
			global i
			tweet_count = tweet_count + 1
			if tweet_count > 10000:
				tweet_count = 0
				i = i + 1

			with open(str(i)+"_"+args.outputfile, mode='a') as file:
				file.write('{},\n'.format(json.dumps(newTweetObj.__dict__)))     
		except:
			exc_type, exc_value, exc_traceback = sys.exc_info()            
			with open(args.errorfile, mode='a') as file:
				file.write('Error: {}\n\nTweet Info: {}\n--------------------------\n'.format(repr(traceback.format_tb(exc_traceback)), tweet))            

		return True

	def on_error(self, status_code):
		if status_code == 420:
			return False
	def clean_tweet(self, tweet):
		return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())

	def get_tweet_sentiment(self, tweet):
		analysis = TextBlob(self.clean_tweet(tweet))

        # set sentiment
		sentiment = None 
		if analysis.sentiment.polarity > 0:
			sentiment = 'positive'
		elif analysis.sentiment.polarity == 0:
			sentiment = 'neutral'
		else:
			sentiment = 'negative'
		return sentiment, analysis.sentiment.polarity


if __name__ == "__main__":
	mylistener = MyStreamListener()
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	myStream = tweepy.Stream(auth,mylistener)
	myStream.filter(track=['ripple','XRP','$XRP'],async=True)






