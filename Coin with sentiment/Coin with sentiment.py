import tweepy
from tweepy import Stream
from tweepy import StreamListener
import json
from textblob import TextBlob
import re
import csv
# import nltk
# nltk.download('punkt')

with open('../apiKeys.json', 'r') as f:
    key_data = json.load(f)

consumer_key = key_data["consumer_key"]
consumer_secret = key_data["consumer_secret"]
access_token = key_data["access_token"]
access_token_secret = key_data["access_token_secret"]

btc = 0
eth = 0

# .CSV파일 생성
header_name = ['Bitcoin', 'Ethereum']
with open('Coin Sentiment.csv', 'w') as file:
    writer = csv.DictWriter(file, fieldnames = header_name)
    writer.writeheader()


class Listener(StreamListener):
    def on_data(self, data):
        raw_twitts = json.loads(data)
        # print(raw_twitts) #뭐뭐 나오는지 체크 가능.
        try:

            tweets = raw_twitts['text']

            if("RT @" in tweets):
                print("RT임.")
            else:
                print("RT아님.")

            print("created_at은 " + raw_twitts['created_at'])

            # RT 제거, link 제거, 모든 이모지 제거
            tweets = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweets).split())
            tweets = ' '.join(re.sub('RT', ' ', tweets).split())

            blob = TextBlob(tweets.strip())

            # 함수 안에서 전역변수 사용을 명시
            global btc
            global eth

            btc_sentiment = 0
            eth_sentiment = 0

            # 감정 분석
            for sent in blob.sentences:
                if "Bitcoin" in sent and ("Ethereum" not in sent and "ETH" not in sent):
                    btc_sentiment = btc_sentiment + sent.sentiment.polarity
                elif "BTC" in sent and ("Ethereum" not in sent and "ETH" not in sent):
                    btc_sentiment = btc_sentiment + sent.sentiment.polarity
                elif "Ethereum" in sent and ("Bitcoin" not in sent and "BTC" not in sent):
                    eth_sentiment = eth_sentiment + sent.sentiment.polarity
                elif "ETH" in sent and ("Bitcoin" not in sent and "BTC" not in sent):
                    eth_sentiment = eth_sentiment + sent.sentiment.polarity

            btc = btc + btc_sentiment
            eth = eth + eth_sentiment

            with open('Coin Sentiment.csv', 'a') as file:
                writer = csv.DictWriter(file, fieldnames=header_name)
                info = {
                    'Bitcoin' : btc,
                    'Ethereum' : eth
                }
                writer.writerow(info)

            print(tweets)
            print("######################################################################################################################################")
        except:
            print('Error got')

    def on_error(self, status) :
        print(status)

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

twitter_stream = Stream(auth, Listener())
twitter_stream.filter(track = ['Bitcoin', 'BTC', 'Ethereum', 'ETH']) #검색하는 키워드