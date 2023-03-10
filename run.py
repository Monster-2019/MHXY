import argparse
import configparser
import os
from datetime import datetime
from multiprocessing import Manager, Pipe, Pool
from time import sleep

import win32com.client
import win32gui
from apscheduler.schedulers.blocking import BlockingScheduler
from loguru import logger

from baotu import Baotu
from btn import Btn
from capture import CaptureScreen
from complex import Complex
from config.user import ACCTZU
from fuben import FuBen
from kjxs import KJ
from login import login
from match import Match
from mijing import Mijing
from shimen import Shimen
from sjqy import SJ
from smc import SMC
from utils import hide_login, push_msg
from yunbiao import Yunbiao
from zhuogui import Zhuogui
from bangpai import Bangpai
from gengzhong import GengZhong

conf = configparser.ConfigParser()

conf.read('config.ini', encoding='utf-8')

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

    os.system(f"start {conf.get('software_path', 'ssk')}")
    sleep(2)

    while True:
        hwnd = win32gui.FindWindow(None, 'UnityWndClass')
        if hwnd:
            break
        sleep(1)

    btn = btn(hwnd)
    for i in range(5 - len(hwnd_list)):
        btn.l(((350, 150), (2, 2)))
        sleep(3)

    os.system('taskkill /F /IM mhxy.exe')
    return


today = datetime.today()
week = today.isoweekday()
shell = win32com.client.Dispatch("WScript.Shell")


@logger.catch()
def daily_tasks(screen, hwnd, lock, manager_dict, manager_list, pipe):
    capture = CaptureScreen(hwnd, screen)
    match = Match(screen)
    btn = Btn(hwnd, lock)
    smc = SMC(capture, match, btn)

    adb = {
        'screen': screen,
        'hwnd': hwnd,
        'capture': capture,
        'match': match,
        'btn': btn,
        'smc': smc,
    }

    try:
        shell.SendKeys('%')
        win32gui.SetForegroundWindow(hwnd)
        hide_login()
    except Exception as e:
        print(e)

    complex_task = Complex(adb)

    complex_task.get_info()

    complex_task.singin()

    bangpai = Bangpai(adb, complex_task.task_finished)

    bangpai.check_in()

    GengZhong(adb, complex_task.task_finished).start()

    # if screen == '0':
    #     complex_task.join_team_leader()
    # else:
    #     complex_task.join_team_player()

    # if week >= 6:
    #     if screen == '0':
    #         Zhuogui(adb, complex_task.task_finished, pipe).leader()
    #     else:
    #         Zhuogui(adb, complex_task.task_finished, pipe).player()

    # if screen == '0':
    #     FuBen(adb, complex_task.task_finished, pipe).leader('ecy')
    # else:
    #     FuBen(adb, complex_task.task_finished, pipe).player()

    Shimen(adb, complex_task.task_finished).start()

    Baotu(adb, complex_task.task_finished).start()

    Mijing(adb, complex_task.task_finished).start()

    SJ(adb, complex_task.task_finished).start()

    KJ(adb, complex_task.task_finished).start()

    Yunbiao(adb, complex_task.task_finished).start()

    GengZhong(adb, complex_task.task_finished).start(True)

    print(f"{screen}账号完成")

    # getInfo()


def start(single=False):
    try:
        import pythoncom
        pythoncom.CoInitialize()

        for index in range(len(ACCTZU)):
            GROUP_NO = index + 1
            hwnd_list = getHwndList()

            if not single:
                openGame(hwnd_list)

            hwnd_list = getHwndList()
            logger.info(f'开始第 {GROUP_NO} 组号')

            if not single:
                login(index, hwnd_list)

            lock = Manager().Lock()
            manager_dict = Manager().dict()
            manager_list = Manager().list([])
            pipe = Pipe()

            game_count = len(hwnd_list)
            p = Pool(game_count)
            for i in range(game_count):
                p.apply_async(daily_tasks, (str(i), hwnd_list[i], lock,
                                            manager_dict, manager_list, pipe))
            p.close()
            p.join()

            msg = f'完成第{GROUP_NO}组号, 活跃：{",".join(manager_list)}'
            logger.info(f'完成第{GROUP_NO}组号')
            push_msg(msg)

        logger.info(f'已完成全部账号')
    except Exception as e:
        print(e)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    # parser.add_argument('--shutdown', '-s', action='store_true', default=False)
    parser.add_argument('--time', '-t', type=str)
    parser.add_argument('--self', '-s', action='store_true', default=False)
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