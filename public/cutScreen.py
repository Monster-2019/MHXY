import sys
sys.path.append('.')
sys.path.append('..')
import win32gui, win32ui, win32con
from time import sleep
from public.glo import Glo
import cv2 as cv

class CScreen(object):
    login = False
    screen = ''
    Coor = ()
    WH = ()
    infoCoor = {
        "btgm": ((412, 258), (135, 25)),
        "name": ((197, 136), (190, 35)),
        "gold": ((106, 634), (130, 24)),
        "silver": ((300, 634), (160, 24)),
        "bb": ((513, 202), (407, 407)),
        "gfbt": ((647, 207), (306, 461))
    }

    def __init__(self, hwnd=False, saveUrl='./images/'):
        # 初始化窗口的句柄
        super(CScreen, self).__init__()
        self.g = Glo()
        self.index = self.g.get('screen')
        self.saveUrl = saveUrl
        if hwnd:
            self.hwnd = hwnd
            self.login = True
            self.screen = 'mnq'
        else:
            self.hwnd = self.g.get('windowClass')
            self.screen = 'screen' + self.index

    def cutScreen(self):
        left, top, right, bot = win32gui.GetWindowRect(self.hwnd)
        self.Coor = (0, 0)
        self.WH = (right - left - 17, bot - top - 39)

        self.saveImg()

        if not self.login:
            img = cv.imread('./images/' + self.screen + '.jpg')
            self.g.set('oldCoor', self.g.get('newCoor'))
            self.g.set('newCoor', [img[200, 200], img[560, 200], img[200, 815], img[560, 815]])

    def customCutScreen(self, infoKey=""):
        if not infoKey:
            return 0

        self.Coor = self.infoCoor[infoKey][0]
        self.WH = self.infoCoor[infoKey][1]

        self.saveImg()

        sleep(0.01)

    def saveImg (self):
        # 返回句柄窗口的设备环境、覆盖整个窗口，包括非客户区，标题栏，菜单，边框
        hwndDC = win32gui.GetDC(self.hwnd)

        # 创建设备描述表
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)

        # 创建内存设备描述表
        # 创建位图对象
        # 截图至内存设备描述表
        saveDC = mfcDC.CreateCompatibleDC()
        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, self.WH[0], self.WH[1])
        saveDC.SelectObject(saveBitMap)
        saveDC.BitBlt((0, 0), (self.WH[0], self.WH[1]), mfcDC, (self.Coor[0], self.Coor[1]), win32con.SRCCOPY)
        saveBitMap.SaveBitmapFile(saveDC, self.saveUrl + self.screen + '.jpg')
        # print(self.saveUrl + self.screen + '.jpg')

        # 释放内存
        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, hwndDC)

if __name__ == '__main__':
    hwnd = win32gui.FindWindow('MPAY_LOGIN', None)
    # hwnd = win32gui.FindWindow(None, "《梦幻西游》手游")
    win32gui.SetForegroundWindow(hwnd)
    print(hwnd)
    CScreen(hwnd, './images/mnq/').cutScreen()
    # CScreen(hwnd, 'C:/Users/1/Documents/leidian/Pictures').cutScreen()
    # C:\Users\1\Desktop\MHXY

