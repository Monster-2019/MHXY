from time import sleep
from cutScreen import CScreen
from btn import Btn
from matchTem import Match
from smc import SMC
from glo import Glo
from log import log
import threading


class Mijing:
    def __init__(self):
        self.g = Glo()
        self.name = Glo().get('name')
        self.B = Btn()
        self.cutScreen = CScreen().cutScreen
        self.matchTem = Match().matchTem
        self.smc = SMC().smc
        self.complete = False
        self.processing = False

    def timing(self):
        self.complete = True

    def start(self):
        try:
            t = threading.Timer(1200, self.timing)
            t.start()
            log(f"账号: { self.name } 开始秘境任务")

            while self.smc("hd", count=0) == 0:
                self.B.RBtn()

            self.B.Hotkey("hd")

            self.smc("rchd", sleepT=0.5)

            self.B.MBtn(590, 330)
            self.B.VBtn(1, 31)
            sleep(0.5)

            self.complete = True

            for n in range(31):
                if n % 10 == 0:
                    sleep(0.5)
                    res = self.smc('hd_mjxy', simi=0.999, count=0)
                    if res:
                        self.cutScreen()
                        temCoor = self.matchTem('hd_mjxy') or self.matchTem(
                            'hd_mjxy1')
                        if temCoor != 0:
                            btnCoor = self.matchTem(
                                'cj', 'imgTem/hd_mjxy') or self.matchTem(
                                    'cj', 'imgTem/hd_mjxy1')
                            newCoor = ((temCoor[0][0] + btnCoor[0][0],
                                        temCoor[0][1] + btnCoor[0][1]),
                                       btnCoor[1])
                            if btnCoor:
                                self.B.LBtn(newCoor, sleepT=3)
                                self.complete = False
                                self.processing = True
                                break

                else:
                    self.B.VBtn(-1)

            if self.complete:
                self.B.RBtn()

            xhList = [
                'mj_mjxy', 'mj_jr', 'qd', 'mj_one', 'mj_tz'
            ]
            # 'mj_mrh', 'mj_yjf', 'mj_esg', 
            if self.processing:
                while self.processing:
                    for item in xhList:
                        self.cutScreen()
                        btnCoor = self.matchTem(item)
                        if btnCoor:
                            if item == 'mj_one':
                                self.B.LBtn(((btnCoor[0][0] + 46, btnCoor[0][1] - 60), btnCoor[1]))

                            elif item == 'mj_jr':
                                self.B.LBtn(btnCoor, maxx=500)

                            elif item == 'mj_tz':
                                self.B.LBtn(btnCoor)
                                self.processing = False
                                break

                            else:
                                self.B.LBtn(btnCoor)

                self.processing = True

            xhList = ['sb', 'mj_tg', 'mj_mjxyrw', 'mj_lb', 'mj_jrzd', 'mj_gb']
            # , 'mj_lq', 'mj_gb'

            sleep(3)

            while self.processing:
                for item in xhList:
                    self.cutScreen()
                    isHd = self.matchTem('hd')
                    if isHd:
                        self.complete = True
                        self.processing = False
                        break
                    isFl = self.matchTem('fl')
                    compare = self.g.compare()
                    if item == 'mj_mjxyrw':
                        btnCoor = self.matchTem(item, simi=0.8)
                    else:
                        btnCoor = self.matchTem(item)
                    if btnCoor:
                        if item == 'sb' or item == 'mj_tg':
                            self.B.LBtn(btnCoor)
                            # self.B.LBtn(((520, 380), (10, 10)))
                            self.complete = True
                            self.processing = False
                            break

                        elif item == 'mj_mjxyrw' and isFl and compare:
                            self.B.LBtn(btnCoor, sleepT=2, minx=700)

                        else:
                            self.B.LBtn(btnCoor, minx=350)

                    sleep(0.5)

            while self.smc('hd') == 0:
                self.smc('mj_lk')

            if self.complete:
                log(f"账号: { self.name } 秘境任务结束")
                t.cancel()
                return 1
            else:
                self.start()

        except Exception as e:
            log(e, True)


if __name__ == '__main__':
    Mijing().start()