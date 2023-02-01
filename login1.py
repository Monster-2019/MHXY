import win32gui, win32con, win32api, win32com.client
from loguru import logger
from time import sleep
import os

from cutScreen import CScreen
from match import Match
from btn import Btn

from config import user

SHELL = win32com.client.Dispatch("WScript.Shell")


def SetForegroundWindowMy(hwnd):
    SHELL.SendKeys('%')
    win32gui.SetForegroundWindow(hwnd)


mnq_hwnd = None
mnq_screen = None
mnq_match = None
mnq_btn = None


def mnqInit():
    os.system('start C:\\leidian\\LDPlayer4\\dnplayer.exe')
    sleep(10)

    while True:
        sleep(0.5)
        tem = win32gui.FindWindow(None, '雷电模拟器')
        mnq_hwnd = win32gui.FindWindowEx(tem, None, 'RenderWindow', None)
        if mnq_hwnd:
            break

    mnq_screen = CScreen(mnq_hwnd).cutScreen
    mnq_match = Match('mnq').matchTem
    mnq_btn = Btn(mnq_hwnd)

    SetForegroundWindowMy(mnq_hwnd)

    while True:
        sleep(1)
        mnq_screen()
        mhxy = mnq_match('mnq_mhxy')
        if mhxy:
            mnq_btn.LBtn(mhxy)
            break

    sleep(8)
    mnq_btn.LBtn(((500, 250), (20, 20)))

    while True:
        mnq_screen()
        sm = mnq_match('mnq_sm')
        if sm:
            sleep(3)
            break

    logger.info('模拟器初始化完成')


def mnq_login(account):
    login_step = ['mnq_sm', 'mnq_tk', account, 'mnq_dl']

    status = False
    while not status:
        for item in login_step:
            mnq_screen()
            coor = mnq_match(item)
            if coor:
                if item == 'mnq_tk':
                    mnq_btn.LBtn(coor, sleepT=1)

                    while True:
                        mnq_screen()
                        coor = mnq_match('mnq_dl')
                        if coor != 0:
                            break
                        else:
                            mnq_btn.LBtn(((100, 160), (2, 2)))
                            # self.mnqBtn.LBtn(((650, 480), (2, 2)))
                        sleep(0.5)

                    sleep(0.5)
                    mnq_btn.LBtn(((460, 190), (2, 2)))

                else:
                    mnq_btn.LBtn(coor)
                    if item == 'mnq_dl':
                        status = True
                        break

            else:
                if item == account:
                    for index in range(3):
                        mnq_screen()
                        coor = mnq_match(item)
                        if coor != 0:
                            break
                        mnq_btn.DBtn((460, 340), (460, 240))
                        sleep(0.5)

    logger.info(f'模拟器{account}登录完成')


def game_login(hwnd, server):
    screen = CScreen(hwnd).cutScreen
    match = Match('mnq').matchTem
    btn = Btn(hwnd)

    login_step = ['dl_qd', 'dl_js', 'dl_djxf', 'dl_yyjs', server]
    status = False
    while not status:
        for item in login_step:
            screen()
            res = match(item)
            if res:
                btn.LBtn(res)
                if item == server:
                    status = True
                    break

    logger.info(f'已登录{server}服务器')


def login(group, hwnd_list):
    login_list = []
    for hwnd in hwnd_list:
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

        game_hwnd = hwnd_list[i]

        win32api.SendMessage(game_hwnd, win32con.WM_KEYDOWN, 27, 0)
        SetForegroundWindowMy(game_hwnd)
        game_btn = Btn(game_hwnd)
        game_btn.LBtn(((485, 483), (57, 15)))
        sleep(1)

        login_window_hwnd = win32gui.FindWindow('MPAY_LOGIN', None)
        login_window_hwnd_screen = CScreen(login_window_hwnd,
                                           './images/mnq/').cutScreen
        login_window_hwnd_screen()

        SetForegroundWindowMy(mnq_hwnd)

        mnq_login(login_account)

        sleep(1)

        game_login(hwnd_list[i], login_server)

        logger.info(f'账号 {login_account} 游戏登陆完成')

        os.system('taskkill /F /IM dnplayer.exe')