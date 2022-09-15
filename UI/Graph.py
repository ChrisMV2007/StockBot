from mplfinance.original_flavor import candlestick_ohlc
from Backend.StockPrices import get_hist
from matplotlib import pyplot as plt
import matplotlib.dates as mpdates
import Backend.Indicators as ind
import pandas as pd

pd.set_option('mode.chained_assignment', None)


class invalid_type(Exception):
    def __init__(self, type, func, options):
        super().__init__(
            f"{type} is not a valid type for function '{func}'; valid options are {options}")


# IMPORTANT NOTE: IF EMA_SMA_W_HIST IS SET TO TRUE, SMA AND EMA MUST BE INPUT AFTER RSI AND STOCHASTIC RSI IN THE
# INDICATORS LIST
def graph(stock, hist, type, dark_mode=False, indicators=[], inames=[], ema_sma_w_hist=False, icolors=[]):
    if indicators=='NA_':
        indicators=[]
    
    if type not in ['line', 'candles']:
        raise invalid_type(type, 'display stock history', ['line', 'candles'])
    if dark_mode:
        plt.style.use('dark_background')

    fig, ax = plt.subplots(
        nrows=len([x for x in inames if x not in ['EMA', 'SMA']]) + 1 if ema_sma_w_hist else len(indicators) + 1,
        ncols=1)

    ax[0].set_xlabel('Date')
    ax[0].set_ylabel('Price')
    ax[0].set_title(f'{stock} {type[:1].capitalize() + type[1:]} Graph')

    hist['Date'] = pd.to_datetime(hist['Date'])
    date_format = mpdates.DateFormatter('%Y-%m-%d')
    ax[0].xaxis.set_major_formatter(date_format)

    if type == 'line':
        ax[0].fill_between(hist['Date'], hist['Close'], where=hist['Close'] > 0, alpha=0.25, color='b',
                           interpolate=True)
        ax[0].plot(hist['Date'], hist['Close'])

    if type == 'candles':
        copy = hist.copy()
        copy['Date'] = copy['Date'].map(mpdates.date2num)
        candlestick_ohlc(ax[0], copy.values, width=0.6, colorup='green', colordown='red', alpha=0.8)

    for index, indicator in enumerate(indicators):
        index, color = index, icolors[index]
        label = inames[index]
        if label == 'Stochastic RSI':
            ax[index + 1].plot(hist['Date'][len(hist) - len(indicator[0]):], indicator[0], color=color[0],
                               label=label)
            ax[index + 1].plot(hist['Date'][len(hist) - len(indicator[1]):], indicator[1], color=color[1],
                               label=label)
            ax[index + 1].fill_between(hist['Date'], -20, 20, color=color[0], alpha=0.25)
            ax[index + 1].fill_between(hist['Date'], 80, 120, color=color[1], alpha=0.25)
        if inames[index] in ['EMA', 'SMA'] and ema_sma_w_hist:
            index = -1
        else:
            ax[index + 1].set_ylabel(inames[index])
        if label == 'RSI':
            ax[index + 1].fill_between(hist['Date'], 10, 30, color=color, alpha=0.25)
            ax[index + 1].fill_between(hist['Date'], 70, 90, color=color, alpha=0.25)
        if label != 'Stochastic RSI':
            ax[index + 1].plot(hist['Date'][len(hist) - len(indicator):], indicator, color=color, label=label)

    fig.autofmt_xdate()
    fig.tight_layout()
    fig.legend(loc='lower left')

    return plt


if __name__ == '__main__':  # Example Graph
    hist = get_hist('AAPL', 100, '1d')
    graph('AAPL', hist, 'candles', dark_mode=True,
          indicators=[ind.rsi(hist, 14, 'Close'), ind.stochastic_rsi(hist, 3, 3, 5, 'Close'), ind.sma(hist, 20),
                      ind.ema(hist, 14)], inames=['RSI', 'Stochastic RSI', 'SMA', 'EMA'], ema_sma_w_hist=True,
          icolors=['#A865C9', ['#FBBF77', 'b'], '#FFD580', '#FFFFE0']).show()
