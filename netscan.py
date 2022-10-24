import os
import time
import curses
from curses.textpad import Textbox, rectangle



menu = ['IP', 'Exit']

def print_menu(stdscr, selected_row_idx):
    h, w = stdscr.getmaxyx()
    stdscr.clear()

    for idx, row in enumerate(menu):
        x = w//2 - len(row)//2
        y = h//2 - len(menu)//2 + idx

        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)

    stdscr.refresh()

def main(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)

    h, w = stdscr.getmaxyx()
    stdscr.clear()

    text = "you pressed {}"

    x = w//2 - len(text)//2
    y = h//2 - len(menu)//2

    current_row_idx = 0

    print_menu(stdscr, current_row_idx)

    while 1:
        key = stdscr.getch()

        stdscr.clear()

        if key == curses.KEY_UP and current_row_idx > 0:
            current_row_idx -= 1
        elif key == curses.KEY_DOWN and current_row_idx < len(menu)-1:
            current_row_idx += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            stdscr.refresh()
            stdscr.getch()

            if current_row_idx == len(menu)-1:
                break
            elif current_row_idx == len(menu)-2:
                win = curses.newwin(1, 18, y, x)
                box = Textbox(win)
                stdscr.addstr(y-2, x-10, "Enter Ip. (Press CTRL + G to exit textbox)")
                rectangle(stdscr, y-1, x-1, y+1, x+20)
                stdscr.refresh()
                box.edit()
                ip = box.gather()
                stdscr.clear()
                stdscr.addstr(y, x-3, "Set Ip to: ")
                stdscr.addstr(y, x+9, ip)
                stdscr.getch()
                stdscr.clear()
                stdscr.refresh()
                stdscr.addstr(y, x-1, " ")
                os.system('nmap -sV ' + ip + " -Pn -oN /home/kali/Desktop/nmap_result")
                stdscr.clear()
                stdscr.addstr(y, x, "Press any key to view output!")
                stdscr.getch()
                stdscr.clear()

                with open('/home/kali/Desktop/nmap_result', 'r') as file:
                    nmap_output = file.read()

                stdscr.addstr(0, 0, nmap_output)
                stdscr.refresh()
                stdscr.getch()
                os.system('rm /home/kali/Desktop/nmap_result')



                stdscr.refresh()

        print_menu(stdscr, current_row_idx)

        stdscr.refresh()



curses.wrapper(main)
