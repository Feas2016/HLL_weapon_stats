import sys
import requests
import io
import re


def from_server():
    """Grabbing logs from Community RCON API
    """
    # The URL to the Community RCON API
    # Account credentials
    # The payload for requesting the logs
    
    URL = '=P' # '666.666.666.666:8010'
    username = 'Fiasco'
    password = '=P'
    time_from = '01-27-2021T20:00:00'   # '01-22-2021T16:00:00'
    time_till = '01-28-2021T01:04:00'
    limit = 999999  # 999999 - max?
    SERVER = '1'    # The server ID of the logs that should be used, must be a string

    URL = f'http://{URL}/api/'
    LOGIN = {'username': username, 'password': password}
    PAYLOAD = {'limit': limit, 'from': time_from, 'till': time_till}
    print(URL, LOGIN, PAYLOAD, SERVER)

    session = requests.session()
    session.post(URL + 'login', json=LOGIN)
    logs = session.get(URL + 'get_historical_logs', params=PAYLOAD).json()['result']

    print(session)
    print(logs)

def From_full_log(log_file):

    nick_list = []
    weapon_list = []
    list = ['Kill', 'Death', 'Weapon']
    log = {list,}

    # parsing file
    with io.open(log_file, encoding='utf-8') as file:
        for line in file:
            if not any(value in line for value in ('CHAT[', 'CONNECTED')):
                # CONNECTED also DISCONNECTED
                if '\n' not in line:    # fix last symbol
                    line += '\n'
                # print(line)
                line = re.sub(r'(.*)KILL                ', '', line)
                nickname_kill = line[:line.find(') -> ')]
                nickname_kill = nickname_kill[:nickname_kill.find('Allies/')]
                nickname_kill = nickname_kill[:nickname_kill.find('(Axis/')]
                nickname_death = re.sub(r'(.*) -> ', '', line)
                nickname_death = nickname_death[:nickname_death.find(') with ')]
                nickname_death = nickname_death[:nickname_death.find('Allies/')]
                nickname_death = nickname_death[:nickname_death.find('(Axis/')]
                weapon = re.sub(r'(.*)\) with ', '', line)
                weapon = weapon[:weapon.find('\n')].replace('None', 'Tank/Arty')

                list = [nickname_kill, nickname_death, weapon]
                # it often happens that a person did not kill anyone
                nick_list += [nickname_death]   #
                weapon_list += [weapon]
                log += (list,)
    print(log)

if __name__ == '__main__':
    log_file = 'f:\\Programming\\HLL_stats\\dev\\log-LS-EXD.txt'
    From_full_log(log_file)
