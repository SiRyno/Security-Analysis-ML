import requests
import os
import bs4 as bs
import pickle
import pandas as pd

def get_list():
    url = "https://en.wikipedia.org/wiki/NIFTY_50"

    resp = requests.get(url)
    soup = bs.BeautifulSoup(resp.text, 'lxml')
    table = soup.find("table", {'class': "wikitable sortable"})
    
    tickers = []
    
    for row in table.findAll('tr')[1:]:
        ticker = row.findAll('td')[1].text
        tickers.append(ticker)

    with open("nifty50tickers.pickle", "wb") as f:
        pickle.dump(tickers, f)

    return tickers

get_list()
