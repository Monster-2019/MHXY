import os
import win32gui, win32con, win32api
from public.btn import Btn
from time import sleep
import psutil
from win32 import win32process

def start():
    try:
        os.system('start C:\\Users\\86155\\Desktop\\duokai\\mhxy.exe')
        sleep(2)

        while True:
            sleep(1)
            hwnd = win32gui.FindWindow(None, 'UnityWndClass')
            if hwnd:
                break

        # mnqBtn = Btn(hwnd)
        # for i in range(5):
        #     mnqBtn.LBtn(((350, 150), (2, 2)))
        #     sleep(1)

        # os.system('taskkill /F /IM mhxy.exe')

        win32gui.PostMessage(hwnd,win32con.WM_CLOSE,0,0)

        # thread_id, process_id = win32process.GetWindowThreadProcessId(hwnd)

        # os.system('taskkill /f /pid %s' % str(process_id))

    except Exception as e:
        print(e)

start()
