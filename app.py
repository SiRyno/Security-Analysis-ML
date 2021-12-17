import pandas as pd
import datetime as dt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas_datareader.data as web
import streamlit as st
from streamlit_echarts import st_echarts
import model as m
import tweepy
import config


auth = tweepy.OAuthHandler(config.TWITTER_CONSUMER_KEY, config.TWITTER_CONSUMER_SECRET)
# auth.set_access_token(config.TWITTER_ACCESS_TOKEN, config.TWITTER_ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

ticker = m.get_ticker()

st.title("Security Analysis")

option = st.sidebar.selectbox("Which Dashboard?", ("twitter", "chart"))
ticker = st.sidebar.selectbox(label="Stock", options=ticker)


st.header(option)


# user = api.get_user(username="traderstewie")
# tweets = api.search_tweets(q=ticker)
tweets = tweepy.Cursor(api.search_tweets, q=ticker)

if option == "twitter":
    for tweet in tweets.items():
        st.write(tweet.text)

# st.subheader("traderstewie")
# st.image(user.profile_image_url)


# for tweet in tweets:
#     if "$" in tweet.text:
#         words = tweet.text.split(" ")
#         for word in words:
#             if word.startswith("$") and word[1:].isalpha():
#                 symbol = word[1:]
#                 st.write(symbol)
#                 st.write(tweet.text)

ticker_yahoo = ticker + ".NS"

start = dt.datetime(2010, 1, 1)
end = dt.datetime.now()

# Stock_name = st.text_input("Ticker", "AAPL")

df = web.DataReader(ticker_yahoo, "yahoo", start, end)
df.reset_index(inplace=True)

# fig = make_subplots(rows=2, cols=1, shared_xaxes=True)
# fig.add_trace(go.Scatter(x=df.Date, y=df["Adj Close"], mode="lines"), row=1, col=1)
# fig.add_trace(go.Bar(x=df.Date, y=df["Volume"]), row=2, col=1)

if option == "chart":
    fig = go.Figure(
        data=[
            go.Candlestick(
                x=df["Date"],
                open=df["Open"],
                high=df["High"],
                low=df["Low"],
                close=df["Close"],
            )
        ]
    )

# fig.show()

st.plotly_chart(fig)
