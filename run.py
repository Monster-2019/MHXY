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
def daily_tasks(hwnd):
    hwnd = str(hwnd)
    capture = CaptureScreen(hwnd, hwnd)
    match = Match(hwnd)
    btn = Btn(hwnd)
    smc = SMC(capture, match, btn)

    adb = {
        'screen': hwnd,
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

    name, level, gold, silver = complex_task.get_info()

    adb["name"] = name

    complex_task = Complex(adb)

    complex_task.singin()

    bangpai = Bangpai(adb, complex_task.task_finished)

    bangpai.check_in()

    # GengZhong(adb, complex_task.task_finished).start()

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

    if datetime.now().hour >= 11:
        SJ(adb, complex_task.task_finished).start()

    if week <= 4 and datetime.now().hour >= 17:
        KJ(adb, complex_task.task_finished).start()

    Yunbiao(adb, complex_task.task_finished).start()

    complex_task.get_hyd()

    # GengZhong(adb, complex_task.task_finished).start(True)

    complex_task.clean()

    print(f"{name}账号完成")


if __name__ == "__main__":
    hwnd = win32gui.FindWindow(None, '《梦幻西游》手游')
    daily_tasks(str(hwnd))