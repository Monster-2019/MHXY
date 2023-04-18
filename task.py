import configparser
import json
import os
from datetime import datetime
from time import sleep

import loguru
import win32com.client
import win32gui

from bangpai import Bangpai
from baotu import Baotu
from btn import Btn
from capture import CaptureScreen
from complex import Complex
from fuben import FuBen
from gengzhong import GengZhong
from gongfang import Gongfang
from kjxs import KJ
from match import Match
from mijing import Mijing
from shimen import Shimen
from sjqy import SJ
from smc import SMC
# from utils import hide_login
from yunbiao import Yunbiao
from zhuogui import Zhuogui

week = datetime.now().isoweekday()
shell = win32com.client.Dispatch("WScript.Shell")

conf = configparser.ConfigParser()
path = os.path.join(os.getcwd(), "config.ini")

logger = loguru.logger


@logger.catch()
def daily_tasks(hwnd,
                config_file=None,
                memory=None,
                lock=None,
                queue=None,
                process_id=0):
    with open(f'config/{config_file}.json', 'r') as f:
        json_data = f.read()
        config = json.loads(json_data)

    loguru.logger.add(lambda message: queue.put(
        (message.record["extra"]["process_id"], message.record["message"])),
                      format="{message}")

    hwnd = str(hwnd)
    capture = CaptureScreen(hwnd, hwnd)
    match = Match(hwnd)
    btn = Btn(hwnd, lock)
    smc = SMC(capture, match, btn)

    adb = {
        'screen': hwnd,
        'hwnd': hwnd,
        'capture': capture,
        'match': match,
        'btn': btn,
        'smc': smc,
    }

    # 置顶，隐藏登录窗口
    # try:
    #     shell.SendKeys('%')
    #     win32gui.SetForegroundWindow(hwnd)
    #     hide_login()
    # except Exception as e:
    #     print(e)

    name, level, gold, silver = Complex(adb).get_info()

    logger = loguru.logger.bind(hwnd=hwnd, name=name, process_id=process_id)

    logger.info(f"账号:{name}, 等级:{level}级, 金币:{gold}, 银币:{silver}")

    adb["logger"] = logger

    complex_task = Complex(adb)

    adb["task_finished"] = complex_task.task_finished

    complex_task.leave_team()

    complex_task.singin()

    bangpai = Bangpai(adb)

    bangpai.check_in()
    level = level if level else 69

    if int(level) >= 60:
        GengZhong(adb).start()

    if "leader" in config and config['leader'] != None:
        if config['leader']:
            memory.value = 1
            complex_task.join_team_leader()

            sleep(1)

            btn.hotkey('zz', sleep_time=1)
            btn.l_key('zr2', sleep_time=0.5)
            btn.r()

            if week in [3, 5]:
                FuBen(adb).leader('lyrm')

            if week in [2, 6, 7]:
                FuBen(adb).leader('lls')

            if week in [1, 4, 7]:
                FuBen(adb).leader('ecy')

            if week in [1, 2, 3, 4, 5, 6]:
                FuBen(adb).leader('jcx')

            sleep(1)

            btn.hotkey('zz', sleep_time=1)
            btn.l_key('zr1', sleep_time=0.5)
            btn.r()

            Zhuogui(adb).leader()

            memory.value = 2

            complex_task.leave_team()

        else:
            logger.info('')
            while True:
                if memory.value == 1:
                    break
                sleep(1)

            complex_task.join_team_player()

            while True:
                if memory.value == 2:
                    break
                sleep(1)

            smc('sb', sleep_time=0.5)

            complex_task.leave_team()

    if config["sm"]:
        Shimen(adb).start()

    if config["bt"]:
        Baotu(adb).start()

    if config["mj"]:
        Mijing(adb).start()

    if datetime.now().hour >= 11 and config["sj"]:
        SJ(adb).start()

    if week <= 5 and datetime.now().hour >= 17 and config["kj"]:
        KJ(adb).start()

    if config["yb"]:
        Yunbiao(adb).start()

    complex_task.get_hyd()

    if int(level) >= 60:
        GengZhong(adb).start(True)

    complex_task.clean()

    conf.read(path, encoding='utf-8')

    bp = int(conf.get('public', 'bp'))
    if bp and week == bp:
        bangpai.start()

    gf = int(conf.get('public', 'gf'))
    if gf and week == gf:
        Gongfang(adb).start()

    logger.info(f"账号完成")

    return 1


if __name__ == "__main__":
    hwnd = win32gui.FindWindow(None, '梦幻西游：时空')
    daily_tasks(str(hwnd))