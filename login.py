import win32gui, win32con, win32api, win32com.client
from time import sleep
from config import user
import os
import traceback

from glo import Glo
from cutScreen import CScreen
from btn import Btn
from matchTem import Match
from log import log
from smc import SMC

class Login(object):
    """docstring for Login"""
    def __init__(self, groupNo, hwndList):
        super(Login, self).__init__()
        self.g = Glo()
        self.smc = None
        self.shell = win32com.client.Dispatch("WScript.Shell")
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
        sleep(12)
        self.mnqBtn.LBtn(((500, 250), (20, 20)))

        while True:
            self.mnqCutScreen()
            res = self.mnqMatchTem('mnq_sm')
            if res:
                sleep(5)
                break
            sleep(1)

        # 等待三秒模拟器登陆账号
        print('模拟器初始化完成')

        return

    def login(self):
        try:
            loginArr = []
            for item in range(len(self.hwndList)):
                self.SetForegroundWindowMy(self.hwndList[item])
                hwnd = win32gui.FindWindow('MPAY_LOGIN', None)
                res = win32gui.IsWindowVisible(hwnd)
                if hwnd != 0 and res != 0:
                    loginArr.append(item)
                    
            # 如果需要登录打开模拟器
            if len(loginArr) > 0:
                self.mnqInit()

            for i in loginArr:
                # 登陆用户名和区
                status = False
                dlAccount = user.ACCTZU[self.groupNo]['acctList'][i]['account']
                dlServer = user.ACCTZU[self.groupNo]['acctList'][i]['server']

                # 前置窗口用
                gameHwnd = self.hwndList[i]
                # self.SetForegroundWindowMy(gameHwnd)

                # 前置游戏窗口
                win32api.SendMessage(gameHwnd, win32con.WM_KEYDOWN, 27, 0)
                self.SetForegroundWindowMy(gameHwnd)
                sleep(0.5)
                gameBtn = Btn(gameHwnd)
                gameBtn.LBtn(((485, 483), (57, 15)))
                sleep(0.5)

                # 截图游戏登陆窗口到共享文件夹进行扫描登陆
                hwnd = win32gui.FindWindow('MPAY_LOGIN', None)
                cutScreen = CScreen(hwnd, './images/mnq/').cutScreen
                cutScreen()

                self.SetForegroundWindowMy(self.mnqHwnd)

                # 'mnq_sm' 'mnq_tk' ((640, 370), (2, 2)) ((640, 370), (2, 2)) sleep(2) 'mnq_dl'

                mnqLoginList = ['mnq_sm', 'mnq_tk', dlAccount, 'mnq_dl']
                status = False
                while not status:
                    for item in mnqLoginList:
                        self.mnqCutScreen()
                        coor = self.mnqMatchTem(item)
                        if coor:
                            if item == 'mnq_tk':
                                self.mnqBtn.LBtn(coor, sleepT=1)

                                while True:
                                    self.mnqCutScreen()
                                    coor = self.mnqMatchTem('mnq_dl')
                                    if coor != 0:
                                        break
                                    else:
                                        self.mnqBtn.LBtn(((100, 160), (2, 2)))
                                        # self.mnqBtn.LBtn(((650, 480), (2, 2)))
                                    sleep(0.5)
                                
                                sleep(0.5)
                                self.mnqBtn.LBtn(((460, 190), (2, 2)))
                                sleep(0.5)

                            else:
                                self.mnqBtn.LBtn(coor)
                                if item == 'mnq_dl':
                                    status = True
                                    break

                        else:
                            if item == dlAccount:
                                for index in range(3):
                                    self.mnqCutScreen()
                                    coor = self.mnqMatchTem(item)
                                    if coor != 0:
                                        break
                                    self.mnqBtn.DBtn((460, 340), (460, 240))
                                    sleep(0.5)
                        sleep(1)

                print('模拟器登录完成')
                # continue

                # 游戏登陆
                # self.g.set('windowClass', self.hwndList[i])
                # self.g.set('screen', str(i))
                sleep(0.5)
                # self.smc = SMC().smc

                cutScreen = CScreen(self.hwndList[i]).cutScreen
                matchTem = Match('mnq').matchTem
                gameBtn = Btn(self.hwndList[i])

                sleep(0.5)

                xhList = ['dl_qd', 'dl_js', 'dl_djxf', 'dl_yyjs', dlServer]
                status = False
                while not status:
                    for item in xhList:
                        # res = self.smc(item, sleepT=0.5)
                        cutScreen()
                        res = matchTem(item)
                        if res:
                            gameBtn.LBtn(res)
                            if item == dlServer:
                                status = True
                                break
                        # if res != 0 and item == dlServer:
                        #     status = True
                        #     break

                log(f'账号 {dlAccount} 游戏登陆完成')

            if len(loginArr) > 0:
                os.system('taskkill /F /IM dnplayer.exe')

            sleep(1)

        except Exception as e:
            print('err12313', e)
            traceback.print_exc()

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