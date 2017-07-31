import time
import json
import demjson
import urllib2
from config import API
from datetime import datetime, timedelta
from collections import defaultdict


class FinanceAPI:

    def __init__(self, symbol, topic):
        self.topic = topic
        self.symbol = symbol

    def request_news(self):
        response = urllib2.urlopen(API.news_api(self.symbol))
        html = response.read()
        content = demjson.decode(html)
        article_list = []
        news_json = content['clusters']
        for cluster in news_json:
            for article in cluster:
                if article == 'a':
                    article_list.extend(cluster[article])
        return article_list

    def request_sentiment(self):
        sentiment = API.sentiment_api(self.symbol)
        return sentiment

    def request_tweet(self, ts):
        start = datetime.fromtimestamp(ts)
        until = start + timedelta(days=1)
        tweets = API.tweet_api(self.topic, start.date(), until.date())
        file = open("tweets.json", "wb")
        tweet_list = []
        for tweet in tweets:
            tweetTime = tweet[0].created_at
            tweetText = API.clean_tweet(tweet[0].text)
            tweetTS = time.mktime(tweetTime.timetuple())
            if not tweet[0].retweeted:
                tweet_content = {int(tweetTS): tweetText}
                tweet_list.append(tweet_content)
                json.dump(tweet_content, file)
                file.write("\n")
        file.close()
        return tweet_list
'''
for tweets in tweepy.Cursor(api.search,q=query,count=1,result_type="recent",include_entities=True,since=currentTime).pages():
    tweetTime = tweets[0].created_at # get the current time of the tweet
    now = datetime.datetime.now()
    interval = now - tweetTime # subtract tweetTime from currentTime
    if interval.seconds <= 3900: #get interval in seconds and use your time constraint in seconds (mine is 1hr and 5 mins = 3900secs)
        print tweets[0].text.encode('utf-8')
        print(tweets[0].created_at)
    else:
        shouldContinue = False
        print(interval.seconds)
        print(tweets[0].created_at)

    print('\n')

    if not shouldContinue: # check if tweet is still within time range. Tweet returned are ordered according to recent already.
        print('exiting the loop')
        break
        return tweet_list
'''

class DataProcess:

    def __init__(self, interval, period):
        self.interval = interval
        self.period = period
        self.date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    @staticmethod
    def get_ts(date):
        return int(time.mktime(date.timetuple()))

    def start(self):
        prev_date = self.date - timedelta(days=self.period)
        while prev_date.weekday() > 4:
            prev_date -= timedelta(days=1)
        start_time = prev_date + timedelta(hours=8)
        return start_time

    def effective_ts_list(self):
        next = self.start()
        time_list = [self.get_ts(next)]
        while next < datetime.now():
            next += timedelta(hours=self.interval)
            if 8 <= next.hour < 24 and next.weekday() <= 4:
                time_list.append(self.get_ts(next))
        return time_list


#news = FinanceAPI("AMZN", "amazon").request_tweet()
#print news
ts = DataProcess(interval=2, period=15).effective_ts_list()
print ts
news = FinanceAPI("AMZN", "amazon").request_tweet(ts[-15])
print news
