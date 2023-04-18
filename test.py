import curses
from time import sleep
from random import randint

stdsrc = curses.initscr()
stdsrc.addstr(0, 0, ('测试' * 20))  # 将字符串转换为 Unicode 编码
string_base = '测试'

count = 20

while True:
    string = string_base * randint(1, 20)
    stdsrc.move(1, 0)
    stdsrc.clrtoeol()
    stdsrc.refresh()
    string = string.ljust(80, '.')
    stdsrc.addstr(1, 0, string)  # 将字符串转换为 Unicode 编码
    stdsrc.refresh()
    sleep(1)
    count -= 1
    if count == 0:
        break

curses.endwin()