import sys
sys.path.append('.')
sys.path.append('..')
from apscheduler.schedulers.blocking import BlockingScheduler
from multiprocessing import Pool, Lock, Manager, Queue
from datetime import datetime
from time import sleep
import requests
import argparse
import signal
import random
import time
import pdb
import os
import traceback

from public.log import log, clearFile
from guajiang import Guajiang
from public.getInfo import Info
from zhuogui import Zhuogui
from lls_pt import LLSPT
from public.lidui import Lidui
from shimen import Shimen
from baotu import Baotu
from mijing import Mijing
from yunbiao import Yunbiao
from sjqy import SJQY
from kjxs import KJXS
from lqhyd import LQHYD
from upgrade import Upgrade
from gengzhong import GengZhong
from clean import Clean
from logout import Logout
from changeAcct import ChangeAcct
import config

from public.glo import Glo

class Run(object):
    def __init__(self):
        self.startTime = datetime.now()
        self.g = Glo()

    def runOver(self):
        self.endTime = datetime.now()
        totalTime = (self.endTime - self.startTime).seconds
        self.h = int(totalTime / 3600)
        self.m = int((totalTime % 3600) / 60)
        self.s = (totalTime % 3600) % 60

    def psuhMsg(self, shutdown=False, times=30):
        self.runOver()
        url = 'https://sc.ftqq.com/SCU69656T782d340ca550c446fba0708c1436e3af5e2aadb811f2f.send'
        msg = '共用' + str(self.h) + '时' + str(self.m) + '分' + str(self.s) + '秒，' + '已自动关机'
        param = {
            'text': msg
        }
        requests.post(url, param)
        currentHour = int(time.strftime('%H', time.localtime()))
        if currentHour < 8 or shutdown:
            os.system(f'shutdown -s -t {times}')

    def richang(self, windowClass, lock, myDict, groupNo):
        currentHour = int(time.strftime('%H', time.localtime()))
        currentWeek = int(time.strftime('%w', time.localtime()))
        g = Glo()
        g.set('lock', lock)
        g.set('config', myDict)

        Info(windowClass).getInfo()

        name = self.g.get('name')
        level = self.g.get('level')

        Guajiang().start()
        # if res == 1: log(f'账号:{name}  ---  刮奖完成')

        if level >= 60:
            GengZhong().start()
        # if res == 1: log(f"账号：{name}  ---  耕种完成")

        if myDict['ZG']:
            Zhuogui().start()
            # if res == 1: log(f'账号:{name}  ---  捉鬼完成')

        if myDict['FB']:
            LLSPT().start()
            # if res == 1: log(f'账号：{name}  ---  琉璃碎普通副本完成')

        Lidui().start()
        # if res == 1: log(f'账号：{name}  ---  已离队')

        if level >= 60:
            GengZhong().start()
        # if res == 1: log(f"账号：{name}  ---  耕种完成")
            
        Shimen().start()
        # if res == 1: log(f"账号：{name}  ---  师门任务完成")

        Baotu().start()
        # if res == 1: log(f"账号：{name}  ---  宝图任务完成")

        Mijing().start()
        # if res == 1: log(f"账号：{name}  ---  秘境任务完成")

        currentHour = int(time.strftime('%H', time.localtime()))
        if currentHour >= 11:
            SJQY().start()
            # if res == 1: log(f"账号：{name}  ---  三界奇缘任务完成")

        currentHour = int(time.strftime('%H', time.localtime()))
        if currentWeek > 0 and currentWeek <= 5 and currentHour >= 17:
            KJXS().start()
            # if res == 1: log(f"账号：{name}  ---  科举乡试任务完成")

        Yunbiao().start()
        # if res == 1: log(f"账号：{name}  ---  运镖任务完成")

        LQHYD().start()

        if level >= 60:
            GengZhong().start()
        # if res == 1: log(f"账号：{name}  ---  耕种完成")

        # currentHour = int(time.strftime('%H', time.localtime()))
        # if int(level) < 69 and currentHour >= 8:
        #     Upgrade().start()
        #     if res == 1: log(f"账号：{name}  ---  剧情完成")

        Clean().start()

        count = self.g.get('count')
        log(f'账号：{name}, 当前等级{level}, 调用{ count }次接口')

        log(f'账号：{name}开始背包整理时间')
        sleep(30)
        log(f'账号：{name}背包整理时间结束')

        Logout().start(myDict['NEXT'])
        # if res == 1: log(f"账号：{name}  ---  已登出")

    def start(self):
        try:
            import pythoncom
            pythoncom.CoInitialize()
            clearFile()
            log('----------------------------------------------------------------------------------------')
            log('多进程已开启')

            for index in range(len(config.ACCTZU)):
                log(f'开始第{index + 1}组号')
                # 登陆/切换账号
                ChangeAcct().start()

                # 进程共享数据
                lock = Manager().Lock()
                manager = Manager()
                d = manager.dict()
                for key in config.ACCTZU[0]['config']:
                    d[key] = config.ACCTZU[0]['config'][key]

                p = Pool(5)
                for i in config.ACCT_LIST:
                    p.apply_async(self.richang, args=(i, lock, d, index))
                    sleep(1)
                p.close()
                p.join()

                log(f'完成第{index + 1}组号')

                del config.ACCTZU[0]
                sleep(2)

            log('运行完成')

            self.psuhMsg()
        except Exception as e:
            self.psuhMsg(True)

    def timingStart(self, timingTime):
        time = timingTime.split(':')
        self.hour = time[0]
        self.minute = time[1]
        log(f'开始定时任务，时间为{self.hour}时{self.minute}分')
        scheduler = BlockingScheduler()
        scheduler.add_job(self.start, 'cron', hour=self.hour, minute=self.minute)
        scheduler.start()

if __name__ == "__main__":
    try:
        if len(sys.argv) == 2:
            if sys.argv[1] == '-t':
                timing = input('请输入定时事件：')
                Run().timingStart(timing)
            else:
                log('无该参数')
        else:
            Run().start()
    except Exception as e:
        traceback.print_exc()
        log(e, True)