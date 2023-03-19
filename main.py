import os
import configparser
import win32gui
import win32process
import psutil
from time import sleep
from btn import Btn
from run import daily_tasks
from login import login
from multiprocessing import Pool

conf = configparser.ConfigParser()
conf.read('config.ini', encoding='utf-8')

timing_time = ''


def get_hwnd_list():
    # 查找所有标题为title的窗口句柄
    handles = []

    def callback(hwnd, handles):
        if win32gui.IsWindowVisible(hwnd) and not win32gui.IsIconic(
                hwnd) and '《梦幻西游》手游' in win32gui.GetWindowText(hwnd):
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
        btn.l(((350, 150), (2, 2)))
        sleep(3)

    os.system('taskkill /F /IM mhxy.exe')
    return

def auto_login(group=0, hwnds=None, **kwds):
    if not hwnds:
        hwnds = get_hwnd_list()
    login(group, hwnds)


def start(hwnds=None, **kwds):
    p = Pool(5)
    if not hwnds:
        hwnds = get_hwnd_list()
    for hwnd in hwnds:
        p.apply_async(daily_tasks, args=(hwnd, ))

    p.close()
    p.join()
    print('脚本完成')

methods = {"1": start, "2": overopen, "3": auto_login, "9": get_hwnd_list}


def call_method(param, **kwds):
    methods.get(param, lambda: print("Invalid parameter"))(**kwds)


def command_selection():
    while True:
        print("Please choose a method to call:")
        print("1. 开始日常")
        print("2. 多开")
        print("3. 自动登录")
        print("0. Exit")
        choice = input("Your choice: ")
        if choice in methods:
            call_method(choice)
            if choice == '1':
                break
        elif choice == "0":
            break
        else:
            print("Invalid choice:", choice)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--time', '-t', type=str)
    parser.add_argument('--action',
                        '-a',
                        choices=["1", "2", "3", "9"],
                        help="1. 开始日常、2. 多开、3. 自动登录")
    parser.add_argument('--group', '-g', type=int)

    args = parser.parse_args()
    timing_time = args.time
    if args.action:
        call_method(args.action, **args)
    else:
        command_selection()