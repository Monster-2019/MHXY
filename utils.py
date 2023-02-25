from win32 import win32process
import win32gui
import os
import requests


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


class GlobalVariable(object):
    _global_dict = {}

    def __init__(self):
        global _global_dict
        self._global_dict = {}

    def set_value(self, key, value):
        self._global_dict[key] = value

    def get_value(self, key):
        try:
            return self._global_dict[key]
        except:
            print(f"{key}不存在")

    def remove_value(self, key):
        try:
            return self._global_dict.pop(key)
        except:
            print(f"{key}不存在")

    def clear(self):
        for key in self._global_dict.keys():
            self._global_dict.pop(key)

class HsvFilter:
    def __init__(self, hMin=None, sMin=None, vMin=None, hMax=None, sMax=None, vMax=None, 
                    sAdd=None, sSub=None, vAdd=None, vSub=None):
        self.hMin = hMin
        self.sMin = sMin
        self.vMin = vMin
        self.hMax = hMax
        self.sMax = sMax
        self.vMax = vMax
        self.sAdd = sAdd
        self.sSub = sSub
        self.vAdd = vAdd
        self.vSub = vSub
