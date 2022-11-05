import UI.User_IO as UI


def main():
    while True:
        UI.login_cycle()
        cont = UI.inp('>>> Would you like to log in or exit the program ("log in", "exit")? ', ans=['log in', 'exit'],
                      rep_msg='Please input "log in" or "exit".')
        if cont == 'log in':
            UI.login_cycle()
        if cont == 'exit':
            return