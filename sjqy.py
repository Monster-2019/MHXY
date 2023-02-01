from time import sleep
from cutScreen import CScreen
from btn import Btn
from match import Match
from smc import SMC
from glo import Glo
from log import log
import threading

class SJQY:
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
            t = threading.Timer(300, self.timing)
            t.start()
            log(f"账号: { self.name } 开始三界奇缘任务")

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
                    if self.smc('sj_wc', simi=0.999, count=0):
                        log(f"账号: { self.name } 三界奇缘任务已完成")
                        self.complete = True
                        self.B.RBtn()
                        break

                    else:
                        self.cutScreen()
                        temCoor = self.matchTem('hd_sjqy') or self.matchTem('hd_sjqy1')
                        if temCoor:
                            btnCoor = self.matchTem('cj', 'imgTem/hd_sjqy') or self.matchTem('cj', 'imgTem/hd_sjqy1')
                            newCoor = ((temCoor[0][0] + btnCoor[0][0], temCoor[0][1] + btnCoor[0][1]), btnCoor[1])
                            if btnCoor:
                                self.B.LBtn(newCoor, sleepT=1)
                                if self.smc('sj_start', count=0):
                                    self.processing = True
                                    break

                else:
                    self.B.VBtn(-1)


            if not self.complete:
                while self.processing:
                    res = self.smc('sj_dw', count=0)
                    if res:
                        self.B.RBtn()
                        self.complete = True
                        self.processing = False
                        break
                    else:
                        self.B.LBtn(((380, 230), (170, 240)), sleepT=0.5)

                while True:
                    self.cutScreen()
                    isHd = self.matchTem('hd')
                    btnCoor = self.matchTem('sygb')
                    if isHd and btnCoor:
                        self.B.LBtn(btnCoor, sleepT=0.5)
                    elif isHd and btnCoor == 0:
                        break
                    else:
                        self.B.RBtn()
                    sleep(0.5)

            if self.complete:
                log(f"账号: { self.name } 三界奇缘任务结束")
                return 1
            else:
                self.start()

        except Exception as e:
            log(e, True)

if __name__ == '__main__':
    SJQY().start()
