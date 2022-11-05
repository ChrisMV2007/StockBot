from matplotlib import pyplot as plt
import pandas as pd


class invalid_time_id(Exception):
    def __init__(self, type):
        super().__init__(
            f"{type} is not a valid time time_id for stock price. Valid options are [Close, Open, High, Low]")


def TI_validity(type):
    if type not in ['Close', 'High', 'Low', 'Open']:
        raise invalid_time_id(type)


def rsi(hist=None, period=None, time_id=None, var_iter=None):
    if var_iter:
        hist, period, time_id = var_iter
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


def stochastic_rsi(hist=None, k_window=None, d_window=None, window=None, time_id=None,
                   var_iter=None):  # k=avg of the high/low, d=moving average of k
    if var_iter:
        hist, k_window, d_window, window, time_id = var_iter
        k_window, d_window, window = int(k_window), int(d_window), int(window)
    TI_validity(time_id)
    hist = hist[time_id]

    min_val = hist.rolling(window=window, center=False).min()
    max_val = hist.rolling(window=window, center=False).max()

    stoch = ((hist - min_val) / (max_val - min_val)) * 100

    K = stoch.rolling(window=k_window, center=False).mean()

    D = K.rolling(window=d_window, center=False).mean()

    return [K, D]


def sma(hist=None, length=None, var_iter=None):
    if var_iter:
        hist, length = var_iter
    reliance = hist['Close'].to_frame()
    reliance['SMA'] = reliance['Close'].rolling(length).mean()
    reliance.dropna(inplace=True)
    return reliance['SMA']


def ema(hist=None, length=None, var_iter=None):
    if var_iter:
        hist, length = var_iter
    if type(hist) != 'DataFrame':
        reliance = hist['Close'].to_frame()
    else:
        reliance = hist['Close']
    reliance['EMA'] = reliance['Close'].ewm(span=length).mean()
    reliance.dropna(inplace=True)
    return reliance['EMA']
