import configparser
import os
from time import sleep
import shutil

import win32api
import win32com.client
import win32con
import win32gui
from loguru import logger

from btn import Btn
from capture import CaptureScreen
from config.user import ACCTZU
from match import Match

conf = configparser.ConfigParser()

conf.read('config.ini', encoding='utf-8')
LEIDIAN_PATH = conf.get('software_path', 'leidian')
SHARED_FOLDER = conf.get('software_path', 'shared_folder')

SHELL = win32com.client.Dispatch("WScript.Shell")


def SetForegroundWindowMy(hwnd):
    SHELL.SendKeys('%')
    win32gui.SetForegroundWindow(hwnd)


mnq_hwnd = None
mnq_capture = None
mnq_match = None
mnq_btn = None


def mnqInit():
    global mnq_hwnd
    global mnq_capture
    global mnq_match
    global mnq_btn
    leidianIsOpened = win32gui.FindWindow(None, '雷电模拟器')
    if leidianIsOpened:
        mnq_hwnd = win32gui.FindWindowEx(leidianIsOpened, None, 'RenderWindow', None)
        print(mnq_hwnd)
        mnq_capture = CaptureScreen(mnq_hwnd, 'mnq').capture
        mnq_match = Match('mnq').match_tem
        mnq_btn = Btn(mnq_hwnd)
        return

    os.system(f"start {LEIDIAN_PATH}")
    sleep(10)

    while True:
        sleep(0.5)
        tem = win32gui.FindWindow(None, '雷电模拟器')
        mnq_hwnd = win32gui.FindWindowEx(tem, None, 'RenderWindow', None)
        if mnq_hwnd:
            break

    mnq_capture = CaptureScreen(mnq_hwnd, 'mnq').capture
    mnq_match = Match('mnq').match_tem
    mnq_btn = Btn(mnq_hwnd)

    SetForegroundWindowMy(mnq_hwnd)

    while True:
        sleep(1)
        mnq_capture()
        mhxy = mnq_match('mnq_mhxy')
        if mhxy:
            mnq_btn.l(mhxy)
            break

    sleep(8)
    mnq_btn.l((500, 250, 20, 20))

    while True:
        mnq_capture()
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
            mnq_capture()
            coor = mnq_match(item, simi=0.999)
            if coor:
                if item == 'mnq_tk':
                    mnq_btn.l(coor, sleep_time=1)

                    while True:
                        mnq_capture()
                        coor = mnq_match('mnq_dl')
                        if coor:
                            break
                        else:
                            mnq_btn.l((140, 345, 2, 2))
                            # self.mnqBtn.l(((650, 480), (2, 2)))
                        sleep(0.5)

                    sleep(0.5)
                    mnq_btn.l((640, 300, 2, 2))
                    sleep(1)

                else:
                    mnq_btn.l(coor)
                    if item == 'mnq_dl':
                        status = True
                        break

            else:
                if item == account:
                    print(3333)
                    for index in range(3):
                        mnq_capture()
                        coor = mnq_match(item)
                        if coor:
                            break
                        mnq_btn.d_vertical((640, 300, 640, 100))
                        sleep(0.5)
            
            sleep(0.5)

    print(f'模拟器{account}登录完成')


def game_login(hwnd, server, screen):
    SetForegroundWindowMy(hwnd)
    print(server)
    screen = str(screen)
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
                    sleep(1)
                    btn.l(coor)
                    status = True
                    break
                
                else:
                    btn.l(coor)
            
            sleep(0.5)

    print(f'已登录{server}服务器')


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
        login_account = ACCTZU[group][i]['account']
        login_server = ACCTZU[group][i]['server']

        game_hwnd = hwnd_list[i]

        win32api.SendMessage(game_hwnd, win32con.WM_KEYDOWN, 27, 0)
        SetForegroundWindowMy(game_hwnd)
        game_btn = Btn(game_hwnd)
        game_btn.l((485, 483, 57, 15))
        sleep(1)

        login_window_hwnd = win32gui.FindWindow('MPAY_LOGIN', None)
        login_window_hwnd_screen = CaptureScreen(login_window_hwnd, 'mnq').capture
        login_window_hwnd_screen()
        shutil.copy('./images/mnq.jpg', SHARED_FOLDER + 'mnq.jpg')

        SetForegroundWindowMy(mnq_hwnd)

        mnq_login(login_account)

        sleep(1)

        game_login(hwnd_list[i], login_server, i)

        logger.info(f'账号 {login_account} 游戏登陆完成')

    os.system('taskkill /F /IM dnplayer.exe')

if __name__ == "__main__":
    hwnd_list = []
    is_finish = False
    hwnd = 0
    while not is_finish:
        if not is_finish and hwnd == 0:
            hwnd = win32gui.FindWindow(None, "《梦幻西游》手游")
        else:
            hwnd = win32gui.FindWindowEx(None, hwnd, None, "《梦幻西游》手游")
        if hwnd:
            hwnd_list.append(hwnd)
        else:
            is_finish = True

    login(0, hwnd_list)

    # hwnd = win32gui.FindWindow(None, "《梦幻西游》手游")

    # game_login(hwnd, 'h3_xyxt', 0)


    # CaptureScreen(3146098, 'mnq')()
    # res = Match('mnq')('h1', simi=0.999)
    # print(res)