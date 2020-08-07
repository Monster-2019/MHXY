import win32gui, win32ui, win32con, win32api
from PIL import Image
import cv2 as cv
import os
from time import sleep
import time
import random

class ChangeAcct(object):
    """docstring for ChangeAcct"""
    def __init__(self):
        super(ChangeAcct, self).__init__()
        self.hwnd = win32gui.FindWindow('GAMEAPP', None)

    def LBtn(self, btnCoor):
        x = btnCoor[0][0] + random.randint(1, btnCoor[1][0])
        y = btnCoor[0][1] + random.randint(1, btnCoor[1][1])
        win32api.PostMessage(self.hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, win32api.MAKELONG(x, y))
        win32api.PostMessage(self.hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, win32api.MAKELONG(x, y))

    def enter(self):
        win32api.SendMessage(self.hwnd,win32con.WM_KEYDOWN, 13, 0);
        win32api.SendMessage(self.hwnd,win32con.WM_KEYUP, 13, 0);

    def gaizhuang(self):
        startT = time.time()
        endT = time.time()
        while endT < startT + 70:
            self.LBtn(((70, 583), (70, 20)))
            sleep(0.01)
            self.enter()
            sleep(0.01)
            self.enter()
            endT = time.time()
            print(endT - startT)

        print(startT, endT)

    def start(self, pythonCode):
        exec(pythonCode)

    def close(self):
        os.system('taskkill /F /IM mymain.exe')

if __name__ == '__main__':
    ChangeAcct().close()
    # ChangeAcct().start('print(123)')
