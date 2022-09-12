import pandas as pd
import Backend.StockPrices as SP
import Backend.Indicators as Indicators
import Graph as graph
import csv


def inp(ques, ans=None, int_only=False, yn=False, rep_msg=None, rep=False, no_ans=False, cond=None):
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
    if cond:
        if cond:
            return res
        else:
            inp(ques, ans=ans, yn=yn, rep_msg=rep_msg, rep=True, no_ans=no_ans, cond=cond)
    return res if not yn and not ans or yn and res in ['yes', 'no'] or ans and res in ans else inp(ques, ans=ans, yn=yn,
                                                                                                   rep_msg=rep_msg,
                                                                                                   rep=True,
                                                                                                   no_ans=no_ans,
                                                                                                   cond=cond)


def new_user(df, path):
    user = input('What would you like your username to be? ')

    if user in list(df['User']):
        print('This username is taken!')
        new_user(df, path)

    else:
        row = df.loc[df['User'] == 'Default']
        row['User'] = row['User'].replace(['Default'], f'{user}')
        newuser = pd.DataFrame(row)
        users = pd.concat([df, newuser.iloc[0]], ignore_index=True)
        with open(path, 'a') as users:
            writer = csv.writer(users)
            writer.writerow(newuser.iloc[0])
        data = pd.read_csv('UsersandSettings.csv', encoding="windows_1258")
        return data.loc[data['User'] == user]


def login(df, path):
    user = input('What is your username? ')

    if user not in list(df['User']):
        print('This user does not exist!')
        login(df, path)

    else:
        data = pd.read_csv('UsersandSettings.csv', encoding="windows_1258")
        return data.loc[data['User'] == user]


def login_signup():
    users = pd.read_csv('UsersandSettings.csv', encoding="windows_1258")
    los = inp('Would you like to log in or sign up (log in, sign up)? ', ['log in', 'sign up'],
              rep_msg='Please enter either "log in" or "sign up"')

    if los == 'sign up':
        userinfo = new_user(users, 'UsersandSettings.csv')
    if los == 'log in':
        userinfo = login(users, 'UsersandSettings.csv')

    return userinfo, los  # los = username


def try_replace(x):
    try:
        return int(x)
    except:
        return x


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
                       dark_mode=True if userinfo['DarkMode'] == 'Y' else False, indicators=indicators, inames=inames,
                       ema_sma_w_hist=True if userinfo['MAwHist'] == 'Y' else False, icolors=colors)


def graph_watchlist(userinfo):
    return [auto_graph(SP.get_hist(s, userinfo['def_hist_days'], userinfo['def_hist_interval']), s, userinfo) for s in
            userinfo['Watchlist'].split(',')]


def manual_graph(username):
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
    oneval_dict = {'graph type': 'Def_Gtype', 'dark mode': 'DarkMode'}
    while param != 'finished':
        params = ['Graph Type', 'Dark Mode', 'Indicators', 'Indicator Settings', 'Indicator Colors', 'Stock History']
        param = inp('Which setting would you like to change ("options" for options, "finished" to exit)? ',
                    ans=['options', 'finished'] + [params], rep_msg='Please input "options", "finished", or a setting')
        if param == 'options':
            print(f'Settings : {params}; some of these settings have sub settings.')

        elif param in params:

            if param in ['graph type', 'dark mode']:
                val = inp(
                    'Would you like your graph to be displayed via line or candles? ' if param == 'Graph Type' else
                    'Would you like to use dark mode?', ans=['line', 'candles'] if param == 'Graph Type' else None,
                    yn=True if param == 'Dark Mode' else None, rep_msg='Please input either "line" or "candles".' if
                    param == 'Graph Type' else 'Please enter either "yes" or "no".')
                userinfo[oneval_dict[val]] = val

            elif param == 'indicators':
                userinfo['Indicators'] = ','.join(
                    [ind for ind in ['rsi', 'stochastic rsi', 'ema', 'sma'] if ind in input(
                        'What indicators would you like to use (RSI, Stochastic RSI, EMA, SMA)? ').lower()])

            elif param in ['indicator colors', 'indicator settings']:
                ind = inp('Which indicator would you like to change the color of (RSI, Stochastic RSI, EMA, SMA)? ' if
                          param == 'indicator colors' else 'Which indicator would you like to change the settings of '
                                                           '(RSI, Stochastic RSI, EMA, SMA)? ',
                          ans=['RSI', 'SMA', 'EMA', 'Stochastic RSI'], rep_msg='Please enter an indicator')

                if param == 'indicator colors':
                    if ind == 'stochastic rsi':
                        cols = [input('What would you like the first stochastic RSI color to be (hex value)? '),
                                input('What would you like the second stochastic RSI color to be (hex value)? ')]
                        if not validity_check(c, ['color', 'color']):
                            print('Please enter valid hex values (ex : "#000000")')
                            continue
                        userinfo['Def_Stochastic RSI_Col'] = ','.join(cols)

                    else:
                        col = input('What color would you like your indicator to be (hex value)? ')
                        if not validity_check([c], ['color']):
                            print('Please enter valid hex values (ex : "#000000")')
                            continue
                        userinfo[f'Def_{ind.upper()}_Col'] = ','.join(cols)

                if param == 'indicator settings':
                    set_user_dict = {'rsi': 'period, time id', 'stochastic rsi': 'k window, d window, window, time id',
                                     'sma': 'sma period', 'ema': 'ema period'}
                    set_validity_dict = {'rsi': [int, ['Close, High, Open, Low']], 'sma': [int], 'ema': [int],
                                         'stochastic rsi': [int, int, int, ['Close, High, Open, Low']]}
                    sets = input(
                        f'What would you like your settings to be for {param.upper() if param != "stochastic rsi" else "stochastic RSI"} (format: <{set_user_dict[param]}>)?')
                    if not validity_check(sets, set_validity_dict[ind]):
                        print(
                            f'Please enter the correct settings format for {ind.upper() if ind != "stochastic rsi" else "stochastic RSI"}. ')
                        continue
                    
    return userinfo


if __name__ == '__main__':
    userinfo, username = login_signup()
