from pymongo import MongoClient
import os

mongo_user = os.environ['mongo_user']
mongo_pass = os.environ['mongo_pass']
mongo_address = os.environ['mongo_address']
mongo_port = os.environ['mongo_port']
mongo_dbname = os.environ['mongo_dbname']

client = MongoClient('mongodb://' + mongo_user + ':' + mongo_pass + '@' + mongo_address + ':' + mongo_port)
db = client[mongo_dbname]


def save_tweets(data, collection):
    for tweet_list in data:
        subject = tweet_list['subject']
        date = tweet_list['date']
        existing_data = db[collection].find({'subject': subject, 'date': date})
        # check if data doesn't already exist for this subject on this date
        if existing_data.count() == 0:
            db[collection].insert(tweet_list)
        else:  # error?
            pass


def get_tweets(subjects, collection):
    results_list = []
    for s in subjects:
        # get latest result for this subject
        res = db[collection].find({'subject': s}).sort('date', -1).limit(1)
        if res.count() == 0:
            res = None
        else:
            res = res[0]
            res['_id'] = None
        results_list.append(res)
    return results_list

