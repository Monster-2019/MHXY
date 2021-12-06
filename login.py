from io import SEEK_END
import win32gui, win32con, win32api, win32com.client
from time import sleep
import config
import os

from public.glo import Glo
from public.cutScreen import CScreen
from public.btn import Btn
from public.matchTem import Match
from public.log import log
from public.smc import SMC

class Login(object):
    """docstring for Login"""
    def __init__(self, groupNo, hwndList):
        super(Login, self).__init__()
        self.g = Glo()
        self.smc = SMC().smc
        self.shell = win32com.client.Dispatch("WScript.Shell")
        print('hwndList:', hwndList)
        self.hwndList = hwndList
        self.groupNo = groupNo
        self.hwnd = 0
        self.mnqHwnd = 0
        self.mnqCutScreen = None
        self.mnqMatchTem = None
        self.mnqBtn = None

    # 前置窗口
    def SetForegroundWindowMy(self, hwnd):
        self.shell.SendKeys('%')
        win32gui.SetForegroundWindow(hwnd)

    def mnqInit(self):
        os.system('start C:\\leidian\\LDPlayer4\\dnplayer.exe')
        sleep(10)

        while True:
            sleep(1)
            tem = win32gui.FindWindow(None, '雷电模拟器')
            self.mnqHwnd = win32gui.FindWindowEx(tem, None, 'RenderWindow', None)
            if self.mnqHwnd != 0:
                break
        
        self.mnqCutScreen = CScreen(self.mnqHwnd).cutScreen
        self.mnqMatchTem = Match('mnq').matchTem
        self.mnqBtn = Btn(self.mnqHwnd)

        self.SetForegroundWindowMy(self.mnqHwnd)

        while True:
            sleep(1)
            self.mnqCutScreen()
            res = self.mnqMatchTem('mnq_mhxy')
            if res != 0:
                self.mnqBtn.LBtn(res)
                break
        
        # # 等待8秒跳过动画
        sleep(10)
        self.mnqBtn.LBtn(((520, 119), (53, 60)))
        # 等待三秒模拟器登陆账号
        sleep(8)

        return

    def login(self, arr=[0,1,2,3,4]):
        try:
            loginArr = []
            for item in arr:
                self.SetForegroundWindowMy(self.hwndList[item])
                hwnd = win32gui.FindWindow('MPAY_LOGIN', None)
                print(hwnd)
                if hwnd != 0:
                    loginArr.append(item)
                    
            # 如果需要登录打开模拟器
            if len(loginArr) > 0:
                print(loginArr)
                self.mnqInit()   

            for i in loginArr:
                # 登陆用户名和区
                status = False
                dlAccount = config.ACCTZU[self.groupNo]['acctList'][i]['account']
                dlServer = config.ACCTZU[self.groupNo]['acctList'][i]['server']

                # 前置窗口用
                gameHwnd = self.hwndList[i]
                # self.SetForegroundWindowMy(gameHwnd)

                # 前置游戏窗口
                win32api.SendMessage(gameHwnd, win32con.WM_KEYDOWN, 27, 0)
                self.SetForegroundWindowMy(gameHwnd)
                sleep(0.5)

                # 截图游戏登陆窗口到共享文件夹进行扫描登陆
                hwnd = win32gui.FindWindow('MPAY_LOGIN', None)
                cutScreen = CScreen(hwnd, 'C:/Users/86155/Documents/leidian/Pictures/').cutScreen
                cutScreen()

                self.SetForegroundWindowMy(self.mnqHwnd)

                # 'mnq_sm' 'mnq_tk' ((640, 370), (2, 2)) ((640, 370), (2, 2)) sleep(2) 'mnq_dl'

                mnqLoginList = ['mnq_sm', 'mnq_tk', dlAccount, 'mnq_dl']
                for item in mnqLoginList:
                    status = False
                    while not status:
                        self.mnqCutScreen()
                        coor = self.mnqMatchTem(item)
                        if coor != 0:
                            if item == 'mnq_tk':
                                self.mnqBtn.LBtn(coor, sleepT=1)

                                while True:
                                    self.mnqCutScreen()
                                    coor = self.mnqMatchTem('mnq_dl')
                                    if coor != 0:
                                        break
                                    else:
                                        self.mnqBtn.LBtn(((640, 370), (2, 2)))
                                    sleep(0.5)
                                
                                sleep(1)
                                self.mnqBtn.LBtn(((630, 300), (2, 2)))
                                sleep(1)
                            else:
                                self.mnqBtn.LBtn(coor)

                            status = True
                        else:
                            if item == dlAccount:
                                for index in range(3):
                                    self.mnqCutScreen()
                                    coor = self.mnqMatchTem(item)
                                    if coor != 0:
                                        break
                                    self.mnqBtn.DBtn((630, 450), (630, 350))
                                    sleep(0.5)
                        sleep(1)

                print('模拟器登录完成')
                # continue

                # 游戏登陆
                self.g.set('windowClass', self.hwndList[i])
                self.g.set('screen', str(i))
                self.smc = SMC().smc
                sleep(1)
                xhList = ['dl_qd', 'dl_djxf', 'dl_yyjs', dlServer]
                status = False
                while not status:
                    for item in xhList:
                        res = self.smc(item, sleepT=0.5)
                        if res != 0 and item == dlServer:
                            status = True
                            break

                log(f'账号 {dlAccount} 游戏登陆完成')

            os.system('taskkill /F /IM dnplayer.exe')

            sleep(1)

        except Exception as e:
            print('err', e)

if __name__ == '__main__':
    hwndList = []
    isStart = False
    hwnd = 0
    while not isStart:
        if not isStart and hwnd == 0:
            hwnd = win32gui.FindWindow(None, "《梦幻西游》手游")
        else:
            hwnd = win32gui.FindWindowEx(None, hwnd, None, "《梦幻西游》手游")
        if hwnd:
            hwndList.append(hwnd)
        else:
            isStart = True

    Login(0, hwndList).login()