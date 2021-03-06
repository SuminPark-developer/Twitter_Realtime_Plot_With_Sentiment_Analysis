import tweepy
from tweepy import Stream
from tweepy import StreamListener
import json
import datetime
from datetime import timedelta
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

btc_original = 0
btc_RT = 0
total_tweet = 0

# .CSV파일 생성
header_name = ['Create_Time', 'Bitcoin_Original', 'Bitcoin_RT', 'Total_Tweet']
with open('tweet data.csv', 'w') as file:
    csv_writer = csv.DictWriter(file, fieldnames = header_name)
    csv_writer.writeheader()

class Listener(StreamListener):
    def on_data(self, data):
        raw_twitts = json.loads(data)
        # print(raw_twitts) #뭐뭐 나오는지 체크 가능.
        try:

            tweets = raw_twitts['text']

            print("created_at은 " + raw_twitts['created_at'])
            # 문자열로 되어 있는 시간을 Datetime 객체로 변경 - https://brownbears.tistory.com/432
            date_time_str = raw_twitts['created_at']
            date_time_obj = datetime.datetime.strptime(date_time_str, '%a %B %d %H:%M:%S +0000 %Y')
            print('Date-time: ', date_time_obj)

            # https://yuddomack.tistory.com/entry/%ED%8C%8C%EC%9D%B4%EC%8D%AC-datetime-%EB%82%A0%EC%A7%9C-%EA%B3%84%EC%82%B0
            date_time_obj = date_time_obj + timedelta(seconds=10)

            # 함수 안에서 전역변수 사용을 명시
            global btc_original
            global btc_RT
            global total_tweet

            btc_count = 0
            btc_RT_count = 0

            if ("RT @" in tweets):
                print("RT임.")
                btc_RT_count = btc_RT_count + 1
            else:
                print("RT아님.")
                btc_count = btc_count + 1

            btc_original = btc_original + btc_count
            btc_RT = btc_RT + btc_RT_count
            total_tweet = btc_original + btc_RT

            with open('tweet data.csv', 'a') as file:
                csv_writer = csv.DictWriter(file, fieldnames=header_name)
                info = {
                    'Create_Time' : date_time_obj,
                    'Bitcoin_Original' : btc_original,
                    'Bitcoin_RT' : btc_RT,
                    'Total_Tweet' : total_tweet
                }
                csv_writer.writerow(info)

            # RT 제거, link 제거, 모든 이모지 제거
            tweets = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweets).split())
            tweets = ' '.join(re.sub('RT', ' ', tweets).split())

            print(date_time_obj, btc_original, btc_RT, total_tweet)
            print(tweets)
            print("######################################################################################################################################")
        except:
            print('Error got')

    def on_error(self, status) :
        print(status)

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

twitter_stream = Stream(auth, Listener())
twitter_stream.filter(track = ['Bitcoin', 'BTC']) #검색하는 키워드