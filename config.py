import re
import quandl
import tweepy

class API:

    def __init__(self):
        pass

    @staticmethod
    def news_api(symbol, qs='&start=0&num=2000'):
        return 'http://www.google.com/finance/company_news?output=json&q=' \
               + symbol + qs

    @staticmethod
    def sentiment_api(symbol):
        return quandl.get('NS1/' + symbol + '_US', authtoken='YdMDrWCtysnDHxyUUyXa')

    @staticmethod
    def tweet_api(topic, start, until):
        consumer_key = 'wY2hSQ1eB4MGPcqryo1gtdHOj'
        consumer_secret = 'POMGrCy9Yi8ku9SxzkP712X04JrFuHWl8KSfaTRZKZ8Wnuwali'
        access_token = '2738088724-KDez4xiSfZ6syHvbv85AxpG5U3SQJucV00vWaws'
        access_token_secret = '8Bpij2lmkMdhyvCl2ic41LPJWuMFbkxUr9SP1ZghCRkrh'
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        #fetched_tweets = api.search(q=topic, rpp=100, lang="en")
        fetched_tweets = tweepy.Cursor(api.search, q=topic, rpp=100, result_type="recent",
                                       include_entities=True, lang="en", since=start, until=until).pages()
        return fetched_tweets

    @staticmethod
    def clean_tweet(tweet):
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
