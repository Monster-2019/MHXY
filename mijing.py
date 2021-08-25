from time import sleep
from public.cutScreen import CScreen
from public.btn import Btn
from public.matchTem import Match
from public.smc import SMC
from public.glo import Glo
from public.log import log
import threading


class Mijing:
    def __init__(self):
        self.name = Glo().get('name')
        self.B = Btn()
        self.cutScreen = CScreen().cutScreen
        self.matchTem = Match().matchTem
        self.smc = SMC().smc
        self.complete = False
        self.processing = False

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
                self.cutScreen()
                res = self.matchTem('hd_mjxy') or self.matchTem('hd_mjxy1')
                if res != 0:
                    self.cutScreen(res)
                    res = self.matchTem('hd_no', simi=0.97)
                    if res == 0:
                        complete = True
                        log(f"账号: { self.name } 秘境任务已完成")
                        break
            self.B.VBtn(-1)

        self.B.VBtn(1, 21)

        self.B.RBtn()

        return complete

    def timing(self):
        self.complete = True

    def start(self):
        try:
            t = threading.Timer(1200, self.timing)
            t.start()
            log(f"账号: { self.name } 开始秘境任务")

            while True:
                res = self.smc('hd', count=0)
                if res == 0:
                    self.B.RBtn()
                else:
                    break

            self.complete = self.isComplete()

            # 匹配秘境降妖
            if not self.complete:
                log(f"账号: { self.name } 秘境任务进行中")

                if not self.processing:
                    self.B.Hotkey('hd')
                    self.smc('rchd', sleepT=0.5)
                    page = 1
                    while True:
                        self.cutScreen()
                        temCoor = self.matchTem(
                            'hd_mjxy', simi=0.9) or self.matchTem('hd_mjxy1',
                                                                  simi=0.9)
                        if temCoor != 0:
                            btnCoor = self.matchTem(
                                'cj', 'imgTem/hd_mjxy') or self.matchTem(
                                    'cj', 'imgTem/hd_mjxy1')
                            newCoor = ((temCoor[0][0] + btnCoor[0][0],
                                        temCoor[0][1] + btnCoor[0][1]),
                                       btnCoor[1])
                            if btnCoor != 0:
                                self.B.LBtn(newCoor)
                                self.processing = True
                                break

                        else:
                            page += 1
                            self.B.VBtn(-1, 10)
                            sleep(0.5)
                            if page == 4:
                                self.complete = True
                                self.processing = False
                                break

                xhList = [
                    'mj_mjxy', 'mj_jr', 'qd', 'mj_mrh', 'mj_yjf', 'mj_nz',
                    'mj_tz'
                ]
                if self.processing:
                    while self.processing:
                        for item in xhList:
                            res = self.smc(item, sleepT=1)
                            if res != 0 and item == 'mj_tz':
                                self.processing = False
                                break

                    self.processing = True

                xhList = [
                    'hd', 'sb', 'mj_18', 'mj_tg', 'mj_mjxyrw', 'mj_lb',
                    'mj_jrzd', 'mj_lq', 'mj_gb'
                ]

                wheel = 0
                while self.processing:
                    if self.complete:
                        self.smc('mj_lk', simi=0.6)

                    for item in xhList:
                        self.cutScreen()
                        btnCoor = self.matchTem(item, simi=0.8)
                        if btnCoor != 0:
                            if item == 'hd':
                                self.processing = False
                                break

                            elif item == 'sb' or item == 'mj_18' or item == 'mj_tg' or wheel >= 3:
                                self.B.LBtn(((520, 380), (10, 10)))
                                self.B.LBtn(((520, 380), (10, 10)))
                                self.complete = True

                            elif item == 'mj_lb':
                                self.B.LBtn(btnCoor, sleepT=5)
                                wheel += 1

                            elif item == 'mj_jrzd':
                                sleep(1)
                                res = self.smc('mj_18')
                                if res != 0:
                                    self.complete = True

                                else:
                                    self.B.LBtn(btnCoor)

                            else:
                                self.B.LBtn(btnCoor)

                            sleep(2)

                while True:
                    res = self.smc('sy')
                    if res == 0:
                        break
                    sleep(0.5)

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