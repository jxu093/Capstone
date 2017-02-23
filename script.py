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


oauth_consumer_key="oYAHgmB6rp38N0FbkgiUrUEMU"
oauth_consumer_secret="7TwDhGihkbYj0N1IzjncURQIXf4RfnLjyOzMiJP095zfnxT6Zq"
oauth_access_token="493633798-Gr6DW1HSZP5Sqz4IJ5HPGmFxDJQ9zqm2qHgyhnVC"
oauth_access_secret="6t5TT1kDSs8nuTHC3zC9nzSMY0c8vK5GPdLUPvIAgxGQg"

watson_key = "ef7f17d18f551bcb1ffa88902dbd3116f065d02e"
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
        # strip emojis for compatibility with Watson
        filtered_text = myre.sub('',item['text'])

        analysis = {'_id': item['id'], 'tweet': filtered_text, 'user' : item['user']['screen_name'],
                    'followers': item['user']['followers_count']}

        # print item['user']['screen_name'], item['id_str']
        try:
            sentiment = alchemy_language.sentiment(text=filtered_text)
        except WatsonException as e:
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


