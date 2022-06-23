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
        self.processing = False

    def timing(self):
        self.complete = True
        self.processing = False

    def start(self):
        try:
            t = threading.Timer(900, self.timing)
            t.start()
            log(f"账号: { self.name } 开始运镖任务")

            while self.smc("hd", count=0) == 0:
                self.B.RBtn()

            self.B.Hotkey("hd")

            self.smc("rchd", sleepT=0.5)

            self.B.MBtn(590, 330)
            self.B.VBtn(1, 31)
            sleep(0.5)

            for n in range(31):
                if n % 10 == 0:
                    sleep(0.5)
                    if self.smc('yb_wc', simi=0.999, count=0):
                        log(f"账号: { self.name } 运镖任务已完成")
                        self.complete = True
                        break
                    
                    else:
                        self.cutScreen()
                        temCoor = self.matchTem('hd_yb1') or self.matchTem(
                            'hd_yb')
                        if temCoor:
                            btnCoor = self.matchTem(
                                'cj', 'imgTem/hd_yb1') or self.matchTem(
                                    'cj', 'imgTem/hd_yb')
                            newCoor = ((temCoor[0][0] + btnCoor[0][0],
                                        temCoor[0][1] + btnCoor[0][1]),
                                       btnCoor[1])
                            if btnCoor:
                                self.B.LBtn(newCoor)
                                self.processing = True
                                break

                else:
                    self.B.VBtn(-1)

            if not self.complete:
                count = 0
                xhList = ['yb_ys', 'qd']
                while self.processing:
                    isHd = self.smc('hd', count=0)
                    if isHd:
                        if count >= 3:
                            self.complete = True
                            self.processing = False
                            break
                        while self.smc('hd', count=0):
                            self.smca(xhList)

                        count += 1

                    sleep(5)

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