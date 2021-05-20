import tweepy
from tweepy import Stream
from tweepy import StreamListener
import json
from textblob import TextBlob
import re
import csv
import pickle
import pandas as pd

# import nltk
# nltk.download('punkt')

with open('../apiKeys.json', 'r') as f:
    key_data = json.load(f)

consumer_key = key_data["consumer_key"]
consumer_secret = key_data["consumer_secret"]
access_token = key_data["access_token"]
access_token_secret = key_data["access_token_secret"]

time = 0
btc_original = 0
btc_RT = 0
total_tweet = 0

# .CSV파일 생성
header_name = ['Time', 'Bitcoin_Original', 'Bitcoin_RT', 'Total_Tweet']
with open('All Tweets.csv', 'w') as file:
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

            # 함수 안에서 전역변수 사용을 명시
            global time
            global btc_original
            global btc_RT
            global total_tweet

            btc_count = 0
            btc_RT_count = 0

            if ("RT @" in tweets):
                btc_RT_count = btc_RT_count + 1
            else:
                btc_count = btc_count + 1

            time = raw_twitts['created_at']
            btc_original = btc_original + btc_count
            btc_RT = btc_RT + btc_RT_count
            total_tweet = btc_original + btc_RT

            with open('All Tweets.csv', 'a') as file:
                writer = csv.DictWriter(file, fieldnames=header_name)
                info = {
                    'Time' : time,
                    'Bitcoin_Original' : btc_original,
                    'Bitcoin_RT' : btc_RT,
                    'Total_Tweet' : total_tweet
                }
                writer.writerow(info)

            # RT 제거, link 제거, 모든 이모지 제거
            tweets = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweets).split())
            tweets = ' '.join(re.sub('RT', ' ', tweets).split())

            print(tweets)
            # csv 파일을 읽어다가 Pandas의 기본 데이터구조인 DataFrame 으로 만들어줌. https://blog.naver.com/PostView.nhn?blogId=resumet&logNo=221449693886
            data = pd.read_csv("./All Tweets.csv")
            print(data)
            # pandas 데이터 프레임 pickle로 저장하기
            data.to_pickle("data.pickle")

            print("######################################################################################################################################")
        except:
            print('Error got')

    def on_error(self, status) :
        print(status)

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

twitter_stream = Stream(auth, Listener())
twitter_stream.filter(track = ['Bitcoin', 'BTC']) #검색하는 키워드