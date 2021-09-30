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
            res = self.smc('bb_cbt', sleepT=1)
            if res != 0:
                self.smc('bb_sy', sleepT=0.5)
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
                while not useComplete:
                    btnCoor = self.smc('sy', count=0)
                    if btnCoor != 0:
                        if btnCoor[0][0] + btnCoor[1][0] < 920:
                            count += 1
                            self.B.LBtn(btnCoor)
                            sleep(4)

                    else:
                        if self.smc('hd', count=0):
                            compare = False
                            for i in range(3):
                                self.cutScreen()
                                compare = self.g.compare()
                                if compare:
                                    break
                                sleep(0.5)

                            if compare:
                                break
                                
                    sleep(1)

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
                res = self.smc('bt_wc', simi=0.999, count=0)
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

            while self.smc('hd', count=0) == 0:
                self.B.RBtn()
            
            self.B.MBtn(900, 300)
            self.B.VBtn(1, 20)
            sleep(0.5)

            if self.matchTem('bt_btrw', simi=0.95):
                print(f"账号: { self.name } 已领取宝图任务")
                self.processing = True
            sleep(0.5)

            if not self.processing:
                self.complete = self.isComplete()

            if not self.complete:
                print(f"账号: { self.name } 宝图任务进行中")

                if not self.processing:
                    self.B.Hotkey('hd')
                    self.smc('rchd', sleepT=0.5)
                    page = 1
                    while True:
                        self.cutScreen()
                        temCoor = self.matchTem('hd_btrw') or self.matchTem(
                            'hd_btrw1')
                        if temCoor != 0:
                            btnCoor = self.matchTem(
                                'cj', 'imgTem/hd_btrw') or self.matchTem(
                                    'cj', 'imgTem/hd_btrw1')
                            newCoor = ((temCoor[0][0] + btnCoor[0][0],
                                        temCoor[0][1] + btnCoor[0][1]),
                                       btnCoor[1])
                            if btnCoor != 0:
                                self.B.LBtn(newCoor)
                                self.processing = True
                                sleep(5)

                                while True:
                                    r = self.smc('bt_ttwf')
                                    if r != 0:
                                        break

                                    sleep(3)

                                break
                        else:
                            page += 1
                            self.B.VBtn(-1, 10)
                            sleep(0.5)
                            if page == 4:
                                break

                xhList = ['bt_cbthdwc', 'bt_btrw']

                while self.processing:
                    for item in xhList:
                        self.cutScreen()
                        isHd = self.matchTem('hd')
                        if item == 'bt_btrw':
                            btnCoor = self.matchTem(item, simi=0.95)
                        else:
                            btnCoor = self.matchTem(item)
                        if btnCoor != 0:
                            if item == 'bt_cbthdwc':
                                self.complete = True
                                sleep(1)
                                break

                            else:
                                self.B.LBtn(btnCoor)

                        else:
                            if item == "bt_btrw" and isHd:
                                sleep(2)
                                compare = False
                                for i in range(5):
                                    self.cutScreen()
                                    compare = self.g.compare()
                                    if compare:
                                        break
                                    sleep(0.5)

                                if compare:
                                    self.processing = not self.isComplete()

                        sleep(1)

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