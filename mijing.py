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
        self.g = Glo()
        self.name = Glo().get('name')
        self.B = Btn()
        self.cutScreen = CScreen().cutScreen
        self.matchTem = Match().matchTem
        self.smc = SMC().smc
        self.complete = False
        self.processing = False

    def isComplete(self):
        complete = True
        self.B.Hotkey('hd')
        self.smc('rchd', sleepT=0.5)
        self.B.MBtn(590, 330)
        self.B.VBtn(1, 31)
        sleep(0.5)

        for n in range(31):
            if n % 10 == 0:
                sleep(0.5)
                res = self.smc('hd_mjxy', simi=0.999, count=0)
                if res != 0:
                    complete = False
                    break

            else:
                self.B.VBtn(-1)

        self.B.VBtn(1, 31)
        self.B.RBtn()

        if complete:
            log(f"账号: { self.name } 秘境任务已完成")

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
                        temCoor = self.matchTem('hd_mjxy') or self.matchTem(
                            'hd_mjxy1')
                        if temCoor != 0:
                            btnCoor = self.matchTem(
                                'cj', 'imgTem/hd_mjxy') or self.matchTem(
                                    'cj', 'imgTem/hd_mjxy1')
                            newCoor = ((temCoor[0][0] + btnCoor[0][0],
                                        temCoor[0][1] + btnCoor[0][1]),
                                       btnCoor[1])
                            if btnCoor != 0:
                                self.B.LBtn(newCoor, sleepT=3)
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
                    'mj_mjxy', 'mj_jr', 'qd', 'mj_one', 'mj_tz', 'mj_mjxyrw'
                ]
                # 'mj_mrh', 'mj_yjf', 'mj_esg', 
                if self.processing:
                    while self.processing:
                        for item in xhList:
                            res = self.smc(item, sleepT=1)
                            if res != 0:
                                if item == 'mj_one':
                                    self.B.LBtn(((res[0][0] + 46, res[0][1] - 60), res[1]))

                                if item == 'mj_mjxyrw':
                                    self.processing = False
                                    break

                    self.processing = True

                xhList = ['hd', 'sb', 'mj_tg', 'mj_mjxyrw', 'mj_lb', 'mj_jrzd', 'mj_gb', 'fl']
                # , 'mj_lq', 'mj_gb'

                while self.processing:
                    for item in xhList:
                        if self.complete:
                            self.smc('mj_lk')
                        
                        self.cutScreen()
                        btnCoor = self.matchTem(item)
                        if item == 'mj_mjxyrw':
                            btnCoor = self.matchTem(item, simi=0.9)
                        if btnCoor != 0:
                            if item == 'hd':
                                self.processing = False
                                break

                            elif item == 'sb' or item == 'mj_tg':
                                self.B.LBtn(btnCoor)
                                # self.B.LBtn(((520, 380), (10, 10)))
                                self.complete = True

                            elif item == 'mj_mjxyrw':
                                self.B.LBtn(btnCoor, sleepT=2)
                                continue

                            elif item == 'fl':
                                self.B.RBtn()
                                self.B.RBtn()
                                sleep(0.5)

                            else:
                                self.B.LBtn(btnCoor)

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