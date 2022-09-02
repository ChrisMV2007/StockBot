import yfinance as yf
import pandas as pd
import datetime
from datetime import date, timedelta


def get_hist(ticker, days, interval):
    end_date = date.today().strftime("%Y-%m-%d")
    start_date = (date.today() - timedelta(days=days)).strftime("%Y-%m-%d")
    data = yf.download(ticker,
                       start=start_date,
                       end=end_date,
                       interval=interval,
                       progress=False)
    data["Date"] = data.index
    data = data[["Date", "Open", "High", "Low", "Close"]]
    data.reset_index(drop=True, inplace=True)
    return data


def get_close(ticker):
    ticker = yf.Ticker(ticker)
    data = ticker.history()
    return data['Close'].iloc[-1]


def get_info(ticker, data):
    ticker = yf.Ticker(ticker)
    if data[0] == 'available data':
        return [key for key, val in ticker.info.items()]
    try:
        return [(x, ticker.info[x]) for x in data]
    except:
        print('! ERROR: invalid key for ticker info. !')
        return -1


if __name__ == '__main__':
    print(get_hist('MSFT', 59, '90m'))