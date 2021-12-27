import tweepy
import config

auth = tweepy.AppAuthHandler(
    config.TWITTER_CONSUMER_KEY, config.TWITTER_CONSUMER_SECRET
)
# auth.set_access_token(config.TWITTER_ACCESS_TOKEN, config.TWITTER_ACCESS_TOKEN_SECRET)
# api = tweepy.API(auth)


# for tweet in tweepy.Cursor(api.search_tweets, q="tatasteel").items(10):
#     print(tweet.text)


sess = tweepy.Client(
    config.BEARER_TOKEN,
    config.TWITTER_CONSUMER_KEY,
    config.TWITTER_CONSUMER_SECRET,
    config.TWITTER_ACCESS_TOKEN,
    config.TWITTER_ACCESS_TOKEN_SECRET,
)

tweets = sess.search_recent_tweets("tatasteel")

print(tweets)
