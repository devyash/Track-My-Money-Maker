#!flask/bin/python
from flask import Flask, jsonify, request
from tweepy import OAuthHandler
import tweepy
import json
import re
from google.cloud import language_v1
from flask_cors import CORS
client = language_v1.LanguageServiceClient()

app = Flask(__name__)
CORS(app)

response = {
    "negative": 0,
    "neutral" : 0,
    "positive": 0
}

response2 = {
    "negative": {
      "size": "4",
      "tweets": []
    },
    "neutral": {
      "Size": "4",
      "tweets": []
    },
    "positive": {
      "size": "4",
      "tweets": []
    }
}

def filter_tweet(tweet):
    tweet = tweet.lower()
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))','URL',tweet)
    tweet = re.sub('@[^\s]+','AT_USER',tweet)
    tweet = re.sub('[\s]+', ' ', tweet)
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)
    tweet = tweet.strip('\'"')
    return tweet

access_token = "911600836077391872-kH7wUlhuCdUIqTvov3ha4ZRCCl8wb2u"
access_token_secret = "ih15H1CqTZPJLZ6Lm9ccoSrEi9GS6CXFdHEg7lI689e4C"
consumer_key = "anVP2vNleAyYWwVg5f1lW5zEV"
consumer_secret = "tEdg4nwZS0AQd2hDfwrhLHW2ySoH9xvh18VzFAG6Y9xUbpaLve"

# access_token = "111305796-lEpRQbd49BBVlzBJsn0usVT9cUkF4wZ6xJGABIqa"
# access_token_secret = "RQjR6LS1zjhHp7NWnuokeLhlccG7AFSd6PB34rYksYHs0"
# consumer_key = "B6E7aFvsWte9WznfTZk5Lui2y"
# consumer_secret = "6PV6CI024k3lAmvmnUHbBTePXnSFjxiIQNYwwI9r3AwsOvs4SK"
# consumer_key = "8u72ob94y8D4lHh7vUz7Hmdch"
# consumer_secret = "NXEK09DZS1YMOD3l1DlR8lXkQEsbWsK8Iy4RRhGwrCqKvqCkYl"
# access_token = "111305796-g3TeJvvIJJkPMlhp4WJCgXErLqvqR0nYjHR3cE10"
# access_token_secret	= "rKTtvmUYlIg4D3SnNFrVoVVOYMUmDntQsHbKBUmnHbj2F"


auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
def get_last_day(query):
    r = 0
    for tweet in tweepy.Cursor(api.search,
                               q=query,
                               rpp=100,
                               result_type="recent",
                               include_entities=True,
                               lang="en").items():

        # print tweet.text
        url = "https://twitter.com/" + tweet.user.screen_name + "/status/" + tweet.id_str
        # print url
        # print tweet.created_at
        document = language_v1.types.Document(content=filter_tweet(tweet.text), type="PLAIN_TEXT")
        resp = client.analyze_sentiment(document = document, encoding_type='UTF32')
        # print resp.document_sentiment.score
        # print "\n\n\n\n"
        obj = {
          "text": tweet.text,
          "url": url,
          "score": resp.document_sentiment.score,
          "timestamp": tweet.created_at
        }
        if resp.document_sentiment.score > 0.25:
            response2['positive']['tweets'].append(obj)
        elif resp.document_sentiment.score < -0.25:
            response2['negative']['tweets'].append(obj)
        else:
            response2['neutral']['tweets'].append(obj)
	r += 1
	if r > 500:
		break

def get_last(query):
    i = 0
    e = ""
    cnt = 50
    r = 0
    for tweet in tweepy.Cursor(api.search,
                               q=query,
                               rpp=100,
                               result_type="recent",
                               include_entities=True,
                               lang="en").items():
        url = "https://twitter.com/" + tweet.user.screen_name + "/status/" + tweet.id_str
	if i == cnt:
        	document = language_v1.types.Document(content=filter_tweet(e), type="PLAIN_TEXT")
        	resp = client.analyze_sentiment(document = document, encoding_type='UTF32')
		e = ""
		print resp.document_sentiment.score
        	if resp.document_sentiment.score > 0.1:
            		response['positive'] += i
        	elif resp.document_sentiment.score < -0.1:
            		response['negative'] += i
        	else:
            		response['neutral'] += i
		i = 0
	e += tweet.text + " "
	i += 1
	r += 1
	if r > 500:
		break

    document = language_v1.types.Document(content=filter_tweet(e), type="PLAIN_TEXT")
    resp = client.analyze_sentiment(document = document, encoding_type='UTF32')
    e = ""
    print resp.document_sentiment.score
    if resp.document_sentiment.score > 0.1:
    	response['positive'] += i
    elif resp.document_sentiment.score < -0.1:
     	response['negative'] += i
    else:
    	response['neutral'] += i
    i = 0



@app.route('/query', methods=['GET'])
def query():
    print "query hit"
    q = request.args.get('q')
    get_last(q)
    return jsonify({"response":response})

@app.route('/q', methods=['GET'])
def test():
    print "q hit"
    q = request.args.get('q')
    get_last_day(q)
    return jsonify({"response":response2})


if __name__ == '__main__':
    app.run(debug=True)
