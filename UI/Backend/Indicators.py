import StockPrices
from matplotlib import pyplot as plt
import pandas as pd


class invalid_time_id(Exception):
    class SalaryNotInRangeError(Exception):
        def __init__(self, type):
            self.salary = salary
            super().__init__(
                f"{type} is not a valid time time_id for stock price. Valid options are [Close, Open, High, Low]")


def TI_validity(type):
    if type not in ['Close', 'High', 'Low', 'Open']:
        raise invalid_time_id(type)


def rsi(hist, period, time_id):
    TI_validity(time_id)
    hist = hist[time_id]
    close_hist = hist.diff()

    up, down = close_hist.copy(), close_hist.copy()
    up[up < 0] = 0
    down[down > 0] = 0

    _gain = up.ewm(com=(period - 1), min_periods=period).mean()
    _loss = down.abs().ewm(com=(period - 1), min_periods=period).mean()

    RS = _gain / _loss
    return pd.Series(100 - (100 / (1 + RS)), name="RSI")


def stochastic_rsi(hist, k_window, d_window, window, time_id):  # k=avg of the high/low, d=moving average of k
    TI_validity(time_id)
    hist = hist[time_id]

    min_val = hist.rolling(window=window, center=False).min()
    max_val = hist.rolling(window=window, center=False).max()

    stoch = ((hist - min_val) / (max_val - min_val)) * 100

    K = stoch.rolling(window=k_window, center=False).mean()

    D = K.rolling(window=d_window, center=False).mean()

    return K, D


def sma(hist, length):
    reliance = hist['Close'].to_frame()
    reliance['SMA30'] = reliance['Close'].rolling(length).mean()
    reliance.dropna(inplace=True)
    return reliance


def ema(hist, length):
    reliance = hist['Close'].to_frame()
    reliance['EMA'] = reliance['Close'].ewm(span=length).mean()
    reliance.dropna(inplace=True)
    return reliance


if __name__ == '__main__':
    hist = StockPrices.get_hist('MSFT', 59, '90m')
    k, d = stochastic_rsi(hist, 3, 3, 20, 'Close')
    fig = plt.figure('MSFT')
    plt.plot([x for x in range(len(hist))], k)
    plt.plot([x for x in range(len(hist))], d)
    plt.show()
