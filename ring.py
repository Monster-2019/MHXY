import time
from time import sleep

from cv2 import compare, fastAtan2
from cutScreen import CScreen
from btn import Btn
from match import Match
from smc import SMC
from glo import Glo
from log import log


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
        self.btn.hotkey("hd")

        self.smc("rchd", sleep_time=0.5)

        self.B.MBtn(590, 330)
        self.B.v(1, 31)
        sleep(0.5)

        for n in range(31):
            if n % 10 == 0:
                sleep(0.5)
                res = self.smc("jyl_wc", simi=0.999, count=0)
                if res != 0:
                    log(f"账号: { self.name } 经验链已完成")
                    complete = True
                    break
            else:
                self.B.v(-1)

        self.B.v(1, 31)

        self.btn.r()

        return complete

    def start(self):
        try:
            log(f"账号: { self.name } 开始经验链")
            complete = False
            processing = False

            while True:
                res = self.smc("hd", count=0)
                if res == 0:
                    self.btn.r()
                else:
                    self.B.MBtn(900, 300)
                    self.B.v(-1, 20)
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

                self.btn.hotkey('zz', sleep_time=1)
                self.btn.l('zr1', sleep_time=0.5)
                self.btn.l('zr1', sleep_time=0.5)
                self.btn.r()

                if not processing:
                    self.btn.hotkey("hd")
                    self.smc("rchd", sleep_time=0.5)
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
                                self.btn.l(newCoor)
                                sleep(5)

                                getList = ["dh_jyl", "dh_lqjyl", "qd_1"]

                                for item in getList:
                                    while True:
                                        r = self.smc(item, sleep_time=0.5)
                                        if r != 0:
                                            break

                                processing = True
                                break

                        else:
                            page += 1
                            self.B.MBtn(590, 330)
                            self.B.v(-1, 10)
                            sleep(0.5)
                            if page == 4:
                                break

                xhList = [
                    "rw_jyl_wc", "rw_jyl", "gm", "gm_1", 'btgm', "dh", "sj"
                ]

                count = 0
                loopCount = 0
                CS = False

                while not complete or processing:
                    for item in xhList:
                        self.cutScreen()
                        btnCoor = self.matchTem(item)
                        isHd = self.matchTem('hd')
                        if item == 'dh' or item == 'rw_jyl':
                            btnCoor = self.matchTem(item, simi=0.9)
                        if btnCoor != 0:
                            loopCount = 0
                            if item == 'rw_jyl_wc':
                                complete = True
                                processing = False
                                break

                            elif item == "dh":
                                while True:
                                    self.cutScreen()
                                    btnCoor = self.matchTem("dh", simi=0.9)
                                    if btnCoor != 0:
                                        newCoor = (
                                            (btnCoor[0][0] + 14,
                                             btnCoor[0][1] + 64),
                                            (87, 22),
                                        )
                                        self.btn.l(newCoor)
                                        sleep(0.3)
                                    else:
                                        break

                            elif item == "btgm":
                                sleep(2)
                                res = self.smc('bt_sj') or self.smc('bt_jlh') or self.smc('bt_mgh')
                                if res and not CS:
                                    CS = True
                                    self.btn.r()
                                    self.btn.r()

                                    self.btn.hotkey('gj')

                                    while True:
                                        self.B.DBtn((900, 350), (130, 350))
                                        sleep(1)
                                        res = self.smc('gj_xysm')
                                        if res:
                                            break

                                    start = int(time.time())
                                    end = int(time.time())
                                    while end - start < 1200:
                                        end = int(time.time())
                                        res = self.smc('sj')
                                        if res:
                                            CS = False
                                            break
                                        sleep(1)

                                    self.btn.l(((500, 450), (2, 2)))
                                    
                                else:
                                    self.btn.l(btnCoor)
                                    CS = False
                                    res = self.smc("gm_sb", count=0)
                                    if res:
                                        newCoor = ((308, 245), (294, 75))
                                        CS = True
                                        self.btn.l(newCoor)
                                        continue
                                    sleep(0.5)
                                    self.btn.r()

                            elif item == "gm_1":
                                sleep(2)
                                self.btn.l(btnCoor)
                                res = self.smc("gm_sb", count=0)
                                if res:
                                    newCoor = ((308, 245), (294, 75))
                                    self.btn.l(newCoor)
                                    continue
                                sleep(0.5)
                                self.btn.r()

                            else:
                                self.btn.l(btnCoor)

                        else:
                            if item == 'rw_jyl' and isHd:
                                if count == 3:
                                    complete = True
                                    processing = False

                                compare = False
                                for i in range(3):
                                    self.cutScreen()
                                    compare = self.g.compare()
                                    if compare:
                                        break
                                    sleep(0.5)

                                if compare:
                                    print('站立不动')
                                    self.btn.r()
                                    self.btn.r()
                                    sleep(0.5)
                                    self.B.MBtn(900, 300)
                                    self.B.v(-1, 20)
                                    res = self.smc('rw_jyl', simi=0.9)
                                    if res == 0:
                                        count += 1
                                    else:
                                        count = 0

                    loopCount += 1
                    if loopCount == 3:
                        self.btn.r()
                        loopCount = 0

            if complete:
                log(f"账号: { self.name } 经验链结束")
                return 1
            else:
                self.start()

        except Exception as e:
            log(e, True)


if __name__ == "__main__":
    Ring().start()
