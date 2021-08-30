import time
from time import sleep

from cv2 import fastAtan2
from public.cutScreen import CScreen
from public.btn import Btn
from public.matchTem import Match
from public.smc import SMC
from public.glo import Glo
from public.log import log


class Ring:
    def __init__(self, hwnd=False):
        super(Ring, self).__init__()
        self.g = Glo()
        self.name = self.g.get("name")
        self.B = Btn(hwnd)
        self.cutScreen = CScreen(hwnd).cutScreen
        self.matchTem = Match().matchTem
        self.smc = SMC(hwnd).smc

    def isComplete(self):
        complete = False
        self.B.Hotkey("hd")

        self.smc("jjxx", sleepT=0.5)

        self.B.MBtn(590, 330)
        self.B.VBtn(1, 21)
        sleep(0.5)

        for n in range(21):
            if n % 10 == 0:
                sleep(0.5)
                res = self.smc("jyl_wc", simi=0.999, count=0)
                if res != 0:
                    log(f"账号: { self.name } 经验链已完成")
                    complete = True
                    break
            else:
                self.B.VBtn(-1)

        self.B.VBtn(1, 21)

        self.B.RBtn()

        return complete

    def start(self):
        try:
            log(f"账号: { self.name } 开始经验链")
            complete = False
            processing = False

            while True:
                res = self.smc("hd", count=0)
                if res == 0:
                    self.B.RBtn()
                else:
                    self.B.MBtn(900, 300)
                    self.B.VBtn(-1, 20)
                    sleep(0.5)

                    r = self.smc("rw_jyl", simi=0.94, count=0)
                    if r != 0:
                        print(f"账号: { self.name } 已领取经验链")
                        processing = True
                    sleep(0.5)
                    break

            if not processing:
                complete = self.isComplete()

            if not complete:
                print(f"账号: { self.name } 经验链进行中")

                if not processing:
                    self.B.Hotkey("hd")
                    self.smc("jjxx", sleepT=0.5)
                    page = 1
                    while True:
                        self.cutScreen()
                        temCoor = self.matchTem("hd_jyl")
                        if temCoor != 0:
                            btnCoor = self.matchTem("cj", "imgTem/hd_jyl")
                            newCoor = (
                                (
                                    temCoor[0][0] + btnCoor[0][0],
                                    temCoor[0][1] + btnCoor[0][1],
                                ),
                                btnCoor[1],
                            )
                            if btnCoor != 0:
                                self.B.LBtn(newCoor)
                                sleep(5)

                                getList = ["dh_jyl", "dh_lqjyl", "qd_1"]

                                for item in getList:
                                    while True:
                                        r = self.smc(item, sleepT=0.5)
                                        if r != 0:
                                            break

                                processing = True
                                break

                        else:
                            page += 1
                            self.B.MBtn(590, 330)
                            self.B.VBtn(-1, 10)
                            sleep(0.5)
                            if page == 4:
                                break

                xhList = ["rw_jyl_wc", "rw_jyl", "gm", "gm_1", 'btgm', "dh", "sj"]

                while not complete or processing:
                    for item in xhList:
                        self.cutScreen()
                        btnCoor = self.matchTem(item)
                        if item == 'dh' or item == 'rw_jyl':
                            btnCoor = self.matchTem(item, simi=0.94)
                        if btnCoor != 0:
                            if item == 'rw_jyl_wc':
                                complete = True
                                processing = False
                                break

                            elif item == "dh":
                                while True:
                                    self.cutScreen()
                                    btnCoor = self.matchTem("dh", simi=0.94)
                                    if btnCoor != 0:
                                        newCoor = (
                                            (btnCoor[0][0] + 14, btnCoor[0][1] + 64),
                                            (87, 22),
                                        )
                                        self.B.LBtn(newCoor)
                                        sleep(0.3)
                                    else:
                                        break

                            elif item == "gm_1" or item == "btgm":
                                self.B.LBtn(btnCoor)
                                res = self.smc("gm_sb", count=0)
                                if res == 0:
                                    newCoor = ((308, 245), (294, 75))
                                    self.B.LBtn(newCoor)

                            else:
                                self.B.LBtn(btnCoor)

                            sleep(1)
                    
                        else:
                            if item == "rw_jyl" and self.smc('hd', count=0):
                                if self.g.compare():
                                    self.B.RBtn()
                                    self.B.MBtn(900, 300)
                                    self.B.VBtn(-1, 20)

                        sleep(0.5)

            if complete:
                log(f"账号: { self.name } 经验链结束")
                return 1
            else:
                self.start()

        except Exception as e:
            log(e, True)


if __name__ == "__main__":
    Ring().start()
