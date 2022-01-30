import pandas as pd
import numpy as np
import datetime as dt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas_datareader.data as web
import streamlit as st
import model as m
import tweepy
import config


ticker = m.get_ticker()

st.title("Security Analysis")

option = st.sidebar.selectbox("Which Dashboard?", ("chart", "twitter"))
ticker = st.sidebar.selectbox(label="Stock", options=ticker)

st.title(option)
st.subheader(ticker)

if option == "twitter":
    auth = tweepy.OAuthHandler(
        config.TWITTER_CONSUMER_KEY, config.TWITTER_CONSUMER_SECRET
    )
    api = tweepy.API(auth, wait_on_rate_limit=True)

    tweets = tweepy.Cursor(api.search_tweets, q=ticker)

    i = 1
    for tweet in tweets.items():
        if i <= 30:
            st.write(str(i) + " -> " + tweet.text)
            i += 1


ticker_yahoo = ticker + ".NS"

start = dt.datetime(2010, 1, 1)
end = dt.datetime.now()

df = web.DataReader(ticker_yahoo, "yahoo", start, end)
df.reset_index(inplace=True)

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
    st.plotly_chart(fig)

    window = 30

    num_samples = len(df) - window
    indices = np.arange(num_samples).astype(int)[:, None] + np.arange(
        window + 1
    ).astype(int)
    data = df["Adj Close"].values[indices]
    X = data[:, :-1]
    y = data[:, -1]
    split_frac = 0.8
    split_indices = int(split_frac * num_samples)
    X_train = X[:split_indices]
    y_train = y[:split_indices]
    X_test = X[split_indices:]
    y_test = y[split_indices:]

    from sklearn.linear_model import LinearRegression

    # Train
    linear_reg_model = LinearRegression()
    linear_reg_model.fit(X_train, y_train)

    # Inferences
    y_pred_train_linear_reg = linear_reg_model.predict(X_train)
    y_pred_linear_reg = linear_reg_model.predict(X_test)

    st.write(y_pred_linear_reg)
