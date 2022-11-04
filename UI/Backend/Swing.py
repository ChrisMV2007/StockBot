import pandas as pd
import datetime
from datetime import date, timedelta
from UI.Backend.StockPrices import get_hist
from matplotlib import pyplot as plt
from UI.Backend.Indicators import ema


def swing(hist, ema_len, length, step):
    ema_ = ema(hist, ema_len)
    cut = len(ema_) - length if len(ema_) > length else 0
    ema_ = ema_.tolist()[cut::step]
    res = []
    for ind, ma in enumerate(ema_):
        try:
            prev = ema_[ind - 1]
            res.append('+' if prev < ma else '-' if prev > ma else '=')
        except:
            continue
    return [round(res.count('+') / len(res) * 100, 2),
            round(res.count('-') / len(res) * 100, 2)]


def swing_certainty(hist, ema_len, length, step):
    pos, neg = swing(hist, ema_len, length, step)
    posneg = "positive" if pos > neg else "negative"
    certainty = pos if pos > neg else neg
    return posneg, certainty


if __name__ == '__main__':
    tsla = get_hist('GOOG', 130, '1d')
    posneg, certainty = swing_certainty(tsla, 30, 100, 5)
    print(f'GOOG has a {posneg} trend (certainty : {certainty}%)')
