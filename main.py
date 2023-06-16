import json
import multiprocessing
import win32com.client
import win32gui
import logging

from loguru import logger
from login import auto_login
from task import daily_tasks
from utils import get_hwnds, get_json_file, push_msg, openmore, init_log_dir
from multiprocessing import Manager, Process
from time import sleep
from zhuogui import main as loop_zhuogui
from rich.live import Live
from rich.table import Table
from rich.console import Console


logger_format = ("<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                 "<level>{level: <6}</level> | "
                 "{message}")

logger = logging.getLogger('mhxy')
logger.setLevel(logging.INFO)

def generate_table(tableData):
    table = Table()
    table.add_column('ID')
    table.add_column('Name')
    table.add_column('Level')
    table.add_column('Gold')
    table.add_column('Sliver')
    table.add_column('Status')

    for row in tableData:
        table.add_row(*row)

    return table


def init_terminal_print(queue):
    tabledata = [
        ['0' if i == 0 else "" for i in range(6)],
        ['1' if i == 0 else "" for i in range(6)],
        ['2' if i == 0 else "" for i in range(6)],
        ['3' if i == 0 else "" for i in range(6)],
        ['4' if i == 0 else "" for i in range(6)],
    ]

    console = Console()
    console.clear()
    # logger = logging.getLogger('mhxy')

    with Live(generate_table(tabledata), refresh_per_second=20) as live:
        try:
            while True:
                message = queue.get()
                msg = message.msg
                # print(111, msg, message)
                if msg is None:
                    break
                id = message.id
                if msg[0] == '(':
                    fm_message = eval(msg)
                    for i, val in enumerate(fm_message):
                        tabledata[id][i + 1] = str(val)
                else:
                    tabledata[id][5] = str(msg)

                live.update(generate_table(tabledata))

        except Exception as e:
            print('e', e)
        

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
        process_list = []

        for i, row in enumerate(groupConfig):
            p = Process(target=daily_tasks, args=(row['hwnd'], row['config'], memory, lock,
                                   queue, i))
            p.start()
            process_list.append(p)
            sleep(1)

        terminal_print = Process(target=init_terminal_print, args=(queue, ))
        terminal_print.start()
        
        for process in process_list:
            process.join()

        terminal_print.terminate()

        push_msg('已全部完成')
    except KeyboardInterrupt:
        for p in process_list:
            p.terminate()
        exit(0)


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


def call_method(param, **kwds):
    func_map.get(param, lambda: print("Invalid parameter"))(**kwds)


def command_selection():
    choice = None
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
            break
        else:
            print("无效选项:", choice)

    func_list[choice]()


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