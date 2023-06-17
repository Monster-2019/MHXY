import win32gui
import threading
import sys
from time import sleep
from win32 import win32process


def hide_login():
    hwnd = win32gui.FindWindow('MPAY_LOGIN', None)
    win32gui.ShowWindow(hwnd, 0)  # 0 隐藏  1 显示

    return True


def logout(hwnd):
    import os
    thread_id, process_id = win32process.GetWindowThreadProcessId(hwnd)
    os.system('taskkill /f /pid %s' % str(process_id))

    return True


def push_msg(msg):
    import requests
    url = 'https://push.dongxin.co/v1/message/send'
    params = {
        "token": "aa625b3a82edd843e819bb72",
        "title": "梦幻西游脚本完成提醒",
        "content": msg,
        "template": "text"
    }
    res = requests.post(url, json=params)

    return res.json()


def get_hwnds():
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
    import psutil
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    process = psutil.Process(pid)
    create_time = process.create_time()
    return create_time


def get_json_file(filename):
    import json
    with open(f'config/{filename}.json', 'r') as f:
        json_data = f.read()
        data = json.loads(json_data)
        formatted_data = json.dumps(data, indent=2)
    return formatted_data


def openmore(hwnd_list=[]):
    import configparser
    import os
    
    from time import sleep
    from btn import Btn

    if len(hwnd_list) == 5:
        logger.info('已打开客户端，退出软件')
        return

    conf = configparser.ConfigParser()
    path = os.path.join(os.getcwd(), "config.ini")
    conf.read(path, encoding='utf-8')

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


def init_log_dir():
    import os
    with open("app.log", mode="w", encoding="utf-8"):
        pass

    import glob
    jpg_files = glob.glob('images/*.jpg')

    for jpg_file in jpg_files:
        os.remove(jpg_file)


class PauseableThread(threading.Thread):
    def __init__(self, target, args=(), stop_func=None):
        super(PauseableThread, self).__init__()
        self.target = target
        self.args = args
        self.pause = False
        self.stop = False
        self.stop_func = stop_func

    def run(self):
        sys.settrace(self.trace_func)
        if self.args:
            self.target(*self.args)
        else:
            self.target()

    def trace_func(self, frame, event, arg):
        if self.pause:
            while self.pause:
                sleep(0.1)
        if self.stop:
            if self.stop_func:
                self.stop_func()
            sys.exit()
        return self.trace_func

    def pause_thread(self):
        self.pause = True

    def resume_thread(self):
        self.pause = False

    def stop_thread(self):
        self.stop = True

def culture(self):
    while True:
        coor = self.smc('culture_t', simi=0.998) or self.smc('culture_d',
                                                                simi=0.998)
        if coor:
            sleep(0.2)
            self.smc('culture_active')
            sleep(0.3)
        else:
            break
    print('培养激活完成')


if __name__ == "__main__":
    push_msg('已全部完成')