import json
import os
import multiprocessing
import win32com.client
import win32gui
import curses

from loguru import logger
from login import auto_login
from task import daily_tasks
from utils import get_hwnds, get_json_file, push_msg, openmore, init_log_dir, PauseableThread
from multiprocessing import Value, Pool, Lock, Queue, Manager
from time import sleep
from zhuogui import main as loop_zhuogui

logger_format = ("<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                 "<level>{level: <6}</level> | "
                 "{extra[hwnd]: <8} - {extra[name]: <10} - {message}")

logger.configure(handlers=[{
    "sink": "app.log",
    "encoding": "utf-8",
    "enqueue": True,
    "backtrace": True,
    "catch": True,
    "format": logger_format
}, {
    "sink": "error.log",
    "level": "ERROR",
    "encoding": "utf-8",
    "format": logger_format
}],
                 extra={
                     "hwnd": "",
                     "name": "",
                     "lock": None,
                     "process_id": 0
                 })


def err_call_back(err):
    print(f'出错啦~ error：{str(err)}')


def init_terminal_print(queue):
    stdscr = curses.initscr()
    curses.curs_set(0)

    while True:
        try:
            id, message = queue.get()
            stdscr.move(id, 0)
            stdscr.clrtoeol()
            stdscr.refresh()
            string = str(id) + " | " + message
            string = string.ljust(80, '.')
            stdscr.addstr(id, 0, string)
        except queue.Empty:
            pass

        stdscr.refresh()


def exit_terminal_print():
    curses.curs_set(1)
    curses.endwin()


def start(groupConfig=[]):
    try:
        if not groupConfig:
            hwnds = get_hwnds()
            account_json = get_json_file('auto_login')
            account_json = json.loads(account_json)["accounts"]
            config = [[row['config'] for row in group]
                      for group in account_json][0]
            groupConfig = [{
                "hwnd": hwnds[i],
                "config": config[i]
            } for i in range(len(hwnds))]

        manager = Manager()
        memory = manager.Value('i', 0)
        lock = manager.Lock()
        queue = manager.Queue()

        pool = Pool(5)

        for i, row in enumerate(groupConfig):
            pool.apply_async(daily_tasks,
                             args=(row['hwnd'], row['config'], memory, lock,
                                   queue, i),
                             error_callback=err_call_back)
            sleep(1)

        terminal_print = PauseableThread(target=init_terminal_print,
                                         args=(queue, ),
                                         stop_func=exit_terminal_print)
        terminal_print.start()

        pool.close()
        pool.join()

        terminal_print.stop_thread()

        push_msg('已全部完成')
    except Exception as e:
        print(e)


def stop(hwnd):
    global threads
    if hwnd not in threads:
        return
    threads[hwnd].stop_thread()

    del threads[hwnd]


def end():
    pass


def onekey(config=[]):
    logger.info("开始一键")
    account_json = get_json_file('auto_login')
    account_json = json.loads(account_json)["accounts"]
    if not account_json:
        logger.info("没有配置自动登录账号")
    if not config:
        config = [[row['config'] for row in group]
                  for group in account_json][0]
    for group in account_json:
        hwnds = get_hwnds()
        openmore(hwnds)
        hwnds = get_hwnds()

        auto_login(group, hwnds)

        groupConfig = [{
            "hwnd": hwnd,
            "config": config[i]
        } for i, hwnd in enumerate(hwnds)]

        start(groupConfig)


shell = win32com.client.Dispatch("WScript.Shell")


def top(hwnd):
    shell.SendKeys('%')
    win32gui.SetForegroundWindow(hwnd)


func_map = {
    # "gameWindows": get_hwnd_list,
    "onekey": onekey,
    "openmore": openmore,
    "auto_login": auto_login,
    "start": start,
    "stop": stop,
    "end": end,
    "top": top,
}

func_list = [
    None, onekey, openmore, auto_login, start, stop, end, loop_zhuogui
]


@logger.catch()
def call_method(param, **kwds):
    func_map.get(param, lambda: print("Invalid parameter"))(**kwds)


def command_selection():
    while True:
        print("请选择你的选项:")
        print("1. 一键日常")
        print("2. 多开")
        print("3. 自动登录")
        print("4. 开始日常")
        print("6. 结束脚本")
        print("7. 队长无限鬼")
        print("0. 退出")
        choice = int(input("你的选择是: "))
        if choice == 0:
            break
        elif choice in range(len(func_list)):
            func_list[choice]()
        else:
            print("无效选项:", choice)


if __name__ == "__main__":
    init_log_dir()

    import argparse

    multiprocessing.freeze_support()

    parser = argparse.ArgumentParser()
    parser.add_argument("func_name", nargs="?", choices=func_map.keys())
    parser.add_argument("--params", dest='kwargs', nargs='*')
    args = parser.parse_args()

    try:
        if args.func_name:
            if args.kwargs:
                kwargs = {
                    k: v
                    for k, v in (kv_str.split('=') for kv_str in args.kwargs)
                }
            else:
                kwargs = {}
            call_method(args.func_name, **kwargs)
        else:
            command_selection()
            # start()
    except Exception as e:
        # os._exit(0)
        logger.exception(e)