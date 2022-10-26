import sys

sys.path.append('.')
sys.path.append('..')
from time import sleep
import win32api, win32con
import random
from glo import Glo


class Btn:
    jwm = {
        'hd': 67,
        'fl': 68,
        'hy': 70,
        'gj': 71,
        'rw': 89,
        'dw': 84,
        'bb': 69,
        'xt': 74,
        'dt': 77,
        'jy': 78,
        'js': 87,
        'jn': 83,
        'zz': 90
    }

    fixedCoor = {
        'zr1': ((890, 161), (40, 40)),
        'zr2': ((890, 338), (40, 40)),
        'zr3': ((890, 515), (40, 40))
    }

    def __init__(self, hwnd=False):
        self.g = Glo()
        if hwnd:
            self.hwnd = hwnd
        else:
            self.hwnd = self.g.get('windowClass')
        self.lock = self.g.get('lock')

    def LBtn(self, btnCoor, sleepT=0.1, count=1, minx=0, miny=0, maxx=2000, maxy=1000):
        if not btnCoor:
            return False

        if isinstance(btnCoor, str):
            btnCoor = self.fixedCoor.get(btnCoor)
        elif btnCoor[0][0] < minx or btnCoor[0][1] < miny or btnCoor[0][0] > maxx or btnCoor[0][1] > maxy:
            return False
        
        x = btnCoor[0][0] + random.randint(1, btnCoor[1][0])
        y = btnCoor[0][1] + random.randint(1, btnCoor[1][1])
        for i in range(count):
            win32api.PostMessage(self.hwnd, win32con.WM_LBUTTONDOWN,
                                 win32con.MK_LBUTTON, win32api.MAKELONG(x, y))
            sleep(0.1)
            win32api.PostMessage(self.hwnd, win32con.WM_LBUTTONUP,
                                 win32con.MK_LBUTTON, win32api.MAKELONG(x, y))
        sleep(sleepT)

        return True

    def RBtn(self):
        win32api.PostMessage(self.hwnd, win32con.WM_RBUTTONDOWN,
                             win32con.MK_RBUTTON, win32api.MAKELONG(520, 403))
        sleep(0.01)
        win32api.PostMessage(self.hwnd, win32con.WM_RBUTTONUP,
                             win32con.MK_RBUTTON, win32api.MAKELONG(520, 403))
        sleep(0.2)

    def VBtn(self, zdelta, count=1):
        if zdelta > 0:
            for i in range(count):
                win32api.SendMessage(self.hwnd, win32con.WM_MOUSEWHEEL,
                                     win32api.MAKELONG(0, 120), 0)
                sleep(0.05)
        elif zdelta < 0:
            for i in range(count):
                win32api.SendMessage(self.hwnd, win32con.WM_MOUSEWHEEL,
                                     win32api.MAKELONG(0, -120), 0)
                sleep(0.05)

    def MBtn(self, x, y):
        win32api.SendMessage(self.hwnd, win32con.WM_MOUSEMOVE, 0000,
                             win32api.MAKELONG(x, y))

    def DBtn(self, s, e):
        if s[0] == e[0]:
            self.MBtn(s[0], s[1])
            win32api.PostMessage(self.hwnd, win32con.WM_LBUTTONDOWN,
                                 win32con.MK_LBUTTON,
                                 win32api.MAKELONG(s[0], s[1]))
            win32api.PostMessage(self.hwnd, win32con.WM_MOUSEMOVE, 0000,
                                 win32api.MAKELONG(e[0], e[1]))
            sleep(0.1)
            win32api.PostMessage(self.hwnd, win32con.WM_LBUTTONUP,
                                 win32con.MK_LBUTTON,
                                 win32api.MAKELONG(e[0], e[1]))
            sleep(0.5)

        elif s[1] == e[1]:
            self.MBtn(s[0], s[1])
            win32api.PostMessage(self.hwnd, win32con.WM_LBUTTONDOWN,
                                 win32con.MK_LBUTTON,
                                 win32api.MAKELONG(s[0], s[1]))
            win32api.PostMessage(self.hwnd, win32con.WM_MOUSEMOVE, 0000,
                                 win32api.MAKELONG(e[0], e[1]))
            sleep(0.1)
            win32api.PostMessage(self.hwnd, win32con.WM_LBUTTONUP,
                                 win32con.MK_LBUTTON,
                                 win32api.MAKELONG(e[0], e[1]))
            sleep(0.5)

        else:
            for i in range(e[1] - s[1]):
                if i % 10 == 0:
                    startH = s[1] + i
                    self.MBtn(s[0], startH)
                    win32api.PostMessage(self.hwnd, win32con.WM_LBUTTONDOWN,
                                         win32con.MK_LBUTTON,
                                         win32api.MAKELONG(s[0], startH))
                    win32api.PostMessage(self.hwnd, win32con.WM_MOUSEMOVE,
                                         0000, win32api.MAKELONG(e[0], startH))
                    win32api.PostMessage(self.hwnd, win32con.WM_LBUTTONUP,
                                         win32con.MK_LBUTTON,
                                         win32api.MAKELONG(e[0], startH))
                    sleep(0.05)

    def Hotkey(self, char, sleepT=0.5):
        anjian = self.jwm[char]
        if self.lock != None:
            self.lock.acquire()
        win32api.keybd_event(18, 0, 0, 0)
        win32api.SendMessage(self.hwnd, win32con.WM_KEYDOWN, anjian, 0)
        sleep(0.05)
        win32api.keybd_event(18, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.SendMessage(self.hwnd, win32con.WM_KEYUP, anjian, 0)
        win32api.keybd_event(18, 0, 0, 0)
        win32api.keybd_event(18, 0, win32con.KEYEVENTF_KEYUP, 0)
        if self.lock != None:
            self.lock.release()
        sleep(sleepT)


if __name__ == "__main__":
    t = Btn()