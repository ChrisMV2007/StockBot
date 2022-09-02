import pandas as pd
from Backend.StockPrices import get_hist
from matplotlib import pyplot as plt
import mplfinance


class invalid_type(Exception):
    def __init__(self, type, func, options):
        super().__init__(
            f"{type} is not a valid type for function '{func}'; valid options are {options}")


def display_hist(stock, hist, type):
    if type not in ['line', 'candles']:
        raise invalid_type(type, 'display stock history', ['line', 'candles'])
    if type == 'line':
        plt.figure(f"{stock} Line Graph")
        plt.xlabel('Date')
        plt.ylabel('Close')
        plt.title(f'{stock} Line Graph')
        plt.fill_between(hist['Date'], hist['Close'], where=hist['Close'] > 0, alpha=0.25, color='b', interpolate=True)
        plt.plot(hist['Date'], hist['Close'])
        return plt
