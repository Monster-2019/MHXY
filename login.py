import os
from time import sleep
from loguru import logger

import win32api
import win32com.client
import win32con
import win32gui

from btn import Btn
from capture import CaptureScreen
from match import Match
from smc import SMC

SHELL = win32com.client.Dispatch("WScript.Shell")


def SetForegroundWindowMy(hwnd):
    if not hwnd:
        return
    SHELL.SendKeys('%')
    win32gui.SetForegroundWindow(hwnd)


coor = {
    'dropdown': ((180, 180, 2, 2)),
    'prevpage': ((327, 250, 1, 1)),
    'nextpage': ((327, 318, 1, 1))
}


def game_login(hwnd, server):
    screen = str(hwnd)
    capture = CaptureScreen(hwnd, screen).capture
    match = Match(screen).match_tem
    btn = Btn(hwnd)

    login_step = ['dl_qd', 'dl_js', 'dl_djxf', 'dl_yyjs', server]
    status = False
    while not status:
        for item in login_step:
            capture()
            coor = match(item)
            if coor:
                if item == 'dl_djxf':
                    sleep(2)
                    btn.l(coor)

                elif item == server:
                    sleep(0.5)
                    btn.l(coor)
                    status = True
                    break

                else:
                    btn.l(coor)

            sleep(0.5)

    logger.info(f'已登录{server}服务器')


def auto_login(group, hwnds, **kwds):
    if len(hwnds) == 0:
        return

    login_list = []
    for hwnd in hwnds:
        SetForegroundWindowMy(hwnd)
        login_hwnd = win32gui.FindWindow('MPAY_LOGIN', None)
        not_logged = win32gui.IsWindowVisible(login_hwnd)
        if hwnd and not_logged:
            login_list.append(hwnd)

    if not login_list:
        logger.info('已经全部登录')
        return

    for i in range(len(hwnds)):
        login_account = group[i]['account']
        login_server = group[i]['server']

        game_hwnd = hwnds[i]

        win32api.SendMessage(game_hwnd, win32con.WM_KEYDOWN, 27, 0)
        SetForegroundWindowMy(game_hwnd)
        # game_btn = Btn(game_hwnd)
        # game_btn.l((485, 483, 57, 15))
        sleep(1)

        login_hwnd = win32gui.FindWindow('MPAY_LOGIN', None)
        login_screen = CaptureScreen(login_hwnd, str(login_hwnd))
        login_match = Match(str(login_hwnd))
        login_btn = Btn(login_hwnd)

        login_smc = SMC(login_screen, login_match, login_btn)

        login_btn.l(coor['dropdown'], sleep_time=0.5)
        login_btn.l(coor['prevpage'])

        select_account = login_smc(login_account, simi=0.998, sleep_time=0.5)

        if select_account:
            login_smc('join_game')
        else:
            login_btn.l(coor['nextpage'], sleep_time=0.5)
            select_account = login_smc(login_account, simi=0.998, sleep_time=0.5)
            login_smc('join_game')

        game_login(hwnds[i], login_server)

        logger.info(f'账号 {login_account} 游戏登陆完成')


if __name__ == "__main__":
    hwnds = []
    is_finish = False
    hwnd = 0
    while not is_finish:
        if not is_finish and hwnd == 0:
            hwnd = win32gui.FindWindow(None, "梦幻西游：时空")
        else:
            hwnd = win32gui.FindWindowEx(None, hwnd, None, "梦幻西游：时空")
        if hwnd:
            hwnds.append(hwnd)
        else:
            is_finish = True

    auto_login(0, hwnds)

    # hwnd = win32gui.FindWindow(None, "梦幻西游：时空")

    # game_login(hwnd, 'h3_xyxt', 0)

    # CaptureScreen(3146098, 'mnq')()
    # res = Match('mnq')('h1', simi=0.999)
    # logger.info(res)