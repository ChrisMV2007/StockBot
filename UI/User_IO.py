import pandas as pd
import UI.Backend.StockPrices as SP
import UI.Backend.Indicators as Indicators
import UI.Graph as graph
import UI.Backend.IndicatorAnalysis as IndAnal
import UI.Backend.Swing as Swing
import csv
import functools
import yfinance as yf

pd.set_option('display.max_columns', 100)

csv_dir = 'UsersandSettings.csv'


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
        data = pd.read_csv(csv_dir, encoding="windows_1258")
        return data.loc[data['user'] == user], user


def login(df, path):
    user = input('>>> What is your username? ')

    if user not in list(df['user']):
        print('This user does not exist!')
        login(df, path)

    else:
        data = pd.read_csv(csv_dir, encoding="windows_1258")
        return (data.loc[data['user'] == user], user)


def login_signup():
    print('\n-----[LOGIN/SIGNUP]-----\n')
    users = pd.read_csv(csv_dir, encoding="windows_1258")
    los = inp('>>> Would you like to log in or sign up (log in, sign up)? ', ['log in', 'sign up'],
              rep_msg='Please enter either "log in" or "sign up"')

    if los == 'sign up':
        userinfo, username = new_user(users, csv_dir)
    if los == 'log in':
        userinfo, username = login(users, csv_dir)

    for i in ['user', 'watchlist', 'def_gtype', 'darkmode', 'def_indicators', 'def_rsi_set', 'def_stochastic rsi_set',
              'def_ema_set', 'def_sma_set', 'def_rsi_col', 'def_stochastic rsi_col', 'def_ema_col', 'def_sma_col',
              'mawhist', 'def_hist_length', 'def_hist_interval']:
        if ',' not in userinfo[i]:
            userinfo[i] = try_replace(userinfo[i])
        elif ',' in userinfo[i]:
            userinfo[i] = [try_replace(x) for x in userinfo[i].split(',')]

    userinfo.drop(userinfo.filter(regex="Unnamed"), axis=1, inplace=True)
    return userinfo, username


def auto_graph(hist, stockname, userinfo):
    inames = [ind for ind in ['SMA', 'EMA', 'Stochastic RSI', 'RSI'] if
              ind.lower() in userinfo['def_indicators'].iloc[0]]

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

        try:
            isettings = list(map(try_replace, userinfo[f'def_{i.lower()}_set'].iloc[0].split(',')))
        except:
            isettings = [try_replace(userinfo[f'def_{i.lower()}_set'].iloc[0])]
        indicators.append(idict[i](var_iter=[hist] + isettings))

        col = userinfo[f'def_{i.lower()}_col'].iloc[0]
        colors.append(col if ',' not in col else col.split(','))

    return graph.graph(stock=stockname, hist=hist, type=userinfo['def_gtype'].iloc[0],
                       dark_mode=True if userinfo['darkmode'].iloc[0] == 'yes' else False, indicators=indicators,
                       inames=inames,
                       ema_sma_w_hist=True if userinfo['mawhist'].iloc[0].lower() == 'yes' else False, icolors=colors)


def graph_watchlist(userinfo):
    return [
        auto_graph(SP.get_hist(s, int(userinfo['def_hist_days']), userinfo['def_hist_interval'].iloc[0]), s, userinfo)
        for s in
        userinfo['watchlist'].split(',')]


def int_check(rsp):
    try:
        x = int(rsp)
        return True
    except:
        return False


def validity_check(rsp, format):
    if not isinstance(rsp, list):
        rsp = rsp.split(',')

    for ind, inp in enumerate(rsp):
        if format[ind] == int:
            try:
                x = int(inp)
            except:
                print(
                    f'Incorrect format: format required an integer, a non integer was input; {inp} was input intead.')
                return False
        elif format[ind] == 'color':
            if len(inp) != 7 or inp[0] != '#':
                print(
                    f'Incorrect format: format required a hex value, which entails a hashtag followed by 6 base-16 numbers; {inp} was input instead')
                return False
        else:
            if inp not in format[ind]:
                print(
                    f'Incorrect format: format required a specific response; {format[ind]} were the valid inputs, {inp} was input instead')
                return False
    return True


