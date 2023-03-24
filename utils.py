from win32 import win32process
import win32gui
import os
import requests
import threading
import sys
import time


def hide_login():
    hwnd = win32gui.FindWindow('MPAY_LOGIN', None)
    win32gui.ShowWindow(hwnd, 0)  # 0 隐藏  1 显示

    return True


def logout(hwnd):
    thread_id, process_id = win32process.GetWindowThreadProcessId(hwnd)
    os.system('taskkill /f /pid %s' % str(process_id))

    return True


def push_msg(msg):
    url = 'https://push.dongxin.co/v1/message/send'
    params = {
        "token": "54ae34e322deb80bb8d26e70",
        "title": "梦幻西游脚本完成提醒",
        "content": msg,
        "template": "text"
    }
    res = requests.post(url, json=params)
    print(res.json())

    return res.json()


class PauseableThread(threading.Thread):
    def __init__(self, target, args=()):
        super(PauseableThread, self).__init__()
        self.target = target
        self.args = args
        self.pause = False    # 用于暂停线程的标识
        self.stop = False    # 用于停止线程的标识

    def run(self):
        sys.settrace(self.trace_func)
        if self.args:
            self.target(*self.args)
        else:
            self.target()

    def trace_func(self, frame, event, arg):
        if self.pause:
            while self.pause:
                time.sleep(0.1)
        if self.stop:
            sys.exit()
        return self.trace_func

    def pause_thread(self):
        self.pause = True

    def resume_thread(self):
        self.pause = False

    def stop_thread(self):
        self.stop = True


if __name__ == "__main__":
    hide_login()