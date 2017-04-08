from pymongo import MongoClient

# try to import database server info from config file if it exists
# otherwise load from environment variables
try:
    import config_file
    mongo_user = config_file.mongo_configs['mongo_user']
    mongo_pass = config_file.mongo_configs['mongo_pass']
    mongo_address = config_file.mongo_configs['mongo_address']
    mongo_port = config_file.mongo_configs['mongo_port']
    mongo_dbname = config_file.mongo_configs['mongo_dbname']
except ImportError:
    import os
    mongo_user = os.environ['mongo_user']
    mongo_pass = os.environ['mongo_pass']
    mongo_address = os.environ['mongo_address']
    mongo_port = os.environ['mongo_port']
    mongo_dbname = os.environ['mongo_dbname']


client = MongoClient('mongodb://' + mongo_user + ':' + mongo_pass + '@' + mongo_address + ':' + mongo_port + '/' + mongo_dbname)
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


# save new data for custom topic
def save_custom_data(data, username):
    data['username'] = username
    db['customdata'].insert(data)


# load saved data for custom topic
def get_custom_data(username):
    results_list = []
    res = db['customdata'].find({'username': username}).sort('date', -1)
    # filter for one result per subject
    if res.count() == 0:
        res = None
    else:
        topic_set = set([])
        for r in res:
            if r['subject'] not in topic_set:
                topic_set.add(r['subject'])
                results_list.append(r)
    return results_list


# save new user to database
def create_user(user):
    existing_user = db['users'].find({'username': user['username']})
    if existing_user.count() == 0:
        db['users'].insert(user)
        return 'user created'
    else:
        return 'user already exists'


# load existing user
def get_user(username):
    res = db['users'].find({'username': username})
    if res.count() == 0:
        res = None
    else:
        res = res[0]
    return res
