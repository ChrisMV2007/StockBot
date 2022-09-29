import pandas as pd
import Backend.StockPrices as SP
import Backend.Indicators as Indicators
import Graph as graph
import csv


def inp(ques, ans=None, int_only=False, yn=False, rep_msg=None, rep=False, no_ans=False, cond='_'):
    if ans:
        ans = [an.lower() for an in ans]
    if rep:
        print(rep_msg)
    res = input(ques).lower()
    if no_ans and not res:
        return False
    if int_only:
        try:
            return str(int(res))
        except:
            inp(ques, int_only=True, rep_msg=rep_msg, rep=True)
    if cond != '_':
        if cond:
            return res
        else:
            inp(ques, ans=ans, yn=yn, rep_msg=rep_msg, rep=True, no_ans=no_ans, cond=cond)
    return res if not yn and not ans or yn and res in ['yes', 'no'] or ans and res in ans else inp(ques, ans=ans, yn=yn,
                                                                                                   rep_msg=rep_msg,
                                                                                                   rep=True,
                                                                                                   no_ans=no_ans,
                                                                                                   cond=cond)


def try_replace(x):
    try:
        return int(x)
    except:
        return x


def new_user(df, path):
    user = input('What would you like your username to be? ')

    if user in list(df['user']):
        print('This username is taken!')
        new_user(df, path)

    else:
        row = df.loc[df['user'] == 'Default']
        row['user'] = row['user'].replace(['Default'], f'{user}')
        newuser = pd.DataFrame(row)
        users = pd.concat([df, newuser.iloc[0]], ignore_index=True)
        with open(path, 'a') as users:
            writer = csv.writer(users)
            writer.writerow(newuser.iloc[0])
        data = pd.read_csv('UsersandSettings.csv', encoding="windows_1258")
        return data.loc[data['user'] == user], user


def login(df, path):
    user = input('>>> What is your username? ')

    if user not in list(df['user']):
        print('This user does not exist!')
        login(df, path)

    else:
        data = pd.read_csv('UsersandSettings.csv', encoding="windows_1258")
        return data.loc[data['user'] == user], user


def login_signup():
    print('\n------------------------------ \n')
    users = pd.read_csv('UsersandSettings.csv', encoding="windows_1258")
    los = inp('>>> Would you like to log in or sign up (log in, sign up)? ', ['log in', 'sign up'],
              rep_msg='Please enter either "log in" or "sign up"')

    if los == 'sign up':
        userinfo, username = new_user(users, 'UsersandSettings.csv')
    if los == 'log in':
        userinfo, username = login(users, 'UsersandSettings.csv')

    # PLACEHOLDER FOR ACTUAL ALGORITHM

    for ind, set in enumerate(userinfo):
        userinfo[ind] = try_replace(i)

    return userinfo, username


def auto_graph(hist, stockname, userinfo):
    inames = [ind for ind in ['SMA', 'EMA', 'Stochastic RSI', 'RSI'] if ind in userinfo['Def_Indicators']]

    if 'EMA' in inames:
        inames.remove('EMA')
        inames.append('EMA')
    if 'SMA' in inames:
        inames.remove('SMA')
        inames.append('SMA')

    indicators = []
    colors = []
    for i in inames:
        idict = {'SMA': Indicators.sma, 'EMA': Indicators.ema, 'RSI': Indicators.rsi,
                 'Stochastic RSI': Indicators.stochastic_rsi}

        isettings = list(map(try_replace(try_replace, userinfo[f'Def_{i}_Set'].split(','))))
        indicators.append(idict[i](var_iter=[hist] + [isettings]))

        col = userinfo[f'Def_{i}_Col']
        colors.append(col if ',' not in col else col.split(','))

    return graph.graph(stock=stockname, hist=hist, type=userinfo['Def_Gtype'],
                       dark_mode=True if userinfo['DarkMode'] == 'yes' else False, indicators=indicators, inames=inames,
                       ema_sma_w_hist=True if userinfo['MAwHist'] == 'Y' else False, icolors=colors)


def graph_watchlist(userinfo):
    return [auto_graph(SP.get_hist(s, userinfo['def_hist_days'], userinfo['def_hist_interval']), s, userinfo) for s in
            userinfo['Watchlist'].split(',')]


