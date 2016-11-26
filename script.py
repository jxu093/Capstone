import requests
from requests_oauthlib import OAuth1
from watson_developer_cloud import AlchemyLanguageV1
from operator import itemgetter


oauth_consumer_key="oYAHgmB6rp38N0FbkgiUrUEMU"
oauth_consumer_secret="7TwDhGihkbYj0N1IzjncURQIXf4RfnLjyOzMiJP095zfnxT6Zq"
oauth_access_token="493633798-Gr6DW1HSZP5Sqz4IJ5HPGmFxDJQ9zqm2qHgyhnVC"
oauth_access_secret="6t5TT1kDSs8nuTHC3zC9nzSMY0c8vK5GPdLUPvIAgxGQg"

watson_key = "41a26a160fde86a9a545f8aac84a8b494da69000"
alchemy_language = AlchemyLanguageV1(api_key=watson_key)


def get_oauth():
    oauth = OAuth1(oauth_consumer_key,
                   client_secret=oauth_consumer_secret,
                   resource_owner_key=oauth_access_token,
                   resource_owner_secret=oauth_access_secret)
    return oauth


universities = ["mcmaster university"]
university_data = []


def get_data():
    if len(university_data) == 0:
        for u in universities:
            university_data.append(twit_search(u))

    return university_data


def twit_search(query):
    url = 'https://api.twitter.com/1.1/search/tweets.json?q='+query
    oauth = get_oauth()
    json_obj = requests.get(url, params={'count':100, 'lang': 'en'}, auth=oauth)
    data = json_obj.json()

    tweet_list = {'positive': [], 'negative': [], 'neutralCount': 0, 'score': 0}

    for item in data['statuses']:
        analysis = {'tweet': item['text'], 'user' : item['user']['screen_name'],
                    'followers': item['user']['followers_count']}

        # print item['user']['screen_name'], item['id_str']
        sentiment = alchemy_language.sentiment(text=item['text'])
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


