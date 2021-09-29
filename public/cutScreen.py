import sys
sys.path.append('.')
sys.path.append('..')
import win32gui, win32ui, win32con
from PIL import Image
from time import sleep
from public.glo import Glo
import cv2 as cv
from PIL import Image
import numpy as np

class CScreen(object):
    login = False
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

    def __init__(self, hwnd=False):
        # 初始化窗口的句柄
        super(CScreen, self).__init__()
        self.g = Glo()
        self.index = self.g.get('screen')
        if hwnd:
            self.hwnd = hwnd
            self.login = True
        else:
            # self.hwnd = win32gui.FindWindow('class neox::toolkit::Win32Window' + self.index, None)
            self.hwnd = self.g.get('windowClass')

    def cutScreen(self, infoKey=""):
        # 获取句柄窗口的大小信息
        # 可以通过修改该位置实现自定义大小截图
        left, top, right, bot = win32gui.GetWindowRect(self.hwnd)
        if (infoKey != "" and isinstance(infoKey, str)):
            self.Coor = self.infoCoor[infoKey][0]
            self.WH = self.infoCoor[infoKey][1]
        elif (infoKey != "" and isinstance(infoKey, tuple)):
            self.Coor = infoKey[0]
            self.WH = infoKey[1]
        else:
            self.Coor = (0, 0)
            self.WH = (right - left - 17, bot - top - 39)

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

        # 将截图保存到文件中
        try:
            ###获取位图信息
            bmpinfo = saveBitMap.GetInfo()
            bmpstr = saveBitMap.GetBitmapBits(True)
            ###生成图像
            im_PIL = Image.frombuffer('RGB',(bmpinfo['bmWidth'],bmpinfo['bmHeight']),bmpstr,'raw','BGRX',0,1)
            ###PrintWindow成功,保存到文件,显示到屏幕
            im_PIL.save("./images/screen" + self.index + '.jpg') #保存

        except Exception as e:
            print(f'报错{e}')

        # 释放内存
        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, hwndDC)
        sleep(0.01)

        if infoKey == "" and not self.login:
            img = cv.imread('./images/screen' + self.index  + '.jpg')
            self.g.set('oldCoor', self.g.get('newCoor'))
            # self.g.set('newCoor', [img[200, 200], img[560, 815]])
            self.g.set('newCoor', [np.array(img[200, 200]).sum(), np.array(img[560, 815]).sum()])
            # print([np.array(img[200, 200]).sum(), np.array(img[560, 815]).sum()])
            

if __name__ == '__main__':
    CScreen().cutScreen()
