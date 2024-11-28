from pymongo import MongoClient



client = MongoClient("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")


db = client["tiny_tweets_db"]

collection_name = db["User_app"]