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


if __name__ == "__main__":
    hide_login()