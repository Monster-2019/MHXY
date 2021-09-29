from time import sleep
from public.cutScreen import CScreen
from public.matchTem import Match
from public.zudui import Zudui
from public.btn import Btn
from public.glo import Glo
from public.smc import SMC
from public.log import log
import time


class LLSPT:
    def __init__(self):
        super(LLSPT, self).__init__()
        self.g = Glo()
        self.name = self.g.get('name')
        self.B = Btn()
        self.smc = SMC().smc
        self.matchTem = Match().matchTem
        self.cutScreen = CScreen().cutScreen
        self.index = self.g.get('screen')

    def isComplete(self):
        complete = False
        self.B.Hotkey("hd")

        self.smc("rchd", sleepT=0.5)

        self.B.MBtn(590, 330)
        self.B.VBtn(1, 21)
        sleep(0.5)

        for n in range(21):
            if n % 10 == 0:
                sleep(0.5)
                res = self.smc("ecy_wc", simi=0.999, count=0)
                if res != 0:
                    log(f"账号: { self.name } 副本任务已完成")
                    complete = True
                    break
            else:
                self.B.VBtn(-1)

        self.B.VBtn(1, 21)

        self.B.RBtn()

        return complete

    def leader(self):
        log(f"开始副本任务")
        complete = False
        processing = False

        while True:
            res = self.smc('hd', count=0)
            if res == 0:
                self.B.RBtn()
            else:
                break

        complete = self.isComplete()

        if not complete:
            if not self.g.getObj('config', 'TeamStatus'):
                Zudui().start()

        self.B.Hotkey('zz', sleepT=1)
        self.B.LBtn('zr2', sleepT=0.5)
        self.B.LBtn('zr2', sleepT=0.5)
        self.B.RBtn()

        if not complete:
            log(f"副本任务进行中")

            self.B.Hotkey('hd')
            self.smc('rchd', sleepT=0.5)
            page = 1
            while True:
                self.cutScreen()
                temCoor = self.matchTem("hd_ecy_pt")
                if temCoor != 0:
                    btnCoor = self.matchTem("cj", "imgTem/hd_smrw")
                    newCoor = (
                        (
                            temCoor[0][0] + btnCoor[0][0],
                            temCoor[0][1] + btnCoor[0][1],
                        ),
                        btnCoor[1],
                    )
                    if btnCoor != 0:
                        self.B.LBtn(newCoor, sleepT=1)

                        # 去完成或继续任务
                        while not processing:
                            for item in ['fb_xzfb', 'fb_ecy_xz']:
                                r = self.smc(item, sleepT=1)
                                if r != 0 and item == 'fb_ecy_xz':
                                    btnCoor = self.matchTem(
                                        'fb_jr', 'imgTem/fb_ecy_xz')
                                    if btnCoor != 0:
                                        newCoor = (
                                            (
                                                r[0][0] + btnCoor[0][0],
                                                r[0][1] + btnCoor[0][1],
                                            ),
                                            btnCoor[1],
                                        )
                                        self.B.LBtn(newCoor, sleepT=3)

                                        r = self.smc('fb_ecy', simi=0.95, count=0)
                                        if r != 0:
                                            processing = True
                                            break

                        break
                else:
                    page += 1
                    self.B.VBtn(-1, 10)
                    sleep(0.5)
                    if page == 4:
                        break

            fbList = ['sb', 'hd', 'fb_tgjq', 'fb_ecy', 'dh', 'djjx']

            while processing:
                for item in fbList:
                    self.cutScreen()
                    btnCoor = self.matchTem(item)
                    if item == 'fb_ecy' or item == 'dh':
                        btnCoor = self.matchTem(item, simi=0.9)
                    if btnCoor != 0:
                        if item == 'sb':
                            while True:
                                self.smc('sb', sleepT=0.5)
                                self.B.Hotkey('dt', sleepT=1)
                                hc = self.smc('dt_cac', sleepT=2)
                                res = self.smc('hd', count=0)
                                if hc != 0 and res != 0:
                                    break
                            break

                        elif item == 'hd':
                            complete = True
                            processing = False
                            log(f"副本任务完成")
                            break

                        elif item == 'fb_ecy':
                            self.B.LBtn(btnCoor, sleepT=3)

                        elif item == 'dh':
                            while True:
                                self.cutScreen()
                                btnCoor = self.matchTem('dh', simi=0.9)
                                if btnCoor != 0:
                                    newCoor = ((btnCoor[0][0] + 14,
                                                btnCoor[0][1] + 64), (247, 41))
                                    self.B.LBtn(newCoor)
                                    sleep(0.3)
                                else:
                                    break

                        elif item == 'djjx':
                            while True:
                                res = self.smc('djjx', sleepT=0.3)
                                if res == 0:
                                    break

                        else:
                            self.B.LBtn(btnCoor)

        if complete:
            self.g.setObj('config', 'FB_WC', True)
            log(f"副本任务结束")
            return 1
        else:
            self.leader()

    def palyer(self):
        complete = False
        Zudui().start()
        while not self.g.getObj('config', 'FB_WC'):
            sleep(5)

        complete = True

        if complete:
            return 1
        else:
            self.palyer()

    def start(self):
        try:
            complete = False
            res = 0
            if int(self.index) == 0:
                res = self.leader()
            else:
                while self.g.getObj('config', 'FB_WC') == None:
                    sleep(3)

                if not self.g.getObj('config', 'FB_WC'):
                    res = self.palyer()
                else:
                    res = 1

            if res != 0:
                return 1
            else:
                self.start()

        except Exception as e:
            log(e, True)


if __name__ == "__main__":
    LLSPT().start()