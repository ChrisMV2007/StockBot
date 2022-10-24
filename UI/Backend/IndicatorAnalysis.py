def rsi_anal(rsi, bound):
    if bound[0] == '>':
        return rsi[rsi.size - 1] > bound[1:]
    if bound[0] == '<':
        return rsi[rsi.size - 1] < bound[1:]


def stochastic_rsi_anal(stochastic_rsi, bound, KoD):  # K comes first
    if KoD.len == 2:
        return True if eval(
            f'{stochastic_rsi[0][stochastic_rsi[0].size - 1]} {bound[0][0]} {bound[0][1:]}') and eval(
            f'{stochastic_rsi[1][stochastic_rsi[1].size - 1]} {bound[1][0]} {bound[1][1:]}') else False
    if KoD.len == 1:
        if KoD == 'K':
            if bound[0][0] == '>':
                return stochastic_rsi[0][stochastic_rsi[0].size - 1] > bound[0][1:]
            if bound[0][0] == '<':
                return stochastic_rsi[0][stochastic_rsi[0].size - 1] < bound[0][1:]
        if KoD == 'D':
            if bound[1][0] == '>':
                return stochastic_rsi[1][stochastic_rsi[1].size - 1] > bound[0][1:]
            if bound[1][0] == '<':
                return stochastic_rsi[1][stochastic_rsi[1].size - 1] < bound[0][1:]


def ema_anal(ema, bound):
    if bound[0] == '>':
        return ema[ema.size - 1] > bound[1:]
    if bound[0] == '<':
        return ema[ema.size - 1] < bound[1:]


def sma_anal(sma, bound):
    if bound[0] == '>':
        return sma[sma.size - 1] > bound[1:]
    if bound[0] == '<':
        return sma[sma.size - 1] < bound[1:]
