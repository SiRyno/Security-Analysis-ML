import pandas as pd


def get_list_csv(save=False):
    url = "https://www1.nseindia.com/content/equities/EQUITY_L.csv"

    sec_pd = pd.read_csv(url)

    # print(sec_pd.head())

    if save:
        sec_pd.to_csv("nifty_sec.csv")


get_list_csv(True)
