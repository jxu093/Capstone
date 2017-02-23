from pymongo import MongoClient

client = MongoClient('localhost', 27017)
db = client.capstone_db


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

