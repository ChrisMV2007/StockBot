import pandas as pd
import UI.Backend.StockPrices as SP
import UI.Backend.Indicators as Indicators
import UI.Graph as graph
import csv

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


def manual_graph(userinfo):
    print('\n-----[SETTINGS INPUT]-----')

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
            '(on default settings), "manual chart" to manually input chart settings, "log out" to log out." ',
            ans=['settings', 'chart', 'manual chart', 'exit', 'log out'], rep_msg="Please enter a valid input")
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
                for ticker in userinfo['watchlist'].split(','):
                    hist = SP.get_hist(ticker, int(userinfo['def_hist_length']), userinfo['def_hist_interval'].iloc[0])
                    auto_graph(hist, ticker, userinfo).show()
        if action == 'manual chart':
            ticker = input('>>> Input stock ticker (all caps): ')
            temp_userinfo = manual_graph(userinfo)
            auto_graph(
                SP.get_hist(ticker, int(temp_userinfo['def_hist_length']), temp_userinfo['def_hist_interval'].iloc[0]),
                ticker, temp_userinfo).show()
        if action == 'log out':
            return
