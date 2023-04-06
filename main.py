import os
import configparser
import win32gui
import win32process
import psutil
import sys
import threading
import json
import loguru
from time import sleep
from btn import Btn
from task import daily_tasks
from login import login
from multiprocessing import Value
import tkinter as tk
from tkinter import filedialog
from utils import PauseableThread, push_msg

# f = open(os.devnull, 'w')
# sys.stdout = f
# sys.stderr = f

import eel

conf = configparser.ConfigParser()
path = os.path.join(os.getcwd(), "config.ini")
conf.read(path, encoding='utf-8')

# timing_time = ''


@eel.expose
def get_all_log():
    with open('app.log', 'r', encoding="utf-8") as log_file:
        log_content = log_file.read()
        return log_content


def update_logs():
    with open('app.log', 'r', encoding="utf-8") as log_file:
        log_content = log_file.read()
        eel.updateAllLog(log_content)


def eel_log_sink(message):
    hwnd = message.record["extra"]["hwnd"]
    msg = message.record["message"]
    eel.updateLog(hwnd, msg)
    update_logs()


logger_format = ("<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
                 "<level>{level: <6}</level> | "
                 "{extra[hwnd]: <8} - {extra[name]: <10} - {message}")

with open("app.log", mode="w", encoding="utf-8"):
    pass

loguru.logger.configure(handlers=[{
    "sink": "app.log",
    "encoding": "utf-8",
    "enqueue": True,
    "backtrace": True,
    "catch": True,
    "format": logger_format
}, {
    "sink": eel_log_sink,
    "enqueue": True,
    "backtrace": True,
}],
                        extra={
                            "hwnd": "",
                            "name": ""
                        })

logger = loguru.logger.bind(hwnd=0)


@eel.expose
def get_hwnd_list():
    # 查找所有标题为title的窗口句柄
    handles = []

    def callback(hwnd, handles):
        if win32gui.IsWindowVisible(hwnd) and not win32gui.IsIconic(
                hwnd) and '梦幻西游：时空' in win32gui.GetWindowText(hwnd):
            handles.append({"hwnd": hwnd})

        return True

    win32gui.EnumWindows(callback, handles)

    for handle in handles:
        handle['start_time'] = get_start_time(handle['hwnd'])

    handles = sorted(handles, key=lambda d: d['start_time'])

    handles = [item["hwnd"] for item in handles]

    return handles


def get_start_time(hwnd):
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    process = psutil.Process(pid)
    create_time = process.create_time()
    return create_time


@eel.expose
def get_software_path():
    path = conf.items('software_path')
    return path


@eel.expose
def set_software_path(path):
    for key, val in path.items():
        conf.set('software_path', key, val)
    conf.write(open('config.ini', 'w'))


@eel.expose
def set_software_dir():
    root = tk.Tk()
    root.attributes('-topmost', True)  # Display the dialog in the foreground.
    root.iconify()  # Hide the little window.
    folder_path = filedialog.askdirectory()
    root.destroy()
    return folder_path


@eel.expose
def set_software_file():
    root = tk.Tk()
    root.attributes('-topmost', True)  # Display the dialog in the foreground.
    root.iconify()  # Hide the little window.
    soft_path = filedialog.askopenfilename()
    root.destroy()
    return soft_path


@eel.expose
def get_auto_login_json():
    with open('config/auto_login.json', 'r') as f:
        json_data = f.read()
        data = json.loads(json_data)
        formatted_data = json.dumps(data, indent=2)
    return formatted_data


@eel.expose
def set_auto_login_json(json_data):
    with open('config/auto_login.json', 'w') as f:
        json.dump(json_data, f, indent=2)


def init_auto_login_json():
    if not os.path.isfile('config/auto_login.json'):
        with open('config/auto_login.json', 'w') as f:
            json.dump({"accounts": []}, f)


threads = dict()


def overopen(hwnd_list=[]):
    if len(hwnd_list) == 5:
        logger.info('已打开客户端，退出软件')
        return

    os.system(f"start {conf.get('software_path', 'ssk')}")
    sleep(2)

    while True:
        hwnd = win32gui.FindWindow(None, 'UnityWndClass')
        if hwnd:
            break
        sleep(1)

    btn = Btn(hwnd)
    for i in range(5 - len(hwnd_list)):
        btn.l(((350, 150, 2, 2)))
        sleep(3)

    logger.info('客户端打开完成')
    os.system('taskkill /F /IM mhxy.exe')
    return


@eel.expose
def stop(hwnd):
    global threads
    if hwnd not in threads:
        return
    threads[hwnd].stop_thread()


@eel.expose
def stopAll(hwnds):
    if not hwnds:
        hwnds = get_hwnd_list()
    for hwnd in hwnds:
        stop(hwnd)

    push_msg('已终止')


@eel.expose
def start(groupConfig, **kwds):
    global threads

    lock = threading.Lock()
    memory = Value('i', 0)

    for row in groupConfig:
        t = PauseableThread(target=daily_tasks,
                            args=(row['hwnd'], lock, row['config'], memory,
                                  eel.updateInfo))
        t.start()
        threads[row['hwnd']] = t

    # for key, value in threads.items():
    # value.join()
    # push_msg('已全部完成')


@eel.expose
def onekey(config):
    logger.info("开始一键")
    account_json = get_auto_login_json()
    account_json = json.loads(account_json)["accounts"]
    for group in account_json:
        hwnds = get_hwnd_list()
        overopen(hwnds)
        hwnds = get_hwnd_list()
        eel.updateWindows()

        login(group, hwnds)

        groupConfig = [{
            "hwnd": hwnd,
            "config": config[i]
        } for i, hwnd in enumerate(hwnds)]

        print(groupConfig)

        start(groupConfig)


@logger.catch
def init_gui(develop):
    init_auto_login_json()
    if develop:
        directory = 'web/src'
        app = 'chrome'
        page = {'port': 5173}
    else:
        directory = 'web/dist'
        app = 'chrome'
        page = 'index.html'
    eel_kwargs = dict(
        host='localhost',
        port=9000,
        size=(1200, 410),
    )
    print(app, eel_kwargs)
    eel.init(directory, ['.tsx', '.ts', '.jsx', '.js', '.html', '.css'])
    try:
        eel.start(page, mode=app, **eel_kwargs)
    except EnvironmentError as e:
        pass
        # If Chrome isn't found, fallback to Microsoft Edge on Win10 or greater
        # if sys.platform in ['win32', 'win64'] and int(platform.release()) >= 10:
        #     eel.start(page, mode='edge', **eel_kwargs)
        # else:
        #     raise


if __name__ == "__main__":
    import sys

    init_gui(develop=len(sys.argv) == 2)