def rsi_anal(rsi, bound):
    if bound[0] == '>':
        return rsi[rsi.size - 1] > float(bound[1:])
    if bound[0] == '<':
        return rsi[rsi.size - 1] < float(bound[1:])


def stochastic_rsi_anal(stochastic_rsi, bound, KoD):  # K comes first
    if len(KoD) == 2:
        return True if eval(
            f'{stochastic_rsi[0][stochastic_rsi[0].size - 1]} {bound[0][0]} {bound[0][1:]}') and eval(
            f'{stochastic_rsi[1][stochastic_rsi[1].size - 1]} {bound[1][0]} {bound[1][1:]}') else False
    if len(KoD) == 1:
        if KoD == 'k':
            if bound[0][0] == '>':
                return stochastic_rsi[0][stochastic_rsi[0].size - 1] > float(bound[0][1:])
            if bound[0][0] == '<':
                return stochastic_rsi[0][stochastic_rsi[0].size - 1] < float(bound[0][1:])
        if KoD == 'd':
            if bound[1][0] == '>':
                return stochastic_rsi[1][stochastic_rsi[1].size - 1] > float(bound[0][1:])
            if bound[1][0] == '<':
                return stochastic_rsi[1][stochastic_rsi[1].size - 1] < float(bound[0][1:])


def ma_anal(ma, bound, price):  # input price as a % above or below
    if bound[0] == '>':
        return (ma[ma.size - 1] - price) / price > float(bound[1:]) / 100
    if bound[0] == '<':
        return (ma[ma.size - 1] - price) / price < float(bound[1:]) / 100
