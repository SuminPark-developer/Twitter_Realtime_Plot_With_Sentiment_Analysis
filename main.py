import json
from textblob import TextBlob
import tweepy
import sys

with open('../apiKeys.json', 'r') as f:
    key_data = json.load(f)

consumer_key = key_data["consumer_key"]
consumer_secret = key_data["consumer_secret"]
access_token = key_data["access_token"]
access_token_secret = key_data["access_token_secret"]

auth_handler = tweepy.OAuthHandler(consumer_key=api_key, consumer_secret=api_secret_key)
auth_handler.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth_handler)

search_term = 'BTC' # tweepy multiple keywords - https://stackoverflow.com/questions/42384305/tweepy-cursor-multiple-or-logic-function-for-query-terms
tweet_amount = 50

tweets = tweepy.Cursor(api.search, q=search_term, lang='en').items(tweet_amount)

polarity = 0

positive = 0
neutral = 0
negative = 0

for tweet in tweets:
    print("###########################")
    # print(tweet)
    # print(tweet.text)
    final_text = tweet.text.replace('RT', '')
    if final_text.startswith(' @'):
        position = final_text.index(':')
        final_text = final_text[position+2:]
    if final_text.startswith('@'):
        position = final_text.index(' ')
        final_text = final_text[position+2:]

    analysis = TextBlob(final_text)
    tweet_polarity = analysis.polarity

    if tweet_polarity > 0.00:
        positive += 1
    elif tweet_polarity < 0.00:
        negative += 1
    elif tweet_polarity == 0.00:
        neutral += 1
    polarity += tweet_polarity
    print(final_text)

print(polarity)
print(f'Amount of positive tweets: {positive}')
print(f'Amount of negative tweets: {negative}')
print(f'Amount of neutral tweets: {neutral}')