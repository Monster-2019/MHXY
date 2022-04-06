from time import sleep
from public.cutScreen import CScreen
from public.btn import Btn
from public.matchTem import Match
from public.smc import SMC
from public.glo import Glo
from public.log import log
import threading


class Yunbiao:
    def __init__(self):
        self.name = Glo().get('name')
        self.B = Btn()
        self.cutScreen = CScreen().cutScreen
        self.matchTem = Match().matchTem
        self.smc = SMC().smc
        self.smca = SMC().smca
        self.complete = False

    def isComplete(self):
        complete = False
        self.B.Hotkey('hd')

        self.smc('rchd', sleepT=0.5)

        self.B.MBtn(590, 330)
        self.B.VBtn(1, 31)
        sleep(0.5)

        for n in range(31):
            if n % 10 == 0:
                sleep(0.5)
                res = self.smc('yb_wc', simi=0.999, count=0)
                if res != 0:
                    log(f"账号: { self.name } 运镖任务已完成")
                    complete = True
                    break
            else:
                self.B.VBtn(-1)

        self.B.VBtn(1, 31)

        self.B.RBtn()

        return complete

    def timing(self):
        self.complete = True

    def start(self):
        try:
            t = threading.Timer(600, self.timing)
            t.start()
            log(f"账号: { self.name } 开始运镖任务")
            processing = False

            while True:
                res = self.smc('hd', count=0)
                if res == 0:
                    self.B.RBtn()
                else:
                    break

            self.complete = self.isComplete()

            if not self.complete:
                log(f"账号: { self.name } 运镖任务进行中")

                if not processing:
                    self.B.Hotkey('hd')
                    self.smc('rchd', sleepT=0.5)
                    page = 1
                    while True:
                        self.cutScreen()
                        temCoor = self.matchTem('hd_yb1') or self.matchTem(
                            'hd_yb')
                        if temCoor != 0:
                            btnCoor = self.matchTem(
                                'cj', 'imgTem/hd_yb1') or self.matchTem(
                                    'cj', 'imgTem/hd_yb')
                            newCoor = ((temCoor[0][0] + btnCoor[0][0],
                                        temCoor[0][1] + btnCoor[0][1]),
                                       btnCoor[1])
                            if btnCoor != 0:
                                self.B.LBtn(newCoor)
                                processing = True
                                break
                        else:
                            page += 1
                            self.B.VBtn(-1, 10)
                            sleep(0.5)
                            if page == 4:
                                break

                count = 0
                xhList = ['yb_ys', 'qd']
                while processing:
                    res = self.smc('hd', count=0)
                    if res != 0:
                        sleep(3)
                        btnCoor = self.smc('yb_ys')
                        if btnCoor != 0:
                            ysStatus = False
                            while not ysStatus:
                                for item in xhList:
                                    res = self.smc(item, sleepT=0.5)
                                    if res != 0 and item == 'qd':
                                        sleep(3)
                                        count += 1
                                        ysStatus = True
                                        log(f'账号: { self.name } 正在进行第{ count }轮运镖'
                                            )
                                        sleep(30)

                                        while True:
                                            res = self.smc('hd', count=0)
                                            if res != 0:
                                                break

                        else:
                            if count != 0:
                                log(f"账号: { self.name } 运镖任务完成")
                                self.complete = True
                                processing = False
                                break

                    sleep(3)

            if self.complete:
                log(f"账号: { self.name } 运镖任务结束")
                t.cancel()
                return 1
            else:
                self.start()

        except Exception as e:
            log(e, True)


if __name__ == '__main__':
    Yunbiao().start()