def manual_graph(userinfo):
    print('\n------------------------- \n')

    def validity_check(rsp, format):
        for ind, inp in enumerate(rsp.split(',')):
            if format[ind] == int:
                try:
                    x = int(rsp)
                except:
                    return False
            elif format[ind] == 'color':
                if len(rsp) != 7 or rsp[0] != '#':
                    return False
            else:
                if rsp not in format[ind]:
                    return False
        return True

    param = None
    oneval_dict = {'graph type': 'def_gtype', 'dark mode': 'darkmode'}
    while param != 'finished':
        params = ['graph type', 'dark mode', 'indicators', 'indicator settings', 'indicator colors', 'stock history',
                  'moving average location']
        param = inp('\n>>> Which setting would you like to change ("options" for options, "finished" to exit)? ',
                    ans=['options', 'finished'] + params, rep_msg='Please input "options", "finished", or a setting')
        if param == 'options':
            print(f'Settings : {params}; some of these settings have sub settings.')

        elif param in [param.lower() for param in params]:

            if param == 'moving average location':
                userinfo['mawhist'] = inp(
                    '>>> Would you like your moving averages (sma/ema) to be displayed in the same graph as the stock '
                    'itself (yes or no)? ', yn=True)

            if param in ['graph type', 'dark mode']:
                val = inp(
                    '>>> Would you like your graph to be displayed via line or candles? ' if param == 'graph type' else
                    '>>> Would you like to use dark mode?', ans=['line', 'candles'] if param == 'graph type' else None,
                    yn=True if param == 'dark mode' else None, rep_msg='Please input either "line" or "candles".' if
                    param == 'graph type' else 'Please enter either "yes" or "no".')
                userinfo[oneval_dict[val]] = val

            if param == 'indicators':
                inds = input('>>> What indicators would you like to use (RSI, Stochastic RSI, EMA, SMA)? ')
                userinfo['Def_Indicators'] = ','.join(
                    [ind for ind in ['rsi', 'stochastic rsi', 'ema', 'sma'] if ind in inds.lower()])

            if param in ['indicator colors', 'indicator settings']:
                ind = inp('>>> Which indicator would you like to change the color of (RSI, Stochastic RSI, EMA, SMA)? '
                          if param == 'indicator colors' else '>>> Which indicator would you like to change the '
                                                              'settings of (RSI, Stochastic RSI, EMA, SMA)? ',
                          ans=['rsi', 'sma', 'ema', 'stochastic rsi'], rep_msg='Please enter an indicator')

            if param == 'indicator colors':
                if ind == 'stochastic rsi':
                    cols = [input('>>> What would you like the first stochastic RSI color to be (hex value)? '),
                            input('>>> What would you like the second stochastic RSI color to be (hex value)? ')]
                    if not validity_check(c, ['color', 'color']):
                        print('Please enter valid hex values (ex : "#000000")')
                        continue
                    userinfo['def_stochastic rsi_col'] = ','.join(cols)

                else:
                    col = input('>>> What color would you like your indicator to be (hex value)? ')
                    if not validity_check([c], ['color']):
                        print('Please enter valid hex values (ex : "#000000")')
                        continue
                    userinfo[f'def_{ind}_col'] = ','.join(cols)

            if param == 'indicator settings':
                set_user_dict = {'rsi': 'period,time id', 'stochastic rsi': 'k window,d window,window,time id',
                                 'sma': 'sma period (only parameter)', 'ema': 'ema period (only parameter)'}
                set_validity_dict = {'rsi': [int, ['Close, High, Open, Low']], 'sma': [int, ['yes', 'no']],
                                     'ema': [int],
                                     'stochastic rsi': [int, int, int, ['Close, High, Open, Low']]}
                sets = input(
                    f'>>> What would you like your settings to be for {ind.upper() if ind != "stochastic rsi" else "stochastic RSI"} (format: <{set_user_dict[ind]}>)?')
                if not validity_check(sets, set_validity_dict[ind]):
                    print(
                        f'Please enter the correct settings format for {ind.upper() if ind != "stochastic rsi" else "stochastic RSI"}. ')
                    continue
                userinfo[f'Def_{ind.upper() if ind != "stochastic rsi" else "stochastic rsi"}_Set'] = sets

            if param == 'Stock History':
                set = inp('>>> Stock history is generated by checking stock prices (samples) with a specified '
                          'interval between each sample. Would \nyou like to change the number of samples or the '
                          'length between each sample (length, interval)? ', ans=['length', 'interval'],
                          rep_msg='Please enter a valid input.')
                if set == 'length':
                    userinfo['def_hist_length'] = inp(
                        '>>> How many samples would you like to be taken (time = samples * interval)? ',
                        int_only=True, rep_msg='Please enter an integer.')

                if set == 'interval':
                    t_ints = ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo']
                    userinfo['def_hist_interval'] = inp(
                        '>>> How long should be taken in between each sample? ',
                        ans=['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo'],
                        rep_msg=f'Please enter a valid time interval. Valid intervals : {t_ints}')

    return userinfo


def change_settings(username, userinfo):
    uinfo = manual_graph(userinfo)

    data = pd.read_csv('UsersandSettings.csv', encoding="windows_1258")
    data = data[data['User'] != username]
    pd.concat([data, uinfo]).to_csv("UsersandSettings.csv", mode="w")


def login_cycle():
    userinfo, username = login_signup()
    active = True
    while active:
        print('\n------------------------- \n')
        action = inp(
            '>>> Input "settings" to change default settings (including your watchlist), "chart" to launch charts '
            '(on default settings), "manual chart" to manually input chart settings, "log out" to log out." ',
            ans=['settings', 'chart', 'manual chart', 'exit'], rep_msg="Please enter a valid input")
        if action == 'settings':
            change_settings(username, userinfo)
        if action == 'chart':
            stock_watchlist = inp(
                '>>> Input "watchlist" to run charts for every stock in your watchlist, input "stock" '
                'to launch a chart for a specific stock.', ans=['watchlist', 'stock'],
                rep_msg='Please enter a valid input')
            if stock_watchlist == 'stock':
                ticker = input('>>> Input stock ticker (all caps): ')
                auto_graph(SP.get_hist(ticker, userinfo['def_hist_length'], userinfo['def_hist_interval']), ticker,
                           userinfo)
            if stock_watchlist == 'watchlist':
                for ticker in userinfo['watchlist'].split(','):
                    auto_graph(SP.get_hist(ticker, userinfo['def_hist_length'], userinfo['def_hist_interval']), ticker,
                               userinfo)
        if action == 'manual chart':
            ticker = input('>>> Input stock ticker (all caps): ')
            manual_graph(userinfo)
            auto_graph(SP.get_hist(ticker, int(userinfo['def_hist_length']), userinfo['def_hist_interval']), ticker,
                       userinfo)
        if action == 'log out':
            return


def main():
    while True:
        login_cycle()
        cont = inp('>>> Would you like to log in or exit the program ("log in", "exit")? ', ans=['log in', 'exit'],
                   rep_msg='Please input "log in" or "exit".')
        if cont == 'log in':
            login_cycle()
        if cont == 'exit':
            return


if __name__ == '__main__':
    main()
