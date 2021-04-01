import time
from time import sleep
from public.cutScreen import CScreen
from public.btn import Btn
from public.matchTem import Match
from public.smc import SMC
from public.glo import Glo
from public.log import log
import threading

class Baotu:
    def __init__(self):
        self.g = Glo()
        self.name = self.g.get('name')
        self.B = Btn()
        self.cutScreen = CScreen().cutScreen
        self.matchTem = Match().matchTem
        self.smc = SMC().smc
        self.smca = SMC().smca
        self.complete = False
        self.processing = False

    def empty(self):
        self.B.Hotkey("bb")
        sleep(0.5)

        self.smc('bb_zl')

        self.B.MBtn(720, 440)
        self.B.VBtn(1, 50)
        sleep(1)

        useComplete = False
        page = 1
        while True:
            res = self.smc('bb_cbt', count=2, sleepT=0.5)
            if res != 0:
            	res = self.smc('bb_cbt', count=2, sleepT=0.5)
            	if res == 0:
	                break
            else:
                self.B.MBtn(700, 400)
                self.B.VBtn(-1, 6)
                page += 1
                if page == 6:
                    log(f"账号: { self.name } 无藏宝图")
                    useComplete = True
                    self.B.RBtn()
                    break

            sleep(0.5)

        return useComplete

    def dig(self):
        log(f"账号: { self.name } 开始挖藏宝图")
        # 打开背包
        empty = self.empty()
        useComplete = False

        count = 0
        if not empty:
            log(f"账号: { self.name } 挖宝中")
            
            while not empty:
                timer1 = time.time()
                timer2 = time.time()
                while not useComplete:
                    res = self.smc('hd', count=0)
                    if res != 0:
                        self.cutScreen()
                        btnCoor = self.matchTem('sy')
                        compareResult = self.g.compare()
                        if btnCoor != 0 and compareResult == True:
                            if btnCoor[0][0] + btnCoor[1][0] < 920:
                                # print('使用藏宝图中')
                                count += 1
                                log('使用一张藏宝图')
                                self.B.LBtn(btnCoor)
                                sleep(4)
                                timer1 = time.time()
                                timer2 = time.time()

                        elif btnCoor == 0 and compareResult == True:
                            # print('站立不动状态')
                            timer2 = time.time()

                        else:
                            timer1 = time.time()
                            timer2 = time.time()
                            # print('找藏宝图中')

                    else:
                        # print('打怪中')
                        timer1 = time.time()
                        timer2 = time.time()
                        res = self.smc('sy')
                        if res != 0:
                            self.B.RBtn()

                    if timer2 - timer1 >= 12:
                        useComplete = True
                        break

                empty = self.empty()
                useComplete = empty

        log(f"账号：{ self.name } 挖了 {count} 张藏宝图")

    def isComplete(self):
        complete = False
        self.B.Hotkey('hd')

        self.smc('rchd', sleepT=0.5)

        self.B.MBtn(590, 330)
        self.B.VBtn(1, 21)
        sleep(0.5)

        for n in range(21):
            if n % 10 == 0:
                sleep(0.5)
                res = self.smca(['bt_wc', 'bt_wc1'], simi=0.9, count=0)
                if res != 0:
                    log(f"账号: { self.name } 宝图任务已完成")
                    complete = True
                    break
            else:
                self.B.VBtn(-1)

        self.B.VBtn(1, 21)

        self.B.RBtn()

        return complete

    def timing(self):
        self.complete = True
        self.processing = False

    def start(self):
        try:
            t = threading.Timer(900, self.timing)
            t.start()
            log(f"账号: { self.name } 开始宝图任务")

            while True:
                res = self.smc('hd', count=0)
                if res == 0:
                    self.B.RBtn()
                else:
                    self.B.MBtn(900, 300)
                    self.B.VBtn(1, 10)
                    sleep(0.5)

                    temCoor = self.matchTem('bt_btrw')
                    if temCoor != 0:
                        print(f"账号: { self.name } 已领取宝图任务")
                        self.processing = True
                    sleep(0.5)
                    break

            self.complete = self.isComplete()

            if not self.complete:
                print(f"账号: { self.name } 宝图任务进行中")

                if not self.processing:
                    self.B.Hotkey('hd')
                    self.smc('rchd', sleepT=0.5)
                    page = 1
                    while True:
                        self.cutScreen()
                        temCoor = self.matchTem('hd_btrw', simi=0.7) or self.matchTem('hd_btrw1', simi=0.7)
                        if temCoor != 0:
                            btnCoor = self.matchTem('cj', 'imgTem/hd_btrw') or self.matchTem('cj', 'imgTem/hd_btrw1')
                            newCoor = ((temCoor[0][0] + btnCoor[0][0], temCoor[0][1] + btnCoor[0][1]), btnCoor[1])
                            if btnCoor != 0:
                                self.B.LBtn(newCoor)
                                self.processing = True
                                break
                        else:
                            page += 1
                            self.B.VBtn(-1, 10)
                            sleep(0.5)
                            if page == 4:
                                break

                xhList = ['bt_cbthdwc', 'bt_ttwf', 'bt_btrw']
                # sTime = time.time()
                # eTime = time.time()

                while self.processing:
                    self.cutScreen()
                    temCoor = self.matchTem('hd')
                    if temCoor != 0:
                        for item in xhList:
                            self.cutScreen()
                            btnCoor = self.matchTem(item)
                            if btnCoor != 0:
                                # sTime = time.time()
                                if item == 'bt_cbthdwc':
                                    self.complete = True
                                    sleep(1)
                                    break

                                elif item == 'bt_ttwf':
                                    self.B.LBtn(btnCoor, sleepT=0.5)
                                    self.B.RBtn()
                                    xhList.remove('bt_ttwf')

                                elif item == 'bt_btrw':
                                    self.B.LBtn(btnCoor)
                                    sleep(10)

                            else:
                                self.B.MBtn(900, 300)
                                self.B.VBtn(1, 10)
                                sleep(0.5)
                                
                                res = self.smc('bt_btrw')
                                if res == 0:
                                    self.complete = self.isComplete()
                                    if self.complete:
	                                    self.processing = not self.complete
	                                    log(f"账号: { self.name } 宝图任务完成")
	                                    break
                                
                                # eTime = time.time()
                                # if eTime - sTime > 60:
                                #     log(f"账号: { self.name } 宝图任务完成")
                                #     complete = True
                                #     processing = False
                                #     sleep(1)
                                #     break
                    # else:
                    #     sTime = time.time()
                    #     eTime = time.time()

                sleep(0.5)
                # count = 0
                # while True:
                #     if count >= 4:
                #         break
                #     self.cutScreen()
                #     temCoor = self.matchTem('hd')
                #     btnCoor = self.matchTem('sy')
                #     if temCoor != 0 and btnCoor != 0:
                #         count += 1
                #         self.B.LBtn(btnCoor, sleepT=0.5)
                #     elif temCoor != 0 and btnCoor == 0:
                #         break
                #     else:
                #         self.B.RBtn()
                #     sleep(0.5)

            self.dig()

            if self.complete:
                log(f"账号: { self.name } 宝图任务结束")
                t.cancel()
                return 1
            else:
                self.start()
        
        except Exception as e:
            log(e, True)

if __name__ == '__main__':
    Baotu().start()