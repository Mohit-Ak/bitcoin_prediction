import sys
import jsonpickle
import os
import tweepy

access_token = "773354492196687872-rWx1dJ6gdAfASqMoZOZIEFIN0iG0tCj"
access_token_secret = "Yxfp9rDc7Tz0ZuNBsnx6n3UWBTziC4Vr13eMxVIfQ7sa1"
consumer_key = "nrREUFBvtdZEoh6bkcPhpb7Yi"
consumer_secret = "BzkO2jYTeGWjpYoFRLpD22Yfsns694x7GsaLk2urrdYGnmdXMT"

auth = tweepy.AppAuthHandler(consumer_key,consumer_secret)
 
api = tweepy.API(auth, wait_on_rate_limit=True,wait_on_rate_limit_notify=True)

if (not api):
    print ("Can't Authenticate")
    sys.exit(-1)

searchQuery = 'bitcoin OR BTC'  # this is what we're searching for
maxTweets = 10000000000000000000 # Some arbitrary large number
tweetsPerQry = 100  # this is the max the API permits
fName = 'tweets_search.txt' 
sinceId = None

max_id = 1000000000000000000000

class Tweet:
    def __init__(self, text, retweet_count, sentiment_text, polarity, created_at):
        self.text = text
        self.retweet_count = retweet_count
        self.sentiment_text = sentiment_text
        self.polarity = polarity
        self.created_at = created_at

    def __str__(self):
        return 'Sentiment: {} {} \nText: {}\nCreated_At: {}\n'.format(self.sentiment_text, self.polarity, self.text, self.created_at)

tweetCount = 0
print("Downloading max {0} tweets".format(maxTweets))

with open(fName, 'w') as f:
    while tweetCount < maxTweets:
        try:
            if (max_id <= 0):
                if (not sinceId):
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry)
                else:
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            since_id=sinceId)
            else:
                if (not sinceId):
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            max_id=str(max_id - 1))
                else:
                    new_tweets = api.search(q=searchQuery, count=tweetsPerQry,
                                            max_id=str(max_id - 1),
                                            since_id=sinceId)
            if not new_tweets:
                print("No more tweets found")
                break
            for tweet in new_tweets:
            	current_tweet = tweet._json
            	print(current_tweet)
            	#current_tweet = print(tweet._json['created_at'])
            	f.write(jsonpickle.encode(tweet._json, unpicklable=False) + '\n')
            tweetCount += len(new_tweets)
            print("Downloaded {0} tweets".format(tweetCount))
            max_id = new_tweets[-1].id
        except tweepy.TweepError as e:

            print("some error : " + str(e))
            break

print ("Downloaded {0} tweets, Saved to {1}".format(tweetCount, fName))