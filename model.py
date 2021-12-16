import pandas as pd
import datetime as dt
import pandas_datareader as web


def get_ticker(save=False):
    url = "https://www1.nseindia.com/content/equities/EQUITY_L.csv"

    ticker = pd.read_csv(url)

    if save:
        ticker.to_csv("nifty_sec.csv")

    return ticker["SYMBOL"].to_list()


ticker = get_ticker()

# print(len(ticker))

ticker_yahoo = [s + ".NS" for s in ticker]


def get_data():
    start = dt.datetime(2000, 1, 1)
    end = dt.datetime.now()

    # df = web.get_data_yahoo(ticker_yahoo[0], start, end)

    data = {
        ticker[c]: web.get_data_yahoo(ticker_yahoo[c], start, end)
        for c in range(len(ticker))
    }

    return data
