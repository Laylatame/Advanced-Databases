#!/usr/bin/python

import tweepy
import pymongo
import json
import keys

#override tweepy.StreamListener
class MyStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        client = pymongo.MongoClient("mongodb+srv://a:" + keys.passw + "@smashtweets-kyzoq.mongodb.net/test?retryWrites=true")
        db = client["SmashTweets"]
        col = db["TweetsComplete"]

        col.insert_one(status._json)
        print ("Added tweet")

    def on_error(self, status):
        print(status)

auth = tweepy.OAuthHandler(keys.consumer_key, keys.consumer_secret)
auth.set_access_token(keys.access_token, keys.access_token_secret)

api = tweepy.API(auth)

# print("auth")

myStream = tweepy.Stream(auth = api.auth, listener = MyStreamListener())
myStream.filter(track=['smash ultimate joker', 'smash ultimate update', 'smash ultimate', 'SSBU'])
# myStream.filter(follow=["1121162847810199553"])