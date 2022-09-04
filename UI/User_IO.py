import pandas as pd
import csv


def inp(ques, ans=None, int_only=False, yn=False, rep_msg=None, rep=False, no_ans=False):
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
    return res if not yn and not ans or yn and res in ['yes', 'no'] or ans and res in ans else inp(ques, ans=ans, yn=yn,
                                                                                                   rep_msg=rep_msg,
                                                                                                   rep=True,
                                                                                                   no_ans=no_ans)


def login_signup():
    users = pd.read_csv('UsersandSettings.csv', encoding="windows_1258")

    los = inp('Would you like to log in or sign up (log in, sign up)? ', ['log in', 'sign up'],
              rep_msg='Please enter either "log in" or "sign up"')

    if los == 'sign up':
        userinfo = new_user(users, 'UsersandSettings.csv')
    if los == 'log in':
        userinfo = login(users, 'UsersandSettings.csv')

