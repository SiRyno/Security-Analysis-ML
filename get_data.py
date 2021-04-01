import get_list
import os
import pandas as pd
import pickle
import datetime as dt
import pandas_datareader.data as web

def get_data(list_get=False):
    if list_get:
        tickers = get_list.get_list()
    else:
        with open("nifty50tickers.pickle", "rb") as f:
            tickers = pickle.load(f)
    
    if not os.path.exists("stock_dfs"):
        os.makedirs("stock_dfs")

    start = dt.datetime(2000, 1, 1)
    end = dt.datetime.now()

    for ticker in tickers:
        if not os.path.exists("stock_dfs/{}.csv".format(ticker)):
            print("Downloading: ", ticker)
            df = web.get_data_yahoo(ticker, start, end)
            df.to_csv("stock_dfs/{}.csv".format(ticker))
        else:
            print("Already have {}.".format(ticker))
        
get_data()