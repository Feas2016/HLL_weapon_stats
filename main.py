import io
import re
import csv
import PySimpleGUI as sg
import os
import datetime


def checkfile(filename):
    """Test of closed file with popup"""
    while True:  # 
        try:
            with open(filename, mode="w",
                        encoding='utf-8-sig') as w_file:
                break
        except:
            sg.popup(
                f'Pls close /{filename} file to continue')


def main(export_name, export_death_name):

    sg.theme('GreenTan')  # GUI
    layout = [[sg.Text('Select the .TXT file to process')],
              [sg.Text('Path to File'), sg.Input(
                  # 'F:/Programming/HLL_stats/log-file.txt'
              ), sg.FileBrowse('View')],
              [sg.OK(), sg.Quit('Exit')]]
    window = sg.Window('HLL Weapon Stats from logs', layout)
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            os._exit(0)
        if event in 'OK':
            path = values[0]
            if not os.path.isfile(path) is True:
                sg.popup('File not found: ', path)
            else:
                filename, file_extension = os.path.splitext(path)
                if file_extension not in ('.txt'):
                    sg.popup("It's not a .txt file: ",
                             filename + file_extension)
                else:
                    window.close()
                    break

    nick_list = []
    weapon_list = []
    list = ['Kill', 'Death', 'Weapon']
    log = (list,)
    d_count_us = 0
    d_count_ge = 0
    rem_minute = 0
    death_string = []
    death_log = (death_string,)

    # parsing file
    with io.open(path, encoding='utf-8') as file:
        for line in file:
            if not any(value in line for value in ('CHAT[', 'CONNECTED', 'TEAM KILL')):
                if 'KILL   ' in line:
                    # 21:27:58 - Sun, Jan 17
                    t = datetime.datetime.strptime(line[:line.find('    ')], '%H:%M:%S - %a, %b %d')
                    temp = re.sub(r'(.*) -> ', '', line)
                    
                    if not int(rem_minute) == int(t.minute):
                        if rem_minute == 0:
                            rem_t = t + datetime.timedelta(minutes=1)
                        death_string = [rem_t.strftime('%H:%M'), d_count_us, d_count_ge]
                        death_log += (death_string,)
                        d_count_us = 0
                        d_count_ge = 0
                        rem_t = t
                        rem_minute = t.minute
                    if "Allies" in temp:
                        d_count_us += 1
                    if "Axis" in temp:
                        d_count_ge += 1
                # print(d_count_us, d_count_ge, rem_minute, t.minute, temp)
                if '\n' not in line:    # fix last symbol
                    line += '\n'
                line = re.sub(r'(.*)KILL                ', '', line)
                nickname_kill = line[:line.find(') -> ')]
                nickname_kill = nickname_kill[:nickname_kill.find('Allies/')]
                nickname_kill = nickname_kill[:nickname_kill.find('(Axis/')]
                nickname_death = re.sub(r'(.*) -> ', '', line)
                nickname_death = nickname_death[:nickname_death.find(') with ')]
                nickname_death = nickname_death[:nickname_death.find('Allies/')]
                nickname_death = nickname_death[:nickname_death.find('(Axis/')]
                weapon = re.sub(r'(.*)\) with ', '', line)
                weapon = weapon[:weapon.find('\n')].replace(
                    'None', 'Tank/Arty')

                list = [nickname_kill, nickname_death, weapon]
                # it often happens that a person did not kill anyone
                nick_list += [nickname_death]   #
                weapon_list += [weapon]
                log += (list,)

            
    # print(log)

    # nick_list & weapon_list
    res = []
    for i in nick_list:
        if i not in res:
            res.append(i)
    nick_list = res
    nick_list.sort()
    res = []
    for i in weapon_list:
        if i not in res:
            res.append(i)
    weapon_list = res
    weapon_list.sort()

    tbl_label = ['#', 'Nickname in steam', 'Kills',
                 'Deaths', 'K/D', 'Best Gun']
    tbl_label.extend(weapon_list)

    # count in log
    checkfile(export_name)
    with open(export_name, mode="w", encoding='utf-8-sig') as w_file:
        file_writer = csv.writer(w_file, delimiter=";", lineterminator="\r",
                                 quoting=csv.QUOTE_NONE, quotechar='',
                                 escapechar=' ')
        file_writer.writerow(tbl_label)
        # print(tbl_label)
        for i in range(len(nick_list)):
            nick = nick_list[i]
            kills = 0
            deaths = 0
            weapon_list_count = []
            for k in range(len(weapon_list)):
                weapon_list_count.append(0)
            for j in range(len(log)):
                # print(log[j][0])
                if nick in log[j][1]:
                    deaths += 1
                if nick in log[j][0]:
                    kills += 1
                for k in range(len(weapon_list)):
                    if nick in log[j][0]:
                        if weapon_list[k] == log[j][2]:
                            weapon_list_count[k] += 1
                # search best gun
                best_gun = 0
                for k in range(len(weapon_list_count)):
                    # >= to fix Kar98 = Kar98_Sniper bug
                    if weapon_list_count[k] >= best_gun:
                        best_gun = weapon_list_count[k]
                        pos_best_gun = k
            # write to csv
            row = str(weapon_list_count).replace(
                ", ", ";").replace("[", "").replace("]", "")
            file_writer.writerow(
                [i + 1, nick, kills, deaths, f"'{round(kills / deaths, 2)}'",
                f'{weapon_list[pos_best_gun]} ({best_gun})', row])
    #         print(i + 1, nick, kills, deaths, f"'{round(kills / deaths, 2)}'",
    #             f'{weapon_list[pos_best_gun]} ({best_gun})', row)
    # os.startfile(export_name)

    checkfile(export_death_name)
    # Last death string
    death_string = [t.strftime('%H:%M'), d_count_us, d_count_ge]
    death_log += (death_string,)
    with open(export_death_name, mode="w", encoding='utf-8-sig') as w_file:
        file_writer = csv.writer(w_file, delimiter=";", lineterminator="\r",
                                 quoting=csv.QUOTE_NONE, quotechar='',
                                 escapechar=' ')
        file_writer.writerow(['Time','US Deaths', 'GE Deaths'])
        file_writer.writerows(reversed(death_log))


if __name__ == '__main__':
    export_name = 'HLL_weapon-stats.csv'
    export_death_name = 'HLL_death-stats.csv'

    main(export_name, export_death_name)
    sg.popup(f'Done. Check updated {export_name} and {export_death_name}')
