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

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

def get_last_day(query):
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
            response['positive']['tweets'].append(obj)
        elif resp.document_sentiment.score < -0.25:
            response['negative']['tweets'].append(obj)
        else:
            response['neutral']['tweets'].append(obj)

@app.route('/query', methods=['GET'])
def query():
    q = request.args.get('q')
    get_last_day(q)
    return jsonify({"response":response})

@app.route('/test', methods=['GET'])
def test():
    response={"test":"test"}
    return jsonify({"response":response})


if __name__ == '__main__':
    app.run(debug=True)
