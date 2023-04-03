import os
import configparser
import win32gui
import win32process
import psutil
import sys
import threading
from time import sleep
from btn import Btn
from run import daily_tasks
from login import login
from multiprocessing import Pool
import tkinter as tk
from tkinter import filedialog
from utils import PauseableThread, push_msg

f = open(os.devnull, 'w')
sys.stdout = f
sys.stderr = f

import eel

conf = configparser.ConfigParser()
path = os.path.join(os.getcwd(), "config.ini")
conf.read(path, encoding='utf-8')

timing_time = ''


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

    print(handles)
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


def overopen(hwnd_list=[]):
    if len(hwnd_list) == 5:
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

    os.system('taskkill /F /IM mhxy.exe')
    return


def auto_login(group=0, hwnds=None, **kwds):
    if not hwnds:
        hwnds = get_hwnd_list()
    login(group, hwnds)


threads = dict()


def stop(hwnd):
    global threads
    threads[hwnd].stop_thread()


@eel.expose
def stopAll(hwnds):
    if not hwnds:
        return
    global threads
    for hwnd in hwnds:
        stop(hwnd)


@eel.expose
def start(hwnds=None, **kwds):
    global threads
    lock = threading.Lock()

    for hwnd in hwnds:
        t = PauseableThread(target=daily_tasks,
                            args=(hwnd, lock, eel.updateInfo, eel.updateState))
        t.start()
        threads[hwnd] = t

    for thread in threads:
        thread.join()

    push_msg('已全部完成')


@eel.expose
def onekey():
    hwnds = get_hwnd_list()
    overopen(hwnds)
    hwnds = get_hwnd_list()
    auto_login(0, hwnds)
    start(hwnds)


def init_gui(develop):
    print(develop)
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