# mongo "mongodb+srv://smashtweets-kyzoq.mongodb.net/test" --username a
# use SmashTweets
# db.Tweets.aggregate([ { $match: {} }, { $out: "TweetsCopy" } ])

import tweepy
import pymongo
import keys

auth = tweepy.OAuthHandler(keys.consumer_key, keys.consumer_secret)
auth.set_access_token(keys.access_token, keys.access_token_secret)

api = tweepy.API(auth)

client = pymongo.MongoClient("mongodb+srv://a:" + keys.passw + "@smashtweets-kyzoq.mongodb.net/test?retryWrites=true")
db = client["SmashTweets"]
col = db["TweetsCopy"]
x = 1

for doc in col.find():

    print(x)
    x = x+1

    try:
        status = api.get_status(doc["Tweet ID"])

        col.update_one({'_id': doc['_id']}, {"$set": {
            "Retweets": status.retweet_count,
            "Favorites": status.favorite_count,
            }})
    except Exception:
        print("Deleted tweet with ID: " + doc["Tweet ID"])
        pass
