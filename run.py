import argparse
import os
from datetime import datetime
from multiprocessing import Manager, Pool
from time import sleep

import win32com.client
import win32gui
from apscheduler.schedulers.blocking import BlockingScheduler
from loguru import logger

from btn import Btn
from capture import CaptureScreen
from complex import Complex
from config.user import ACCTZU
from login import login
from match import Match
from smc import SMC
from utils import hide_login, push_msg

logger.add('run.log',
           rotation="1 week",
           encoding="utf-8",
           retention="7 days",
           backtrace=True,
           catch=True,
           enqueue=True)


def getHwndList():
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

    return hwnd_list


def openGame(hwnd_list=[]):
    if len(hwnd_list) == 5:
        return

    os.system('start C:\\Users\\DX\\Desktop\\duokai\\mhxy.exe')
    sleep(2)

    while True:
        hwnd = win32gui.FindWindow(None, 'UnityWndClass')
        if hwnd:
            break
        sleep(1)

    btn = btn(hwnd)
    for i in range(5 - len(hwnd_list)):
        btn.LBtn(((350, 150), (2, 2)))
        sleep(3)

    os.system('taskkill /F /IM mhxy.exe')
    return


today = datetime.today()
week = today.isoweekday()
shell = win32com.client.Dispatch("WScript.Shell")


def daily_tasks(screen, hwnd, lock, manager_dict, manager_list):
    capture = CaptureScreen(hwnd, screen)
    match = Match(screen)
    btn = Btn(hwnd, lock)
    smc = SMC(capture, match, btn).smc

    try:
        shell.SendKeys('%')
        win32gui.SetForegroundWindow(hwnd)
        hide_login()
    except Exception as e:
        print(e)

    complex_task = Complex(capture, match, btn, smc)

    complex_task.get_info()

    complex_task.singin()

    if screen == '0':
        complex_task.join_team_leader()
    else:
        complex_task.join_team_player()

    # getInfo()


def start(single=False):
    import pythoncom
    pythoncom.CoInitialize()

    for index in range(len(ACCTZU)):
        GROUP_NO = index + 1
        hwnd_list = getHwndList()

        if not single:
            openGame(hwnd_list)

        hwnd_list = getHwndList()
        logger.info(f'开始第 {GROUP_NO} 组号')
        login(index, hwnd_list)

        lock = Manager().Lock()
        manager_dict = Manager().dict()
        manager_list = Manager().list([])

        game_count = len(hwnd_list)
        p = Pool(game_count)
        for i in range(game_count):
            p.apply_async(
                daily_tasks,
                (str(i), hwnd_list[i], lock, manager_dict, manager_list))
        p.close()
        p.join()

        msg = f'完成第{GROUP_NO}组号, 活跃：{",".join(manager_list)}'
        logger.info(f'完成第{GROUP_NO}组号')
        push_msg(msg)

    logger.info(f'已完成全部账号')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parser.add_argument('--shutdown', '-s', action='store_true', default=False)
    parser.add_argument('--time', '-t', type=str)
    parser.add_argument('--self', action='store_true', default=False)
    args = parser.parse_args()

    if args.time:
        time = args.time.split(":")
        hour, minute = time
        logger.info(f'开始定时任务，时间为{hour}时{minute}分')
        scheduler = BlockingScheduler()
        scheduler.add_job(start,
                          'cron',
                          hour=hour,
                          minute=minute,
                          args=args.self)
        scheduler.start()
    else:
        start(args.self)