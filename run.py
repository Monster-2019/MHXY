from datetime import datetime

import win32com.client
import win32gui
from loguru import logger

from baotu import Baotu
from btn import Btn
from capture import CaptureScreen
from complex import Complex
# from config.user import ACCTZU
# from fuben import FuBen
from kjxs import KJ
from match import Match
from mijing import Mijing
from shimen import Shimen
from sjqy import SJ
from smc import SMC
from utils import hide_login, push_msg
from yunbiao import Yunbiao
# from zhuogui import Zhuogui
from bangpai import Bangpai
from gengzhong import GengZhong

logger.add('run.log',
           rotation="1 week",
           encoding="utf-8",
           retention="7 days",
           backtrace=True,
           catch=True,
           enqueue=True)

week = datetime.now().weekday()
shell = win32com.client.Dispatch("WScript.Shell")


@logger.catch()
def daily_tasks(hwnd, lock=None, updateInfo=None, updateStatus=None):
    hwnd = str(hwnd)
    capture = CaptureScreen(hwnd, hwnd)
    match = Match(hwnd)
    btn = Btn(hwnd, lock)
    smc = SMC(capture, match, btn)

    global print
    original_print = print

    def updateState(*args, **kwds):
        updateStatus({"hwnd": hwnd, "status": args[0]})
        original_print(args[0])

    print = updateState

    adb = {
        'screen': hwnd,
        'hwnd': hwnd,
        'capture': capture,
        'match': match,
        'btn': btn,
        'smc': smc,
        "original_print": original_print,
        "print": print
    }

    try:
        shell.SendKeys('%')
        win32gui.SetForegroundWindow(hwnd)
        hide_login()
    except Exception as e:
        print(e)

    complex_task = Complex(adb)

    name, level, gold, silver = complex_task.get_info()

    updateInfo({
        "hwnd": hwnd,
        "name": name,
        "level": level,
        "gold": gold,
        "silver": silver,
    })

    adb["name"] = name

    complex_task = Complex(adb)

    adb["task_finished"] = complex_task.task_finished

    complex_task.singin()

    bangpai = Bangpai(adb)

    bangpai.check_in()

    # GengZhong(adb).start()

    # if screen == '0':
    #     complex_task.join_team_leader()
    # else:
    #     complex_task.join_team_player()

    # if week >= 6:
    #     if screen == '0':
    #         Zhuogui(adb, pipe).leader()
    #     else:
    #         Zhuogui(adb, pipe).player()

    # if screen == '0':
    #     FuBen(adb, pipe).leader('ecy')
    # else:
    #     FuBen(adb, pipe).player()

    Shimen(adb).start()

    Baotu(adb).start()

    Mijing(adb).start()

    if datetime.now().hour >= 11:
        SJ(adb).start()

    if week <= 4 and datetime.now().hour >= 17:
        KJ(adb).start()

    Yunbiao(adb).start()

    complex_task.get_hyd()

    # GengZhong(adb).start(True)

    complex_task.clean()

    print(f"{name}账号完成")

    print = original_print


if __name__ == "__main__":
    hwnd = win32gui.FindWindow(None, '《梦幻西游》手游')
    daily_tasks(str(hwnd))