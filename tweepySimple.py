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
        col = db["Tweets"]

        tweet = {
            "Tweet ID": status.id_str,
            "Text": status.text,
            "Retweets": status.retweet_count,
            "Favorites": status.favorite_count,
            "Replies": status.reply_count,
            "Date": status.created_at,
            "Source": status.source,
            "Language": status.lang,
            "Location": status.coordinates,

            "User": {
                "Username": status.user.screen_name,
                "Followers": status.user.followers_count,
                "Verified": status.user.verified
            },

            "Hashtags": [x["text"] for x in status.entities["hashtags"]],
            "Media": True if "media" in status.entities else False
        }

        col.insert_one(tweet)
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