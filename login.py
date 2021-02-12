import win32gui, win32ui, win32con, win32api, win32com.client
from time import sleep
from PIL import Image
import cv2 as cv
import numpy as np
import random
import config
import os

from public.glo import Glo
from public.cutScreen import CScreen
from public.btn import Btn
from public.matchTem import Match
from public.log import log
from public.smc import SMC

class Login(object):
    asc = {
        'd': 68,
        '1': 97,
        '2': 98,
        '5': 101,
        '8': 104,
        '9': 105,
        '.': 110,
        'CR': 13,
    }
    """docstring for Login"""
    def __init__(self, groupNo):
        super(Login, self).__init__()
        self.g = Glo()
        self.shell = win32com.client.Dispatch("WScript.Shell")
        self.hwnd = 0
        self.groupNo = groupNo

    def SetForegroundWindowMy(self, hwnd):
        self.shell.SendKeys('%')
        win32gui.SetForegroundWindow(hwnd)

    def input(self, hwnd, smc):
        str = 'dd128915..'
        for char in str:
            anjian = self.asc[char]
            win32api.keybd_event(anjian,0,0,0)
            sleep(0.1)
            win32api.keybd_event(anjian,0,win32con.KEYEVENTF_KEYUP,0)

        # smc('mmdl', sleepT=0.3)

        win32api.keybd_event(self.asc['CR'],0,0,0)
        win32api.keybd_event(self.asc['CR'],0,win32con.KEYEVENTF_KEYUP,0)

    def filtter(self, hwnd, lparam):
        if win32gui.GetWindowTextLength(hwnd) == 12:
            style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
            if style and win32con.WS_EX_APPWINDOW:
                self.hwnd = hwnd

    def openGame(self, arr=[0,1,2,3,4]):
        os.system('start C:\\Users\\dongx\\Desktop\\SSKMH.exe')
        sleep(5)
        win32gui.EnumWindows(self.filtter, 0)
        # 遍历多开器的子窗口，设置多开器句柄
        hwndChildList = []
        win32gui.EnumChildWindows(self.hwnd, lambda hwnd, param: param.append(hwnd), hwndChildList)
        self.hwnd = hwndChildList[len(hwndChildList) - 1]
        self.SetForegroundWindowMy(self.hwnd)
        self.cutScreen = CScreen().cutScreen
        self.mymatchTem = Match().matchTem
        self.B = Btn()
        self.smc = SMC().smc
        for i in arr:
            n = 0
            self.B.LBtn(((638, 483), (178, 38)))
            while True:
                if n > 7:
                    self.B.LBtn(((638, 483), (178, 38)))
                    n = 0

                hwnd = win32gui.FindWindow('class neox::toolkit::Win32Window' + str(i), '《梦幻西游》手游')
                if hwnd != 0:
                    arr.remove(i)
                    sleep(0.5)
                    break
                n += 1

        sleep(1)
        os.system('taskkill /F /IM SSKMH.exe')

    def login(self, arr=[0,1,2,3,4]):
        openArr = []
        loginArr = []
        for item in arr:
            hwnd = win32gui.FindWindow('class neox::toolkit::Win32Window' + str(item), '《梦幻西游》手游')
            if hwnd != 0:
                self.SetForegroundWindowMy(hwnd)
                hwnd = win32gui.FindWindow('MPAY_LOGIN', None)
                if hwnd != 0:
                    loginArr.append(item)
            else:
                openArr.append(item)
                loginArr.append(item)

        # if len(openArr) > 0:
        #     self.openGame(openArr)

        for i in loginArr:
            # 登陆用户名和区
            status = False
            dlCoor = config.ACCTZU[self.groupNo]['acctList'][i]['coor']
            dlServer = config.ACCTZU[self.groupNo]['acctList'][i]['server']

            # 数据初始化
            self.g.set('windowClass', str(i))
            # 前置窗口用
            self.hwnd = win32gui.FindWindow('class neox::toolkit::Win32Window' + str(i), '《梦幻西游》手游')
            self.SetForegroundWindowMy(self.hwnd)
            self.cutScreen = CScreen().cutScreen
            self.mymatchTem = Match().matchTem
            self.B = Btn()
            self.smc = SMC().smc

            # 前置游戏窗口
            win32api.SendMessage(self.hwnd, win32con.WM_KEYDOWN, 27, 0)
            self.SetForegroundWindowMy(self.hwnd)
            sleep(0.5)

            # 游戏登陆窗口
            hwnd = win32gui.FindWindow('MPAY_LOGIN', None)
            cutScreen = CScreen(hwnd).cutScreen
            mymatchTem = Match().matchTem
            B = Btn(hwnd)
            smc = SMC(hwnd).smc
            # sleep(0.5)

            smc('select_zh')
            page = 1
            while True:
                res = smc(dlCoor, simi=0.97)
                if res == 0:
                    B.LBtn(((326, 329), (2, 2)))
                    sleep(0.1)
                else:
                    break

            sleep(0.5)
            smc('dl', sleepT=1)
            res = smc('android', sleepT=0.5)
            if res == 0:
                self.input(hwnd, smc)
                sleep(1)
                smc('android', sleepT=1.5)

            # 游戏登陆
            xhList = ['dl_qd', 'dl_djxf', 'dl_yyjs', dlServer]
            while not status:
                for item in xhList:
                    self.cutScreen()
                    btnCoor = self.mymatchTem(item)
                    if btnCoor != 0:
                        if item == dlServer:
                            self.B.LBtn(btnCoor, sleepT=2)

                            self.cutScreen()
                            btnCoor = self.mymatchTem('qr')
                            if btnCoor != 0:
                                self.B.LBtn(btnCoor)

                                while True:
                                    self.cutScreen()
                                    btnCoor = self.mymatchTem('dl_dlyx')
                                    if btnCoor != 0:
                                        self.B.LBtn(btnCoor)
                                        break

                            status = True
                            break
                        else:
                            self.B.LBtn(btnCoor)
                            sleep(0.5)

            log(f'账号{i}游戏登陆完成')

        sleep(5)

if __name__ == '__main__':
    Login(0).login()