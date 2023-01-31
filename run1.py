from apscheduler.schedulers.blocking import BlockingScheduler
from multiprocessing import Pool, Manager
from loguru import logger
from time import sleep
import os
import win32gui, win32com.client
import argparse

from config import user

from login1 import login

logger.add('run.log',
           rotation="1 week",
           encoding="utf-8",
           retention="7 days",
           backtrace=True,
           catch=True,
           enqueue=True)


def getHwndList():
    hwndList = []
    isFinish = False
    hwnd = 0
    while not isFinish:
        if not isFinish and hwnd == 0:
            hwnd = win32gui.FindWindow(None, "《梦幻西游》手游")
        else:
            hwnd = win32gui.FindWindowEx(None, hwnd, None, "《梦幻西游》手游")
        if hwnd:
            hwndList.append(hwnd)
        else:
            isFinish = True

    return hwndList


def openGame(hwndList=[]):
    if len(hwndList) == 5:
        return

    os.system('start C:\\Users\\DX\\Desktop\\duokai\\mhxy.exe')
    sleep(2)

    while True:
        hwnd = win32gui.FindWindow(None, 'UnityWndClass')
        if hwnd:
            break
        sleep(1)

    btn = btn(hwnd)
    for i in range(5 - len(hwndList)):
        btn.LBtn(((350, 150), (2, 2)))
        sleep(3)

    os.system('taskkill /F /IM mhxy.exe')
    return


def start(single=False):
    import pythoncom
    pythoncom.CoInitialize()

    for index in range(len(user.ACCTZU)):
        GROUP_NO = index + 1
        hwndList = getHwndList()
        if user.ACCTZU[index]['status']:
            if not single:
                openGame(hwndList)

            hwndList = getHwndList()
            logger.info(f'开始第 {GROUP_NO} 组号')
            login(index, hwndList)

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