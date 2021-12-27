import pandas as pd
import numpy as np
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
    i = 1
    for tweet in tweets.items():
        if i <= 30:
            st.write(str(i) + " -> " + tweet.text)
            i += 1

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
    st.plotly_chart(fig)

    url = "https://yhoo.it/33MKS3H"
    st.write(url)
    # fig.show()

    # Prediction
    # Train the model on the last 29 days and predict the label for the 30th day
    window = 30

    num_samples = len(df) - window
    indices = np.arange(num_samples).astype(np.int)[:, None] + np.arange(
        window + 1
    ).astype(np.int)
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
    # Plot the graph for it has trained on the training data
    # df_linear = df.copy()
    # df_linear.drop(["Open", "High", "Low", "Close", "Volume"], axis=1, inplace=True)
    # df_linear = df_linear.iloc[window:split_indices]
    # df_linear["Adj Close Train"] = y_pred_train_linear_reg[:-window]
    # df_linear.plot(
    #     label="AAPL", figsize=(16, 8), title="Adjusted Closing Price", grid=True
    # )
