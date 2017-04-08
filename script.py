import requests
from requests_oauthlib import OAuth1
from watson_developer_cloud import AlchemyLanguageV1, WatsonException
from operator import itemgetter
import re
import datetime


# regex for emojis
myre = re.compile(u'('
    u'\ud83c[\udf00-\udfff]|'
    u'\ud83d[\udc00-\ude4f\ude80-\udeff]|'
    u'[\u2600-\u26FF\u2700-\u27BF])+',
    re.UNICODE)


try:
    import config_file
    oauth_consumer_key = config_file.oauth_consumer_key
    oauth_consumer_secret = config_file.oauth_consumer_secret
    oauth_access_token = config_file.oauth_access_token
    oauth_access_secret = config_file.oauth_access_secret
    watson_key = config_file.watson_key
except ImportError:
    import os
    oauth_consumer_key = os.environ['oauth_consumer_key']
    oauth_consumer_secret = os.environ['oauth_consumer_secret']
    oauth_access_token = os.environ['oauth_access_token']
    oauth_access_secret = os.environ['oauth_access_secret']
    watson_key = os.environ['watson_key']


alchemy_language = AlchemyLanguageV1(api_key=watson_key)


def get_oauth():
    oauth = OAuth1(oauth_consumer_key,
                   client_secret=oauth_consumer_secret,
                   resource_owner_key=oauth_access_token,
                   resource_owner_secret=oauth_access_secret)
    return oauth


return_data = []


def get_data(subjects):
    if len(return_data) == 0:
        for s in subjects:
            return_data.append(twit_search(s))

    return return_data


def twit_search(query):
    url = 'https://api.twitter.com/1.1/search/tweets.json?q=' + requests.utils.quote(query)
    oauth = get_oauth()
    json_obj = requests.get(url, params={'count':100, 'lang': 'en'}, auth=oauth)
    data = json_obj.json()

    tweet_list = {'subject': query, 'positive': [], 'negative': [], 'neutralCount': 0, 'score': 0,
                  '_id': query + str(datetime.date.today()), 'date' : datetime.date.today().isoformat()}

    for item in data['statuses']:
        # strip emojis for compatibility with Watson and Ascii
        filtered_text = myre.sub('',item['text']).encode('ascii', 'ignore')

        analysis = {'_id': item['id'], 'tweet': filtered_text, 'user' : item['user']['screen_name'],
                    'followers': item['user']['followers_count']}
        # print item['user']['screen_name'], item['id_str']

        try:
            # Send to Watson
            sentiment = alchemy_language.sentiment(text=filtered_text)
        except WatsonException as e:
            # Watson error, print to stdout and move on to next tweet
            print e
            print "tweet: " + item['text']
        if sentiment['status'] == "OK":
            analysis['sentiment'] = sentiment['docSentiment']['type']
            if analysis['sentiment'] == "neutral":
                tweet_list['neutralCount'] += 1
            else:
                analysis['score'] = sentiment['docSentiment']['score']
                tweet_list[analysis['sentiment']].append(analysis)
                tweet_list['score'] += float(sentiment['docSentiment']['score'])

    # for i in range(0, len(tweet_list)):
    #     print tweet_list[i]
    #     print '\n'

    print 'Resulting score: ' + str(tweet_list['score']) + ', ' + str(len(tweet_list['positive'])) + \
          ' positive comments, ' + str(len(tweet_list['negative'])) + ' negative comments, ' + \
          str(tweet_list['neutralCount']) + ' neutral'

    # sort by followers
    tweet_list['positive'].sort(key=itemgetter('followers'), reverse=True)
    tweet_list['negative'].sort(key=itemgetter('followers'), reverse=True)

    return tweet_list


