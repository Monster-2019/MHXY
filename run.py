import sys
sys.path.append('.')
sys.path.append('..')
from apscheduler.schedulers.blocking import BlockingScheduler
from multiprocessing import Pool, Lock, Manager, Queue
from datetime import datetime
from time import sleep
import requests
import random
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
from bangpai import Bangpai
from trading import Trading
from clean import Clean
from logout import Logout
from changeAcct import ChangeAcct
import config

from public.glo import Glo

class Run(object):
    def __init__(self):
        self.startTime = datetime.now()
        self.g = Glo()
        self.totalTime = 0

    def runOver(self):
        self.endTime = datetime.now()
        totalTime = (self.endTime - self.startTime).seconds
        self.m = int(totalTime / 60)
        self.totalTime += self.m

    def pushMsg(self, groupNo, shutdown=False):
        self.runOver()
        url = 'https://sc.ftqq.com/SCU69656T782d340ca550c446fba0708c1436e3af5e2aadb811f2f.send'
        msg = '完成第' + str(groupNo) + '组号, 用时' + str(self.m) + '分钟'
        param = {
            'text': msg
        }
        requests.post(url, param)
        self.startTime = datetime.now()
            
        if groupNo == len(config.ACCTZU):
            url = 'https://sc.ftqq.com/SCU69656T782d340ca550c446fba0708c1436e3af5e2aadb811f2f.send'
            msg = '全部完成，共用时' + str(self.totalTime) + '分钟'
            param = {
                'text': msg
            }
            requests.post(url, param)
            currentHour = datetime.today().hour
            currentWeek = datetime.today().isoweekday()
            if currentHour <= 6 or ((currentWeek == 1 or currentWeek == 4 or currentWeek == 5) and currentHour <= 17):
                shutdown = True

        if shutdown:
            os.system(f'shutdown -s -t 3')

    def richang(self, windowClass, lock, myDict):
        currentHour = datetime.today().hour
        currentWeek = datetime.today().isoweekday()
        g = Glo()
        g.set('lock', lock)
        g.set('config', myDict)

        Info(windowClass).getInfo()

        name = self.g.get('name')
        level = self.g.get('level')

        Guajiang().start()

        if level >= 60:
            GengZhong().start()

        if myDict['ZG']:
            Zhuogui().start()

        if myDict['FB']:
            LLSPT().start()

        Lidui().start()

        if level >= 60:
            GengZhong().start()
            
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

        if level >= 60:
            GengZhong().start()

        # currentHour = int(time.strftime('%H', time.localtime()))
        # if int(level) < 69 and currentHour >= 8:
        #     Upgrade().start()

        Clean().start()

        # if myDict['CJMY']:
        #     Bangpai().start()
        #     Trading().start()

        count = self.g.get('count')
        log(f'账号：{name}, 当前等级{level}, 调用{ count }次接口')

        Logout().start(myDict['NEXT'])

    def start(self):
        try:
            import pythoncom
            pythoncom.CoInitialize()
            clearFile()
            log('----------------------------------------------------------------------------------------')
            log('开始执行')

            for index in range(len(config.ACCTZU)):
                GROUP_NO = index + 1
                # 登陆/切换账号
                if config.ACCTZU[index]['status']:
                    log(f'开始第{GROUP_NO}组号')
                    ChangeAcct().start(index)

                    # 进程共享数据
                    lock = Manager().Lock()
                    d = Manager().dict()
                    for key in config.ACCTZU[index]['config']:
                        d[key] = config.ACCTZU[index]['config'][key]

                    p = Pool(5)
                    for i in config.ACCT_LIST:
                        p.apply_async(self.richang, args=(i, lock, d))
                        sleep(1)
                    p.close()
                    p.join()

                    log(f'完成第{GROUP_NO}组号')
                else:
                    log(f'第{GROUP_NO}组号不执行')

                self.pushMsg(GROUP_NO)
                # del config.ACCTZU[0]
                sleep(2)

            log('运行完成')

        except Exception as e:
            self.pushMsg(-1, True)

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