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
    def __init__(self, groupNo, hwndList):
        super(Login, self).__init__()
        self.g = Glo()
        self.shell = win32com.client.Dispatch("WScript.Shell")
        self.hwndList = hwndList
        self.groupNo = groupNo
        self.hwnd = 0

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

    def login(self, arr=[0,1,2,3,4]):
        openArr = []
        loginArr = []
        for item in arr:
            self.SetForegroundWindowMy(self.hwndList[item])
            hwnd = win32gui.FindWindow('MPAY_LOGIN', None)
            if hwnd != 0:
                loginArr.append(item)
                
        print(loginArr)

        for i in loginArr:
            # 登陆用户名和区
            status = False
            dlCoor = config.ACCTZU[self.groupNo]['acctList'][i]['coor']
            dlServer = config.ACCTZU[self.groupNo]['acctList'][i]['server']

            # 数据初始化
            self.g.set('windowClass', self.hwndList[i])
            self.g.set('screen', str(i))
            # 前置窗口用
            self.hwnd = self.hwndList[i]
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
                res = smc(dlCoor, simi=0.998)
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

        sleep(1)

if __name__ == '__main__':
    Login(0).login()