from random import randint
from time import sleep

import win32api
import win32con

JWM = {
    'bp': ord('B'),
    'hd': ord('C'),
    'fl': ord('D'),
    'bb': ord('E'),
    'hy': ord('F'),
    'gj': ord('G'),
    'xt': ord('J'),
    'dt': ord('M'),
    'jy': ord('N'),
    'jn': ord('S'),
    'dw': ord('T'),
    'js': ord('W'),
    'rw': ord('Y'),
    'zz': ord('Z'),
    'tab': win32con.VK_TAB,
}

FIXED_COOR = {
    'zr1': (890, 161, 40, 40),
    'zr2': (890, 338, 40, 40),
    'zr3': (890, 515, 40, 40)
}

CENTER_COOR = (520, 403)


class Btn(object):

    def __init__(self, hwnd, lock=None):
        self.hwnd = hwnd
        self.lock = lock

    def l(self,
          coor,
          is_click=True,
          sleep_time=0,
          min_x=0,
          min_y=0,
          max_x=2000,
          max_y=1000,
          **kwds):
        if not coor or not is_click: return

        x, y, w, h = coor

        if x < min_x or y < min_y or x > max_x or y > max_y:
            return False

        click_x = x + randint(1, w)
        click_y = y + randint(1, h)

        win32api.PostMessage(self.hwnd, win32con.WM_LBUTTONDOWN,
                             win32con.MK_LBUTTON,
                             win32api.MAKELONG(click_x, click_y))
        sleep(0.01)
        win32api.PostMessage(self.hwnd, win32con.WM_LBUTTONUP,
                             win32con.MK_LBUTTON,
                             win32api.MAKELONG(click_x, click_y))

        sleep(sleep_time)

        return True

    def l_key(self, key, sleep_time=0):
        coor = FIXED_COOR[key]
        if not coor:
            return False
        x, y, w, h = coor

        click_x = x + randint(1, w)
        click_y = y + randint(1, h)

        win32api.PostMessage(self.hwnd, win32con.WM_LBUTTONDOWN,
                             win32con.MK_LBUTTON,
                             win32api.MAKELONG(click_x, click_y))
        sleep(0.01)
        win32api.PostMessage(self.hwnd, win32con.WM_LBUTTONUP,
                             win32con.MK_LBUTTON,
                             win32api.MAKELONG(click_x, click_y))

        sleep(sleep_time)

        return True

    def r(self):
        win32api.PostMessage(self.hwnd, win32con.WM_RBUTTONDOWN,
                             win32con.MK_RBUTTON,
                             win32api.MAKELONG(CENTER_COOR[0], CENTER_COOR[1]))
        sleep(0.01)
        win32api.PostMessage(self.hwnd, win32con.WM_RBUTTONUP,
                             win32con.MK_RBUTTON,
                             win32api.MAKELONG(CENTER_COOR[0], CENTER_COOR[1]))

    def v(self, zdelta, count=1):
        if zdelta > 0:
            for i in range(count):
                win32api.SendMessage(self.hwnd, win32con.WM_MOUSEWHEEL,
                                     win32api.MAKELONG(0, 120), 0)
                sleep(0.01)
        elif zdelta < 0:
            for i in range(count):
                win32api.SendMessage(self.hwnd, win32con.WM_MOUSEWHEEL,
                                     win32api.MAKELONG(0, -120), 0)
                sleep(0.01)

    def m(self, x, y):
        win32api.SendMessage(self.hwnd, win32con.WM_MOUSEMOVE, 0000,
                             win32api.MAKELONG(x, y))

    def d_horizontal(self, coor):
        start_x, start_y, end_x, end_y = coor
        for i in range(end_y - start_y):
            if i % 10 == 0:
                start_h = start_y + i
                self.m(start_x, start_h)
                win32api.PostMessage(self.hwnd, win32con.WM_LBUTTONDOWN,
                                     win32con.MK_LBUTTON,
                                     win32api.MAKELONG(start_x, start_h))
                win32api.PostMessage(self.hwnd, win32con.WM_MOUSEMOVE, 0000,
                                     win32api.MAKELONG(end_x, start_h))
                win32api.PostMessage(self.hwnd, win32con.WM_LBUTTONUP,
                                     win32con.MK_LBUTTON,
                                     win32api.MAKELONG(end_x, start_h))
                sleep(0.05)

    def d_vertical(self, coor):
        start_x, start_y, end_x, end_y = coor
        win32api.PostMessage(self.hwnd, win32con.WM_LBUTTONDOWN,
                             win32con.MK_LBUTTON,
                             win32api.MAKELONG(start_x, start_y))
        win32api.PostMessage(self.hwnd, win32con.WM_MOUSEMOVE, 0000,
                             win32api.MAKELONG(end_x, end_y))
        sleep(0.1)
        win32api.PostMessage(self.hwnd, win32con.WM_LBUTTONUP,
                             win32con.MK_LBUTTON,
                             win32api.MAKELONG(end_x, end_y))

    def hotkey(self, char, sleep_time=0.5):
        key = JWM[char]
        if not key: return

        # if self.lock:
            # self.lock.acquire()

        win32api.keybd_event(18, 0, 0, 0)
        win32api.SendMessage(self.hwnd, win32con.WM_KEYDOWN, key, 0)
        sleep(0.05)
        win32api.keybd_event(18, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.SendMessage(self.hwnd, win32con.WM_KEYUP, key, 0)
        win32api.keybd_event(18, 0, 0, 0)
        win32api.keybd_event(18, 0, win32con.KEYEVENTF_KEYUP, 0)

        # if self.lock:
            # self.lock.release()

        sleep(sleep_time)

    def press(self, char):
        key = JWM[char]
        win32api.SendMessage(self.hwnd, win32con.WM_KEYDOWN, key, 0)
        sleep(0.05)
        win32api.SendMessage(self.hwnd, win32con.WM_KEYUP, key, 0)


if __name__ == "__main__":
    import win32gui

    hwnd = win32gui.FindWindow(None, "梦幻西游：时空")
    btn = Btn(hwnd)
    for i in range(8):
        btn.d_vertical((660, 350, 660, 0))
        sleep(0.01)