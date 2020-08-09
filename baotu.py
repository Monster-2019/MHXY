import time
from time import sleep
from public.cutScreen import CScreen
from public.btn import Btn
from public.matchTem import Match
from public.smc import SMC
from public.glo import Glo
from public.log import log

class Baotu:
    def __init__(self):
        self.g = Glo()
        self.name = self.g.get('name')
        self.B = Btn()
        self.cutScreen = CScreen().cutScreen
        self.matchTem = Match().matchTem
        self.smc = SMC().smc

    def empty(self):
        self.B.Hotkey("bb")
        sleep(0.5)

        self.cutScreen()
        btnCoor = self.matchTem('bb_zl')
        if btnCoor != 0:
            self.B.LBtn(btnCoor)

        self.B.MBtn(720, 440)
        self.B.VBtn(1, 30)
        sleep(1)

        useComplete = False
        page = 1
        while True:
            res = self.smc('bb_cbt', count=2)
            if res != 0:
                break
            else:
                self.B.MBtn(700, 400)
                self.B.VBtn(-1, 6)
                page += 1
                if page == 4:
                    log(f"账号: { self.name } 无藏宝图")
                    useComplete = True
                    self.B.RBtn()
                    break

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
                        if btnCoor != 0:
                            if btnCoor[0][0] + btnCoor[1][0] < 920:
                                # print('使用藏宝图中')
                                count += 1
                                self.B.LBtn(btnCoor, sleepT=3)
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

                    if timer2 - timer1 >= 5:
                        useComplete = True
                        break

                empty = self.empty()

        log(f"账号：{ self.name } 挖了 {count} 张藏宝图")

    def start(self):
        try:
            log(f"账号: { self.name } 开始宝图任务")
            complete = False
            processing = False

            while True:
                self.cutScreen()
                btnCoor = self.matchTem('hd')
                if btnCoor == 0:
                    self.B.RBtn()
                else:
                    self.B.MBtn(900, 300)
                    self.B.VBtn(1, 10)
                    sleep(0.5)

                    temCoor = self.matchTem('bt_btrw')
                    if temCoor != 0:
                        log(f"账号: { self.name } 已领取宝图任务")
                        processing = True
                    self.B.LBtn(btnCoor)
                    sleep(0.5)
                    break

            self.cutScreen()
            btnCoor = self.matchTem('rchd')
            if btnCoor != 0:
                self.B.LBtn(btnCoor)
                
            self.B.MBtn(590, 330)

            self.B.VBtn(1, 21)
            sleep(0.5)

            for n in range(21):
                if n % 10 == 0:
                    self.cutScreen()
                    temCoor = self.matchTem('bt_wc', simi=0.95) or self.matchTem('bt_wc1', simi=0.95)
                    if temCoor != 0:
                        log(f"账号: { self.name } 宝图任务已完成")
                        complete = True
                        break
                self.B.VBtn(-1)
            
            self.B.VBtn(1, 21)
            sleep(0.5)

            # 匹配宝图任务的参加按钮
            if not complete:
                log(f"账号: { self.name } 宝图任务进行中")
                if not processing:
                    count = 0
                    while True:
                        self.cutScreen()
                        temCoor = self.matchTem('hd_btrw', simi=0.95)
                        if temCoor != 0:
                            btnCoor = self.matchTem('cj', 'imgTem/hd_btrw')
                            newCoor = ((temCoor[0][0] + btnCoor[0][0], temCoor[0][1] + btnCoor[0][1]), btnCoor[1])
                            if btnCoor != 0:
                                self.B.LBtn(newCoor)
                                break
                        else:
                            count += 1
                            self.B.VBtn(-1, 10)
                            sleep(0.5)
                            if count == 2:
                                log(f"账号: { self.name } 宝图任务完成")
                                complete = True
                                break
                else:
                    self.B.RBtn()

                xhList = ['bt_cbthdwc', 'bt_ttwf', 'bt_btrw']
                sTime = time.time()
                eTime = time.time()
                while not complete:
                    self.cutScreen()
                    temCoor = self.matchTem('hd')
                    if temCoor != 0:
                        for item in xhList:
                            self.cutScreen()
                            btnCoor = self.matchTem(item)
                            if btnCoor != 0:
                                sTime = time.time()
                                if item == 'bt_cbthdwc':
                                    complete = True
                                    sleep(1)
                                    break

                                elif item == 'bt_ttwf':
                                    self.B.LBtn(btnCoor)
                                    xhList.remove('bt_ttwf')

                                elif item == 'bt_btrw':
                                    self.B.LBtn(btnCoor)
                                    self.B.LBtn(btnCoor)
                                    sleep(20)

                            else:
                                self.B.MBtn(900, 300)
                                self.B.VBtn(1, 10)
                                
                                eTime = time.time()
                                if eTime - sTime > 60:
                                    log(f"账号: { self.name } 宝图任务完成")
                                    complete = True
                                    sleep(1)
                                    break
                    else:
                        sTime = time.time()
                        eTime = time.time()

            else:
                self.B.RBtn()

            while True:
                self.cutScreen()
                temCoor = self.matchTem('hd')
                btnCoor = self.matchTem('sy')
                if temCoor != 0 and btnCoor != 0:
                    self.B.LBtn(btnCoor, sleepT=0.5)
                elif temCoor != 0 and btnCoor == 0:
                    break
                else:
                    self.B.RBtn()

            self.dig()

            if complete:
                log(f"账号: { self.name } 宝图任务结束")
                return 1
            else:
                self.start()
        
        except Exception as e:
            log(e, True)

if __name__ == '__main__':
    Baotu().start()
