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

class ChangeAcct(object):
    """docstring for ChangeAcct"""
    def __init__(self):
        super(ChangeAcct, self).__init__()
        self.g = Glo()
        self.shell = win32com.client.Dispatch("WScript.Shell")
        self.hwnd = 0

    def LBtn(self, btnCoor):
        x = btnCoor[0][0] + random.randint(1, btnCoor[1][0] )
        y = btnCoor[0][1] + random.randint(1, btnCoor[1][1] )
        win32api.PostMessage(self.hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, win32api.MAKELONG(x, y))
        sleep(0.01)
        win32api.PostMessage(self.hwnd, win32con.WM_LBUTTONUP, win32con.MK_LBUTTON, win32api.MAKELONG(x, y))

    def matchTem(self, tem, simi=0.9):
        screen = cv.imread('./images/mnq.jpg', 0)
        newTem = cv.imread('./images/imgTem/' + tem  + '.jpg', 0)

        kernel = np.ones((1, 1), np.uint8)
        screen = cv.morphologyEx(screen, cv.MORPH_OPEN, kernel)
        newTem = cv.morphologyEx(newTem, cv.MORPH_OPEN, kernel)
        # cv.imshow("custom_blur_demo1", screen)
        # cv.imshow("custom_blur_demo", newTem)
        # cv.waitKey(0)
        # cv.destroyAllWindows()

        w, h = newTem.shape[::-1]

        result = cv.matchTemplate(screen, newTem, cv.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

        # log(max_val)
        if max_val > simi:
            return (max_loc, (w, h))
        else:
            return 0

    def cut(self):
        left, top, right, bot = win32gui.GetWindowRect(self.hwnd)
        WH = (right - left, bot - top)
        # 返回句柄窗口的设备环境、覆盖整个窗口，包括非客户区，标题栏，菜单，边框
        # 返回句柄窗口的设备环境、覆盖整个窗口，包括非客户区，标题栏，菜单，边框
        hwndDC = win32gui.GetDC(self.hwnd)

        # 创建设备描述表
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)

        # 创建内存设备描述表
        saveDC = mfcDC.CreateCompatibleDC()

        # 创建位图对象
        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, WH[0], WH[1])
        saveDC.SelectObject(saveBitMap)

        # 截图至内存设备描述表
        saveDC.BitBlt((0, 0), (WH[0], WH[1]), mfcDC, (0, 0), win32con.SRCCOPY)

        # 将截图保存到文件中
        saveBitMap.SaveBitmapFile(saveDC, './images/mnq.jpg')

        # 释放内存
        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, hwndDC)
        sleep(0.01)

    def SetForegroundWindowMy(self, hwnd):
        self.shell.SendKeys('%')
        win32gui.SetForegroundWindow(hwnd)

    def setWindow(self, windowName):
        if windowName == 'mnq':
            tem = win32gui.FindWindow(None, '雷电模拟器')
            self.hwnd = win32gui.FindWindowEx(tem, None, 'RenderWindow', None)
            # self.hwnd = win32gui.FindWindow('LDPlayerMainFrame', None)
            # hwndChildList = []
            # win32gui.EnumChildWindows(self.hwnd, lambda hwnd, param: param.append(hwnd), hwndChildList)
            # self.hwnd = hwndChildList[0]

        elif windowName == 'mnqSM':
            self.hwnd = win32gui.FindWindow('TrayNoticeWindow', None)

        elif windowName == 'gameLogin':
            self.hwnd = win32gui.FindWindow('MPAY_LOGIN', None)

        elif windowName == 'duokai':
            # 遍历所有窗口找出多开器窗口
            win32gui.EnumWindows(self.filtter, 0)
            # 遍历多开器的子窗口，设置多开器句柄
            hwndChildList = []
            win32gui.EnumChildWindows(self.hwnd, lambda hwnd, param: param.append(hwnd), hwndChildList)
            self.hwnd = hwndChildList[len(hwndChildList) - 1]

    def startGame(self, arr):
        if len(arr) > 0:
            os.system('start C:\\Users\\dongx\\Desktop\\SSKMH.exe')
            sleep(5)
            while True:
                try:
                    sleep(1)
                    self.setWindow('duokai')
                    self.cut()
                    break
                except Exception as e:
                    log(e)
            while len(arr) > 0:
                for i in arr:
                    self.LBtn(((638, 483), (178, 38)))
                    sleep(0.5)

                sleep(2)
                for i in arr:
                    hwnd = win32gui.FindWindow('class neox::toolkit::Win32Window' + str(i), '《梦幻西游》手游')
                    if hwnd != 0:
                        arr.remove(i)
                    sleep(0.5)

            sleep(1)
            os.system('taskkill /F /IM SSKMH.exe')

    def login(self, arr):
        if len(arr) > 0:
            os.system('start D:\\software\\dnplayer2\\dnplayer.exe')
            sleep(10)

            try:
                self.setWindow('mnq')
            except Exception as e:
                log(e)
                sleep(10)
                self.setWindow('mnq')
            
            sleep(0.5)

            while True:
                self.cut()
                btn = self.matchTem('mnq_ds')
                if btn != 0:
                    self.LBtn(btn)
                    break

            for i in arr:
                # 登陆用户名和区
                status = False
                dlCoor = config.ACCTZU[0]['acctList'][i]['coor']
                dlServer = config.ACCTZU[0]['acctList'][i]['server']

                # 数据初始化
                self.g.set('windowClass', str(i))
                hwnd = win32gui.FindWindow('class neox::toolkit::Win32Window' + str(i), '《梦幻西游》手游')
                self.SetForegroundWindowMy(hwnd)
                self.cutScreen = CScreen().cutScreen
                self.mymatchTem = Match().matchTem
                self.B = Btn()

                smCom = False
                self.setWindow('mnq')
                sleep(0.5)
                while not smCom:
                    for item in ['mnq_sm', 'mnq_sm1', 'mnq_sys']:
                        self.cut()
                        btn = self.matchTem(item, simi=0.8)
                        if btn != 0:
                            if item == 'mnq_sys':
                                self.setWindow('mnqSM')
                                sleep(0.5)
                                self.cut()
                                btn = self.matchTem('mnq_ssjt')
                                if btn != 0:
                                    self.LBtn(btn)
                                    sleep(0.5)
                                    smCom = True
                                    break
                            else:
                                self.LBtn(btn)
                            sleep(0.5)

                # 前置游戏窗口
                win32api.SendMessage(self.hwnd,win32con.WM_KEYDOWN, 27, 0)
                self.SetForegroundWindowMy(hwnd)
                # sleep(0.5)

                # 游戏登陆窗口
                self.setWindow('gameLogin')

                self.cut()
                btn = self.matchTem('dl_smwc')
                if btn == 0:
                    while True:
                        btn = self.matchTem('dl_sx')
                        if btn != 0:
                            self.LBtn(btn)
                            sleep(1)

                        self.cut()
                        tem = self.matchTem('dl_smwc')
                        if tem != 0:
                            sleep(0.5)
                            break

                self.setWindow('mnq')
                sleep(0.5)

                # 模拟器登陆账号
                xhList = ['mnq_dl', 'mnq_xzzh']
                dlStatus = False
                while not dlStatus:
                    for item in xhList:
                        self.cut()
                        btn = self.matchTem(item, simi=0.8)
                        if btn != 0:
                            if item == 'mnq_dl':
                                self.LBtn(((228, 518), (116, 23)))

                            elif item == 'mnq_xzzh':
                                self.LBtn(dlCoor)
                                dlStatus = True
                                break
                                
                            sleep(0.5)

                while True:
                    self.cut()
                    btn = self.matchTem('mnq_sm', simi=0.8) or self.matchTem('mnq_sm1', simi=0.8)
                    if btn != 0:
                        break
                    else:
                        btn = self.matchTem('mnq_fh', simi=0.8)
                        if btn != 0:
                            self.LBtn(btn)

                # 前置游戏窗口
                # sleep(1)
                self.SetForegroundWindowMy(hwnd)
                log('模拟器登陆完成')
                sleep(2)

                # 游戏登陆
                xhList = ['dl_djxf', 'dl_yyjs', dlServer]
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

                log('游戏登陆完成')

            sleep(10)
            os.system('taskkill /F /IM dnplayer.exe')

    def filtter(self, hwnd, lparam):
        if win32gui.GetWindowTextLength(hwnd) == 12:
            style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
            if style and win32con.WS_EX_APPWINDOW:
                self.hwnd = hwnd

    def start(self):
        try:
            arr = config.ACCTZU[0]['acctList']
            windowArr = []
            loginArr = []
            for index, item in enumerate(arr):
                hwnd = win32gui.FindWindow('class neox::toolkit::Win32Window' + str(index), '《梦幻西游》手游')
                if hwnd == 0:
                    windowArr.append(index)
                    loginArr.append(index)
                else:
                    self.SetForegroundWindowMy(hwnd)
                    self.setWindow('gameLogin')
                    try:
                        self.cut()
                        tem = self.matchTem('dl_smwc') or self.matchTem('dl_sm') or self.matchTem('dl_sx')
                        if tem != 0:
                            loginArr.append(index)
                    except Exception as e:
                        continue

            self.startGame(windowArr)

            self.login(loginArr)

            return 1
        except Exception as e:
            log(e)

if __name__ == '__main__':
    # ChangeAcct().start()
    a = ChangeAcct()
    a.setWindow('mnq')
    a.cut()
    log(a.matchTem('h1'))
    # a.LBtn(((155, 310), (20, 20)))
    # 30,110   500 30
