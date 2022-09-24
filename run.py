import sys

sys.path.append('.')
sys.path.append('..')
from apscheduler.schedulers.blocking import BlockingScheduler
from multiprocessing import Pool, Manager
from datetime import datetime
from time import sleep
import os
import traceback
import win32gui
import argparse

from public.log import log
from guajiang import Guajiang
from public.getInfo import Info
from zhuogui import Zhuogui
from lls_pt import LLSPT
from fuben import FuBen
from public.lidui import Lidui
from shimen import Shimen
from baotu import Baotu
from mijing import Mijing
from yunbiao import Yunbiao
from sjqy import SJQY
from kjxs import KJXS
from lqhyd import LQHYD
# from gengzhong import GengZhong
from clean import Clean
from logout import Logout
from login import Login
from sendMsg import SendMsg
from config import user

from public.glo import Glo
from public.btn import Btn
# from gongfang import Gongfang
# from ring import Ring
# from bangpai import Bangpai


class Run(object):
    def __init__(self):
        self.startTime = datetime.now()
        self.g = Glo()
        self.totalTime = 0
        self.hwndList = []
        self.single = False

    def runOver(self):
        self.endTime = datetime.now()
        totalTime = (self.endTime - self.startTime).seconds
        self.m = int(totalTime / 60)
        self.totalTime += self.m

    def pushMsg(self, groupNo, shutdown=False):
        self.runOver()
        msg = '完成第' + str(groupNo) + '组号, 用时' + str(self.m) + '分钟'
        self.startTime = datetime.now()

        if groupNo == len(user.ACCTZU):
            currentHour = datetime.today().hour
            currentWeek = datetime.today().isoweekday()
            if currentHour <= 6 or (
                (currentWeek == 1 or currentWeek == 4 or currentWeek == 5)
                    and currentHour <= 17):
                shutdown = True

        if shutdown:
            msg += '全部完成，关机'
            SendMsg(msg)
            os.system(f'shutdown -s -t 300')
        else:
            SendMsg(msg)

    def richang(self, screen, windowClass, lock, myDict, q):
        try:
            q.put(screen)
            currentHour = datetime.today().hour
            currentWeek = datetime.today().isoweekday()
            g = Glo()
            g.set('screen', screen)
            g.set('windowClass', windowClass)
            g.set('lock', lock)
            g.set('config', myDict)

            Info().getInfo()

            name = self.g.get('name')
            level = self.g.get('level')

            Guajiang().start()

            # if level >= 60:
                # GengZhong().start()

            if not self.single:
                if myDict['ZG']:
                    Zhuogui().start()

                if myDict['FB']:
                    if currentWeek <= 6:
                        FuBen('jcx').start()
                    
                    if currentWeek % 3 == 1:
                        FuBen('ecy').start()

                    if currentWeek == 2 or currentWeek > 5:
                        FuBen('lls').start()

                    if currentWeek == 3 or currentWeek == 5:
                        FuBen('lyrm').start()


            Lidui().start()

            # if level >= 60:
                # GengZhong().start()

            Shimen().start()

            Baotu().start()

            Mijing().start()

            currentHour = datetime.today().hour
            if currentHour >= 11:
                SJQY().start()

            currentHour = datetime.today().hour
            if currentWeek <= 5 and currentHour >= 17:
                KJXS().start()

            Yunbiao().start()

            LQHYD().start()

            # if level >= 60:
                # GengZhong().start()

            Clean().start()

            # if currentWeek == 1:
                # if level >= 50 and level <= 69:
                    # Ring().start()
                    # Bangpai().start()

                # if level >= 60:
                    # Gongfang().start()
                    
            # currentHour = int(time.strftime('%H', time.localtime()))
            # currentHour = 8
            # if int(level) < 69 and currentHour >= 8:
            # Upgrade().start()

            log(f'账号：{name}  完成!!!!!!!!!!!!!!')
            q.get(screen)

            # while q.qsize():
                # pass

            Logout().start(myDict['NEXT'])

            return 1
        except BaseException as e:
            print('日常错误:', e)

    def getHwndList(self):
        self.hwndList = []
        isStart = False
        hwnd = 0
        while not isStart:
            if not isStart and hwnd == 0:
                hwnd = win32gui.FindWindow(None, "《梦幻西游》手游")
            else:
                hwnd = win32gui.FindWindowEx(None, hwnd, None, "《梦幻西游》手游")
            if hwnd:
                self.hwndList.append(hwnd)
            else:
                isStart = True

    def openGame(self):
        if (len(self.hwndList)) == 5:
            return
        os.system('start C:\\Users\\DX\\Desktop\\duokai\\mhxy.exe')
        sleep(2)

        while True:
            hwnd = win32gui.FindWindow(None, 'UnityWndClass')
            if hwnd:
                break
            sleep(1)

        mnqBtn = Btn(hwnd)
        for i in range(5):
            mnqBtn.LBtn(((350, 150), (2, 2)))
            sleep(8)

        os.system('taskkill /F /IM mhxy.exe')
        sleep(1)

        return

    def start(self, shutdown=False, single=False):
        try:
            self.single = single
            import pythoncom
            pythoncom.CoInitialize()
            log('-------------------------------------开始执行--------------------------------------')

            for index in range(len(user.ACCTZU)):
                GROUP_NO = index + 1
                # 登陆/切换账号
                self.getHwndList()
                if user.ACCTZU[index]['status']:
                    if not single:
                        self.openGame()
                    self.getHwndList()
                    log(f'开始第{GROUP_NO}组号')
                    Login(index, self.hwndList).login()

                    # 进程共享数据
                    lock = Manager().Lock()
                    d = Manager().dict()
                    q = Manager().Queue()
                    for key in user.ACCTZU[index]['config']:
                        d[key] = user.ACCTZU[index]['config'][key]

                    p = Pool(len(self.hwndList))
                    for i in range(len(self.hwndList)):
                        p.apply_async(self.richang,
                                      args=(str(i), self.hwndList[i], lock, d, q))
                        sleep(1)
                    p.close()
                    p.join()

                    log(f'完成第{GROUP_NO}组号')
                    self.pushMsg(GROUP_NO)
                else:
                    log(f'第{GROUP_NO}组号不执行')

                sleep(2)

            log('运行完成')
            self.pushMsg(0, shutdown)

        except BaseException as e:
            print(e)
            # self.pushMsg(-1, True)

    def timingStart(self, timingTime, shutdown):
        time = timingTime.split(':')
        self.hour = time[0]
        self.minute = time[1]
        log(f'开始定时任务，时间为{self.hour}时{self.minute}分')
        scheduler = BlockingScheduler()
        scheduler.add_job(self.start,
                          'cron',
                          hour=self.hour,
                          minute=self.minute,
                          args=shutdown)
        scheduler.start()


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('--shutdown', '-s', action='store_true', default=False)
        parser.add_argument('--time', '-t', type=str)
        parser.add_argument('--self', action='store_true', default=False)
        args = parser.parse_args()
        
        if args.time:
            Run().timingStart(args.time, args.shutdown, args.self)
        else:
            Run().start(args.shutdown, args.self)

    except Exception as e:
        traceback.print_exc()
        log(e, True)