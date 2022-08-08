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
        self.isDig = False

    def empty(self):
        while self.smc('hd', count=0) == 0:
            self.B.RBtn()
                
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
            if res:
                if self.smc('sy', sleepT=0.5):
                    self.B.RBtn()
                    break
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
        useComplete = empty

        count = 0
        if not useComplete:
            log(f"账号: { self.name } 挖宝中")
            
            standingCount = 0

            while not empty:
                self.cutScreen()
                isHd = self.matchTem('hd')
                btnCoor = self.matchTem('sy')
                compare = self.g.compare()

                # 1. 非战斗状态
                # 2-1. 寻路中  站立次数归0  
                # 2-2. 非寻路中  站立次数叠加
                if isHd:
                    if compare:
                        standingCount += 1
                        if standingCount > 10:
                            empty = True
                            useComplete = True
                            break
                        sleep(0.5)
                    else:
                        standingCount = 0

                    if btnCoor and btnCoor[0][0] + btnCoor[1][0] < 920:
                        count += 1
                        self.B.LBtn(btnCoor)
                        sleep(4)

                else:
                    standingCount = 0

                sleep(1)

        log(f"账号：{ self.name } 挖了 {count} 张藏宝图")
        return 1

    def timing(self):
        self.complete = True
        self.processing = False
        self.isDig = False

    def start(self):
        try:
            t = threading.Timer(1200, self.timing)
            t.start()
            log(f"账号: { self.name } 开始宝图任务")

            while self.smc('hd', count=0) == 0:
                self.B.RBtn()
            
            # 已领取
            # self.B.MBtn(900, 300)
            # self.B.VBtn(1, 20)
            # sleep(0.5)

            # if self.matchTem('bt_btrw', simi=0.95):
            #     print(f"账号: { self.name } 已领取宝图任务")
            #     self.processing = True
            # sleep(0.5)

            self.B.Hotkey("hd")

            self.smc("rchd", sleepT=0.5)

            self.B.MBtn(590, 330)
            self.B.VBtn(1, 31)
            sleep(0.5)

            for n in range(31):
                if n % 10 == 0:
                    sleep(0.5)
                    if self.smc("bt_wc", simi=0.999, count=0):
                        log(f"账号: { self.name } 宝图任务已完成")
                        self.complete = True
                        self.B.RBtn()
                        break

                    else:
                        self.cutScreen()
                        temCoor = self.matchTem("hd_btrw") or self.matchTem("hd_btrw1")
                        if temCoor:
                            btnCoor = self.matchTem(
                                "cj", "imgTem/hd_btrw"
                            ) or self.matchTem("cj", "imgTem/hd_btrw1")
                            newCoor = (
                                (
                                    temCoor[0][0] + btnCoor[0][0],
                                    temCoor[0][1] + btnCoor[0][1],
                                ),
                                btnCoor[1],
                            )
                            if btnCoor:
                                self.B.LBtn(newCoor)
                                self.processing = True
                                sleep(5)

                                while True:
                                    if self.smc('bt_ttwf'):
                                        break

                                    sleep(2)
                                
                                break
                else:
                    self.B.VBtn(-1)

            self.B.RBtn()

            if not self.complete:
                print(f"账号: { self.name } 宝图任务进行中")

                xhList = ['bt_cbthdwc', 'bt_btrw']

                while self.processing:
                    for item in xhList:
                        self.cutScreen()
                        isHd = self.matchTem('hd')
                        compare = self.g.compare()
                        if item == 'bt_btrw':
                            btnCoor = self.matchTem(item, simi=0.9)
                        else:
                            btnCoor = self.matchTem(item)
                        if btnCoor and isHd:
                            if item == 'bt_cbthdwc':
                                self.complete = True
                                self.processing = False
                                self.isDig = True
                                sleep(1)
                                break

                            if item == 'bt_btrw' and isHd and compare:
                                self.B.LBtn(btnCoor, gtx=800)
                                sleep(5)

                        elif item == 'bt_btrw' and not btnCoor and isHd and compare:
                            sleep(20)
                            self.cutScreen()
                            isHd = self.matchTem('hd')
                            compare = self.g.compare()
                            if isHd and compare:
                                self.complete = True
                                self.processing = False
                                self.isDig = True
                                break


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