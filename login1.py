import win32gui, win32con, win32api, win32com.client
from loguru import logger
from time import sleep
import os

from cutScreen import CScreen
from matchTem import Match
from btn import Btn

from config import user

SHELL = win32com.client.Dispatch("WScript.Shell")


def SetForegroundWindowMy(hwnd):
    SHELL.SendKeys('%')
    win32gui.SetForegroundWindow(hwnd)


def mnqInit():
    os.system('start C:\\leidian\\LDPlayer4\\dnplayer.exe')
    sleep(10)

    while True:
        sleep(0.5)
        tem = win32gui.FindWindow(None, '雷电模拟器')
        hwnd = win32gui.FindWindowEx(tem, None, 'RenderWindow', None)
        if hwnd:
            break

    screen = CScreen(hwnd).cutScreen
    temMatch = Match('mnq').matchTem
    btn = Btn(hwnd)

    SetForegroundWindowMy(hwnd)

    while True:
        sleep(1)
        screen()
        mhxy = temMatch('mnq_mhxy')
        if mhxy:
            btn.LBtn(mhxy)
            break

    sleep(8)
    btn.LBtn(((500, 250), (20, 20)))

    while True:
        screen()
        sm = temMatch('mnq_sm')
        if sm:
            sleep(3)
            break

    logger.info('模拟器初始化完成')


def login(group, hwndList):
    login_list = []
    for hwnd in hwndList:
        SetForegroundWindowMy(hwnd)
        login_hwnd = win32gui.FindWindow('MPAY_LOGIN', None)
        not_logged = win32gui.IsWindowVisible(login_hwnd)
        if hwnd and not_logged:
            login_list.append(hwnd)

    if len(login_list) == 5:
        mnqInit()
    else:
        logger.info('存在不同登录态，请检查')
        return os._exit()

    for i in range(5):
        login_account = user.ACCTZU[group]['acctList'][i]['account']
        login_server = user.ACCTZU[group]['acctList'][i]['server']

        game_hwnd = hwndList[i]

        win32api.SendMessage(game_hwnd, win32con.WM_KEYDOWN, 27, 0)
        SetForegroundWindowMy(game_hwnd)
        game_btn = Btn(game_hwnd)
        game_btn.LBtn(((485, 483), (57, 15)))
        sleep(1)

        login_window_hwnd = win32gui.FindWindow('MPAY_LOGIN', None)
        login_window_hwnd_screen = CScreen(login_window_hwnd,
                                           './images/mnq/').cutScreen
        login_window_hwnd_screen()