def manual_graph(userinfo):
    print('\n-----[SETTINGS INPUT]-----')

    param = None
    oneval_dict = {'graph type': 'def_gtype', 'dark mode': 'darkmode'}
    while param != 'finished':
        params = ['graph type', 'dark mode', 'indicators', 'indicator settings', 'indicator colors', 'stock history',
                  'moving average location', 'watchlist']
        param = inp('\n>>> Which setting would you like to change ("options" for options, "finished" to exit)? ',
                    ans=['options', 'finished'] + params, rep_msg='Please input "options", "finished", or a setting')
        if param == 'options':
            print(f'Settings : {params}; some of these settings have sub settings.')

        elif param in [param for param in params]:

            if param == 'watchlist':
                userinfo['watchlist'] = input('Input your new watchlist (separate stocks with commas, '
                                              'input as tickers in all caps; note that this setting has no error '
                                              'detection): ')

            if param == 'moving average location':
                userinfo['mawhist'] = inp(
                    '>>> Would you like your moving averages (sma/ema) to be displayed in the same graph as the stock '
                    'itself (yes or no)? ', yn=True)

            if param == 'graph type':
                userinfo['def_gtype'] = inp('>>> Would you like your graph to be displayed via line or candles? ',
                                            ans=['line', 'candles'], rep_msg='Please input either "line" or "candles".')

            if param == 'dark mode':
                userinfo['darkmode'] = inp('>>> Would you like to use dark mode? ', yn=True,
                                           rep_msg='Please enter either "yes" or "no".')

            if param == 'indicators':
                inds = input('>>> What indicators would you like to use (RSI, Stochastic RSI, EMA, SMA)? ')
                userinfo['def_indicators'] = ','.join(
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
                    if not validity_check(cols, ['color', 'color']):
                        print('Please enter valid hex values (ex : "#000000")')
                        continue
                    userinfo['def_stochastic rsi_col'] = ','.join(cols)

                else:
                    col = input('>>> What color would you like your indicator to be (hex value)? ')
                    if not validity_check([col], ['color']):
                        print('Please enter valid hex values (ex : "#000000")')
                        continue
                    userinfo[f'def_{ind}_col'] = col

            if param == 'indicator settings':
                set_user_dict = {'rsi': 'period,time id', 'stochastic rsi': 'k window,d window,window,time id',
                                 'sma': 'sma period (only parameter)', 'ema': 'ema period (only parameter)'}
                set_validity_dict = {'rsi': [int, ['Close', 'High', 'Open', 'Low']], 'sma': [int, ['yes', 'no']],
                                     'ema': [int],
                                     'stochastic rsi': [int, int, int, ['Close', 'High', 'Open', 'Low']]}
                sets = input(
                    f'>>> What would you like your settings to be for {ind.upper() if ind != "stochastic rsi" else "stochastic RSI"} (format: <{set_user_dict[ind]}>)? ')
                if not validity_check(sets, set_validity_dict[ind]):
                    print(
                        f'Please enter the correct settings format for {ind.upper() if ind != "stochastic rsi" else "stochastic RSI"}. ')
                    continue
                userinfo[f'def_{ind.lower()}_set'] = sets

            if param == 'stock history':
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

    data = pd.read_csv(csv_dir, encoding="windows_1258")
    data = data[data['user'] != username]
    data.drop(data.filter(regex="Unnamed"), axis=1, inplace=True)
    pd.concat([data, uinfo]).to_csv(csv_dir, mode="w")


def login_cycle():
    userinfo, username = login_signup()
    active = True
    while active:
        print('\n-----[MENU]-----\n')
        action = inp(
            '>>> Input "settings" to change default settings (including your watchlist), "chart" to launch charts '
            '(on default settings), "manual chart" to manually input chart settings,\n"indicator analysis" to perform '
            'indicator analysis, "trend analysis" to perform trend analysis, "log out" to log out." ',
            ans=['settings', 'indicator analysis', 'chart', 'manual chart', 'exit', 'trend analysis', 'log out'],
            rep_msg="Please enter a valid input")
        if action == 'settings':
            change_settings(username, userinfo)
            data = pd.read_csv(csv_dir, encoding="windows_1258")
            userinfo = (data.loc[data['user'] == username], username)
        if action == 'chart':
            stock_watchlist = inp(
                '>>> Input "watchlist" to run charts for every stock in your watchlist, input "stock" '
                'to launch a chart for a specific stock. ', ans=['watchlist', 'stock'],
                rep_msg='Please enter a valid input')
            if stock_watchlist == 'stock':
                ticker = input('>>> Input stock ticker (all caps): ')
                hist = SP.get_hist(ticker, int(userinfo['def_hist_length']), userinfo['def_hist_interval'].iloc[0])
                auto_graph(hist, ticker, userinfo).show()
            if stock_watchlist == 'watchlist':
                for ticker in userinfo['watchlist'].iloc[0].split(','):
                    hist = SP.get_hist(ticker, int(userinfo['def_hist_length']), userinfo['def_hist_interval'].iloc[0])
                    auto_graph(hist, ticker, userinfo).show()
        if action == 'manual chart':
            ticker = input('>>> Input stock ticker (all caps): ')
            temp_userinfo = manual_graph(userinfo)
            auto_graph(
                SP.get_hist(ticker, int(temp_userinfo['def_hist_length']), temp_userinfo['def_hist_interval'].iloc[0]),
                ticker, temp_userinfo).show()
        if action == 'indicator analysis':
            print('\n-----[INDICATOR ANALYSIS]-----')
            SoW = inp('>>> Input "watchlist" to perform an indicator-based analysis on your whole watchlist, input "'
                      'stock" to just do a singular stock. ', ans=['watchlist', 'stock'],
                      rep_msg='Please enter a valid input.')
            if SoW == 'stock':
                ticker = input('>>> Input the ticker of the stock you want to analyse (all caps): ')
                indsfilled = False
                while not indsfilled:
                    ind_input = input(
                        '>>> Input the indicators you would like to use (rsi, stochastic rsi, ema, sma, separate indicators with commas): ')
                    inds = [ind for ind in ['stochastic rsi', 'sma', 'ema'] if ind in ind_input]
                    skip = False
                    try:
                        if ind_input[ind_input.find('rsi') - 11:ind_input.find('rsi') - 1] != 'stochastic':
                            inds.append('rsi')
                        skip = True
                    except:
                        abcdefg = 0
                    if not skip:
                        try:
                            if ind_input[ind_input.find('rsi') - 11:ind_input.find('rsi') - 1] != 'stochastic':
                                inds.append('rsi')
                        except:
                            absdefg = 0

                    if len(inds) == 0:
                        print(
                            'Please input at least 1 indicator. Available indicators: rsi, stochastic rsi, ema, sma. ')
                    else:
                        indsfilled = True
                indBools = []
                for ind in inds:
                    idict = {'sma': Indicators.sma, 'ema': Indicators.ema, 'rsi': Indicators.rsi,
                             'stochastic rsi': Indicators.stochastic_rsi}
                    if ind == 'stochastic rsi':
                        KoD = inp(
                            ">>> Would you like to use stochastic rsi's K window, D window, or both ('k', 'd', or 'kd')? ",
                            ans=['k', 'd', 'kd'], rep_msg='Please enter a valid input.')
                        fmt = False
                        if KoD == 'kd':
                            while not fmt:
                                bound = [
                                    input('>>> What would like the bound for the k window to be (ex: >3 or <5): '),
                                    input('>>> What would like the bound for the d window to be (ex: >3 or <5): ')]
                                if bound[0][0] in ['>', '<'] and bound[1][0] in ['>', '<'] and int_check(
                                        bound[0][1:]) and int_check(bound[1][1:]):
                                    fmt = True
                                else:
                                    print(
                                        'Please enter your bounds with proper formatting (">" or "<" followed by an integer value).')

                        try:
                            isettings = list(map(try_replace, userinfo[f'def_{ind.lower()}_set'].iloc[0].split(',')))
                        except:
                            isettings = [try_replace(userinfo[f'def_{i.lower()}_set'].iloc[0])]

                        indBools.append(
                            IndAnal.stochastic_rsi_anal(Indicators.stochastic_rsi(var_iter=[SP.get_hist(ticker, int(
                                userinfo['def_hist_length']), userinfo['def_hist_interval'].iloc[0])] + userinfo[
                                                                                               'def_stochastic rsi_set'].iloc[
                                                                                               0].split(',')),
                                                        bound, KoD))
                    elif ind == 'rsi':
                        fmt = False
                        while not fmt:
                            bound = input(f'>>> What would like the bound for {ind} to be (ex: >5 or <30): ')
                            if bound[0] in ['>', '<'] and int_check(bound[1:]):
                                fmt = True
                            else:
                                print(
                                    'Please enter your bound with proper formatting (">" or "<" followed by an integer value).')

                        try:
                            isettings = list(map(try_replace, userinfo[f'def_{ind.lower()}_set'].iloc[0].split(',')))
                        except:
                            isettings = [try_replace(userinfo[f'def_{ind.lower()}_set'].iloc[0])]

                        indBools.append(IndAnal.rsi_anal(idict[ind](var_iter=[SP.get_hist(ticker, int(
                            userinfo['def_hist_length']), userinfo['def_hist_interval'].iloc[0])] + isettings), bound))
                    else:
                        boundnum = inp(f'>>> Would you like to set 1 or 2 bounds for {ind} ("1" or "2")? ',
                                       ans=['1', '2'],
                                       rep_msg='Please enter either a 1 or a 2')
                        if boundnum == '1':
                            fmt = False
                            while not fmt:
                                bound = input(
                                    f'>>> What would like the bound for {ind} to be (note that bounds can be negative for {ind}, and they are input as percentages; check github read me for more info): ')
                                if bound[0] in ['>', '<'] and int_check(bound[1:]):
                                    fmt = True
                                else:
                                    print(
                                        'Please enter your bound with proper formatting (">" or "<" followed by an integer value).')

                            try:
                                isettings = list(
                                    map(try_replace, userinfo[f'def_{ind.lower()}_set'].iloc[0].split(',')))
                            except:
                                isettings = [try_replace(userinfo[f'def_{ind.lower()}_set'].iloc[0])]

                            hist = yf.Ticker(ticker).history()
                            last_quote = hist['Close'].iloc[-1]
                            indBools.append(
                                IndAnal.ma_anal(idict[ind](var_iter=[SP.get_hist(ticker, int(
                                    userinfo['def_hist_length']), userinfo['def_hist_interval'].iloc[0])] + isettings),
                                                bound, float(last_quote)))
                        if boundnum == '2':
                            fmt = False
                            while not fmt:
                                bound1 = input(
                                    f'>>> What would like the bound for {ind} to be (note that bounds can be negative for {ind}, and they are input as percentages; check github read me for more info): ')
                                if bound1[0] in ['>', '<'] and int_check(bound1[1:]):
                                    fmt = True
                                else:
                                    print(
                                        'Please enter your bound with proper formatting (">" or "<" followed by an integer value).')
                            fmt = False
                            while not fmt:
                                bound2 = input(
                                    f'>>> What would like the bound for {ind} to be (note that bounds can be negative for {ind}, and they are input as percentages; check github read me for more info): ')
                                if bound2[0] in ['>', '<'] and int_check(bound2[1:]):
                                    fmt = True
                                else:
                                    print(
                                        'Please enter your bound with proper formatting (">" or "<" followed by an integer value).')

                            try:
                                isettings = list(
                                    map(try_replace, userinfo[f'def_{ind.lower()}_set'].iloc[0].split(',')))
                            except:
                                isettings = [try_replace(userinfo[f'def_{ind.lower()}_set'].iloc[0])]

                            hist = yf.Ticker(ticker).history()
                            last_quote = hist['Close'].iloc[-1]
                            indBools.append(
                                IndAnal.ma_anal(idict[ind](var_iter=[SP.get_hist(ticker, int(
                                    userinfo['def_hist_length']), userinfo['def_hist_interval'].iloc[0])] + isettings),
                                                bound1, float(last_quote)))
                            indBools.append(
                                IndAnal.ma_anal(idict[ind](var_iter=[SP.get_hist(ticker, int(
                                    userinfo['def_hist_length']), userinfo['def_hist_interval'].iloc[0])] + isettings),
                                                bound2, float(last_quote)))
                if functools.reduce(lambda x, y: x * y, indBools):
                    print(f'ANALYSIS RESULTS: {ticker} has cleared your bounds.')
                else:
                    print(f'ANALYSIS RESULTS: {ticker} has not cleared your bounds.')
            if SoW == 'watchlist':
                indsfilled = False
                while not indsfilled:
                    ind_input = input(
                        '>>> Input the indicators you would like to use (rsi, stochastic rsi, ema, sma, separate indicators with commas): ')
                    inds = [ind for ind in ['stochastic rsi', 'sma', 'ema'] if ind in ind_input]
                    skip = False
                    try:
                        if ind_input[ind_input.find('rsi') - 11:ind_input.find('rsi') - 1] != 'stochastic':
                            inds.append('rsi')
                        skip = True
                    except:
                        abcdefg = 0
                    if not skip:
                        try:
                            if ind_input[ind_input.find('rsi') - 11:ind_input.find('rsi') - 1] != 'stochastic':
                                inds.append('rsi')
                        except:
                            absdefg = 0

                    if len(inds) == 0:
                        print(
                            'Please input at least 1 indicator. Available indicators: rsi, stochastic rsi, ema, sma. ')
                    else:
                        indsfilled = True
                if 'stochastic rsi' in inds:
                    KoD = inp(
                        ">>> Would you like to use stochastic rsi's K window, D window, or both ('k', 'd', or 'kd')? ",
                        ans=['k', 'd', 'kd'], rep_msg='Please enter a valid input.')
                    fmt = False
                    if KoD == 'kd':
                        while not fmt:
                            srsibounds = [
                                input('>>> What would like the bound for the k window to be (ex: >3 or <5): '),
                                input('>>> What would like the bound for the d window to be (ex: >3 or <5): ')]
                            if srsibounds[0][0] in ['>', '<'] and srsibounds[1][0] in ['>', '<'] and int_check(
                                    srsibounds[0][1:]) and int_check(srsibounds[1][1:]):
                                fmt = True
                            else:
                                print(
                                    'Please enter your bounds with proper formatting (">" or "<" followed by an integer value).')
                if 'rsi' in inds:
                    fmt = False
                    while not fmt:
                        rsibound = input(f'>>> What would like the bound for rsi to be (ex: >5 or <30): ')
                        if rsibound[0] in ['>', '<'] and int_check(rsibound[1:]):
                            fmt = True
                        else:
                            print(
                                'Please enter your bound with proper formatting (">" or "<" followed by an integer value).')
                if 'ema' in inds:
                    boundnum = inp(f'>>> Would you like to set 1 or 2 bounds for ema ("1" or "2")? ',
                                   ans=['1', '2'],
                                   rep_msg='Please enter either a 1 or a 2')
                    if boundnum == '1':
                        fmt = False
                        while not fmt:
                            emabound = input(
                                f'>>> What would like the bound for ema to be (note that bounds can be negative for ema, and they are input as percentages; check github read me for more info): ')
                            if emabound[0] in ['>', '<'] and int_check(emabound[1:]):
                                fmt = True
                            else:
                                print(
                                    'Please enter your bound with proper formatting (">" or "<" followed by an integer value).')
                    if boundnum == '2':
                        fmt = False
                        while not fmt:
                            emabound1 = input(
                                f'>>> What would like the bound for ema to be (note that bounds can be negative for ema, and they are input as percentages; check github read me for more info): ')
                            if emabound1[0] in ['>', '<'] and int_check(emabound1[1:]):
                                fmt = True
                            else:
                                print(
                                    'Please enter your bound with proper formatting (">" or "<" followed by an integer value).')
                        fmt = False
                        while not fmt:
                            emabound2 = input(
                                f'>>> What would like the bound for ema to be (note that bounds can be negative for ema, and they are input as percentages; check github read me for more info): ')
                            if emabound2[0] in ['>', '<'] and int_check(emabound2[1:]):
                                fmt = True
                            else:
                                print(
                                    'Please enter your bound with proper formatting (">" or "<" followed by an integer value).')
                if 'sma' in inds:
                    boundnum = inp(f'>>> Would you like to set 1 or 2 bounds for sma ("1" or "2")? ',
                                   ans=['1', '2'],
                                   rep_msg='Please enter either a 1 or a 2')
                    if boundnum == '1':
                        fmt = False
                        while not fmt:
                            smabound = input(
                                f'>>> What would like the bound for sma to be (note that bounds can be negative for sma, and they are input as percentages; check github read me for more info): ')
                            if smabound[0] in ['>', '<'] and int_check(smabound[1:]):
                                fmt = True
                            else:
                                print(
                                    'Please enter your bound with proper formatting (">" or "<" followed by an integer value).')
                    if boundnum == '2':
                        fmt = False
                        while not fmt:
                            smabound1 = input(
                                f'>>> What would like the bound for sma to be (note that bounds can be negative for sma, and they are input as percentages; check github read me for more info): ')
                            if smabound1[0] in ['>', '<'] and int_check(smabound1[1:]):
                                fmt = True
                            else:
                                print(
                                    'Please enter your bound with proper formatting (">" or "<" followed by an integer value).')
                        fmt = False
                        while not fmt:
                            smabound2 = input(
                                f'>>> What would like the bound for sma to be (note that bounds can be negative for sma, and they are input as percentages; check github read me for more info): ')
                            if smabound2[0] in ['>', '<'] and int_check(smabound2[1:]):
                                fmt = True
                            else:
                                print(
                                    'Please enter your bound with proper formatting (">" or "<" followed by an integer value).')
                valid_stocks = []
                for ticker in userinfo['watchlist'].iloc[0].split(','):
                    indBools = []
                    for ind in inds:
                        idict = {'sma': Indicators.sma, 'ema': Indicators.ema, 'rsi': Indicators.rsi,
                                 'stochastic rsi': Indicators.stochastic_rsi}
                        if ind == 'stochastic rsi':
                            try:
                                isettings = list(
                                    map(try_replace, userinfo[f'def_{ind.lower()}_set'].iloc[0].split(',')))
                            except:
                                isettings = [try_replace(userinfo[f'def_{i.lower()}_set'].iloc[0])]

                            indBools.append(
                                IndAnal.stochastic_rsi_anal(Indicators.stochastic_rsi(var_iter=[SP.get_hist(ticker, int(
                                    userinfo['def_hist_length']), userinfo['def_hist_interval'].iloc[0])] + userinfo[
                                                                                                   'def_stochastic rsi_set'].iloc[
                                                                                                   0].split(',')),
                                                            srsibounds, KoD))
                        elif ind == 'rsi':
                            try:
                                isettings = list(
                                    map(try_replace, userinfo[f'def_{ind.lower()}_set'].iloc[0].split(',')))
                            except:
                                isettings = [try_replace(userinfo[f'def_{ind.lower()}_set'].iloc[0])]

                            indBools.append(IndAnal.rsi_anal(idict[ind](var_iter=[SP.get_hist(ticker, int(
                                userinfo['def_hist_length']), userinfo['def_hist_interval'].iloc[0])] + isettings),
                                                             rsibound))
                        elif ind == 'ema':
                            if boundnum == '1':
                                try:
                                    isettings = list(
                                        map(try_replace, userinfo[f'def_{ind.lower()}_set'].iloc[0].split(',')))
                                except:
                                    isettings = [try_replace(userinfo[f'def_{ind.lower()}_set'].iloc[0])]

                                hist = yf.Ticker(ticker).history()
                                last_quote = hist['Close'].iloc[-1]
                                indBools.append(
                                    IndAnal.ma_anal(idict[ind](var_iter=[SP.get_hist(ticker, int(
                                        userinfo['def_hist_length']), userinfo['def_hist_interval'].iloc[
                                                                                         0])] + isettings),
                                                    emabound, float(last_quote)))
                            if boundnum == '2':
                                try:
                                    isettings = list(
                                        map(try_replace, userinfo[f'def_{ind.lower()}_set'].iloc[0].split(',')))
                                except:
                                    isettings = [try_replace(userinfo[f'def_{ind.lower()}_set'].iloc[0])]

                                hist = yf.Ticker(ticker).history()
                                last_quote = hist['Close'].iloc[-1]
                                indBools.append(
                                    IndAnal.ma_anal(idict[ind](var_iter=[SP.get_hist(ticker, int(
                                        userinfo['def_hist_length']), userinfo['def_hist_interval'].iloc[
                                                                                         0])] + isettings),
                                                    emabound1, float(last_quote)))
                                indBools.append(
                                    IndAnal.ma_anal(idict[ind](var_iter=[SP.get_hist(ticker, int(
                                        userinfo['def_hist_length']), userinfo['def_hist_interval'].iloc[
                                                                                         0])] + isettings),
                                                    emabound2, float(last_quote)))
                        elif ind == 'sma':
                            if boundnum == '1':
                                try:
                                    isettings = list(
                                        map(try_replace, userinfo[f'def_{ind.lower()}_set'].iloc[0].split(',')))
                                except:
                                    isettings = [try_replace(userinfo[f'def_{ind.lower()}_set'].iloc[0])]

                                hist = yf.Ticker(ticker).history()
                                last_quote = hist['Close'].iloc[-1]
                                indBools.append(
                                    IndAnal.ma_anal(idict[ind](var_iter=[SP.get_hist(ticker, int(
                                        userinfo['def_hist_length']), userinfo['def_hist_interval'].iloc[
                                                                                         0])] + isettings),
                                                    smabound, float(last_quote)))
                            if boundnum == '2':
                                try:
                                    isettings = list(
                                        map(try_replace, userinfo[f'def_{ind.lower()}_set'].iloc[0].split(',')))
                                except:
                                    isettings = [try_replace(userinfo[f'def_{ind.lower()}_set'].iloc[0])]

                                hist = yf.Ticker(ticker).history()
                                last_quote = hist['Close'].iloc[-1]
                                indBools.append(
                                    IndAnal.ma_anal(idict[ind](var_iter=[SP.get_hist(ticker, int(
                                        userinfo['def_hist_length']), userinfo['def_hist_interval'].iloc[
                                                                                         0])] + isettings),
                                                    smabound1, float(last_quote)))
                                indBools.append(
                                    IndAnal.ma_anal(idict[ind](var_iter=[SP.get_hist(ticker, int(
                                        userinfo['def_hist_length']), userinfo['def_hist_interval'].iloc[
                                                                                         0])] + isettings),
                                                    smabound2, float(last_quote)))
                    if functools.reduce(lambda x, y: x * y, indBools):
                        valid_stocks.append(ticker)
                if len(valid_stocks) >= 1:
                    print(f'ANALYSIS RESULTS: {valid_stocks} passed your bounds.')
                else:
                    print('ANALYSIS RESULTS: No stocks passed your bounds.')
        if action == 'trend analysis':
            print('\n-----[TREND ANALYSIS]-----')
            SoW = inp('>>> Input "watchlist" to perform an trend analysis on your whole watchlist, input "'
                      'stock" to just do a singular stock. ', ans=['watchlist', 'stock'],
                      rep_msg='Please enter a valid input.')
            if SoW == 'stock':
                ticker = input(
                    '>>> What stock would you like to perform trend analysis on (input ticker in all caps)? ')
                len = inp('>>> How many intervals back would you like to measure trend for (see github readme for more '
                          'info on how hist tracking works)? ', int_only=True, rep_msg='Please input an integer.')
                time_id = inp(
                    '>>> What time id would you like to use (see github for more info on how hist tracking works)? ',
                    ans=['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo'],
                    rep_msg='Please enter a valid time interval.')
                ema_len = inp('>>> What would you like your averaging length to be (see github readme for more info)? ',
                              int_only=True, rep_msg='Please enter an integer.')
                step = inp(
                    '>>> What would you like the step to be for your trend analysis (check github readme for more '
                    'info, input 1 if you would not like a step)? ', int_only=True, rep_msg='Please input an'
                                                                                            'integer')
                posneg, certainty = Swing.swing_certainty(SP.get_hist(ticker, int(len) + int(ema_len), time_id),
                                                          int(ema_len), int(len), int(step))
                print(f'TREND RESULTS: {ticker} has a {posneg} trend (certainty : {certainty}%)')
            if SoW == 'watchlist':
                len = inp('>>> How many intervals back would you like to measure trend for (see github readme for more '
                          'info on how hist tracking works)? ', int_only=True, rep_msg='Please input an integer.')
                time_id = inp(
                    '>>> What time id would you like to use (see github for more info on how hist track works)? ',
                    ans=['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo'],
                    rep_msg='Please enter a valid time interval.')
                ema_len = inp('>>> What would you like your averaging length to be (see github readme for more info)? ',
                              int_only=True, rep_msg='Please enter an integer.')
                step = inp(
                    '>>> What would you like the step to be for your trend analysis (check github readme for more '
                    'info, input 1 if you would not like a step)? ', int_only=True, rep_msg='Please input an'
                                                                                            'integer')
                posneg_bound = inp(
                    '>>> Which direction you like your stocks to be trending ("positive" or "negative")? ',
                    ans=['positive', 'negative'], rep_msg='Please enter a valid input.')
                threshold = inp('>>> What is the minimum trend certainty percentage you will accept? ', int_only=True,
                                rep_msg='Please enter an integer.')

                qualified = {}
                for ticker in userinfo['watchlist'].iloc[0].split(','):
                    posneg, certainty = Swing.swing_certainty(SP.get_hist(ticker, int(len) + int(ema_len), time_id),
                                                              int(ema_len), int(len), int(step))
                    if posneg == posneg_bound and certainty > int(threshold):
                        qualified[ticker] = certainty
                stocks = ', '.join([f"{ticker} (certainty: {certainty}%)" for ticker, certainty in qualified.items()])
                print(f'TREND RESULTS: The following stocks are trending {posneg_bound}; {stocks}.')

        if action == 'log out':
            return
