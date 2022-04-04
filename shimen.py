from time import sleep
from public.cutScreen import CScreen
from public.btn import Btn
from public.matchTem import Match
from public.smc import SMC
from public.glo import Glo
from public.log import log
from sendMsg import SendMsg
import threading
import sys


class Shimen:
    def __init__(self):
        super(Shimen, self).__init__()
        self.g = Glo()
        self.name = Glo().get("name")
        self.B = Btn()
        self.cutScreen = CScreen().cutScreen
        self.matchTem = Match().matchTem
        self.smc = SMC().smc
        self.smca = SMC().smca
        self.complete = False

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
                res = self.smc("sm_wc", simi=0.999, count=0)
                if res != 0:
                    log(f"账号: { self.name } 师门任务已完成")
                    complete = True
                    break
            else:
                self.B.VBtn(-1)

        self.B.VBtn(1, 21)

        self.B.RBtn()

        return complete

    def timing(self):
        self.complete = True

    def start(self):
        try:
            t = threading.Timer(600, self.timing)
            t.start()
            log(f"账号: { self.name } 开始师门任务")
            processing = False

            while self.smc("hd", count=0) == 0:
                self.B.RBtn()

            self.B.Hotkey("zz", sleepT=1)
            self.B.LBtn("zr1", sleepT=0.5)
            self.B.LBtn("zr1", sleepT=0.5)
            self.B.RBtn()

            while True:
                res = self.smc("sygb", sleepT=0.5)
                if res == 0:
                    break

            self.complete = self.isComplete()

            if not self.complete:
                print(f"账号: { self.name } 师门任务未完成")

                if not processing:
                    self.B.Hotkey("hd")
                    self.smc("rchd", sleepT=0.5)
                    page = 1
                    while True:
                        self.cutScreen()
                        temCoor = self.matchTem("hd_smrw") or self.matchTem("hd_smrw1")
                        if temCoor != 0:
                            btnCoor = self.matchTem(
                                "cj", "imgTem/hd_smrw"
                            ) or self.matchTem("cj", "imgTem/hd_smrw1")
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
                                while True:
                                    self.cutScreen()
                                    btnCoor = self.matchTem("sm_qwc") or self.matchTem(
                                        "sm_jxrw"
                                    )
                                    if btnCoor != 0:
                                        self.B.LBtn(btnCoor, sleepT=1)
                                        processing = True
                                        break

                                break
                        else:
                            page += 1
                            self.B.VBtn(-1, 10)
                            sleep(0.5)
                            if page == 4:
                                break

                smList = [
                    "sm_mpgx",
                    "hd",
                    "sm_sm",
                    "djjx",
                    "dh",
                    "dhda",
                    "gm",
                    "btgm",
                    "gfgm",
                    "sj",
                    "sy",
                    "sm_hdwp",
                    "sm_rwdh",
                    # "jm_gb",
                ]

                count = 0
                while processing:
                    for item in smList:
                        self.cutScreen()
                        if item == "dh" or item == "sm_sm":
                            btnCoor = self.matchTem(item, simi=0.94)
                        else:
                            btnCoor = self.matchTem(item)
                        if btnCoor != 0:
                            if item == "hd":
                                if self.g.compare() == True:
                                    self.B.RBtn()
                                    continue

                            elif item == "dh" or item == "dhda":
                                while True:
                                    self.cutScreen()
                                    btnCoor = self.matchTem(
                                        "dh", simi=0.94
                                    ) or self.matchTem("dhda", simi=0.94)
                                    if btnCoor != 0:
                                        newCoor = (
                                            (btnCoor[0][0], btnCoor[0][1] + 69),
                                            (87, 22),
                                        )
                                        self.B.LBtn(newCoor)
                                        sleep(0.3)
                                    else:
                                        break

                            elif item == "djjx":
                                while True:
                                    res = self.smc("djjx", simi=0.9, sleepT=0.5)
                                    if res == 0:
                                        break
                                
                                sleep(5)

                            elif item == "btgm" or item == "gfgm":
                                sleep(2)
                                newCoor = ((308, 245), (294, 75))
                                self.B.LBtn(newCoor, sleepT=0.5)
                                self.B.LBtn(btnCoor, sleepT=0.5)
                                self.B.RBtn()

                            elif item == "sy":
                                if (btnCoor[0][0] + btnCoor[1][0]) < 920:
                                    self.B.LBtn(btnCoor)

                            elif item == "sm_mpgx":
                                self.smc("sm_jl")
                                self.B.RBtn()
                                print(f"账号: { self.name } 师门任务完成")
                                processing = False
                                self.complete = True
                                break

                            else:
                                self.B.LBtn(btnCoor)

                            count = 0

                            sleep(0.5)

                        else:
                            if item == "sm_sm":
                                if self.smc("hd", count=0) != 0:
                                    self.B.RBtn()
                                    self.B.MBtn(900, 300)
                                    self.B.VBtn(1, 10)
                                    count += 1

                            if count == 5:
                                print(f"账号: { self.name } 师门任务完成1")
                                processing = False
                                self.complete = True
                                break

                sleep(0.5)
                while True:
                    self.cutScreen()
                    temCoor = self.matchTem("hd")
                    btnCoor = self.matchTem("sy")
                    if temCoor != 0 and btnCoor != 0:
                        self.B.LBtn(btnCoor, sleepT=0.5)
                    elif temCoor == 0 and btnCoor == 0:
                        self.B.RBtn()
                    else:
                        break
                    sleep(0.5)

            if self.complete:
                log(f"账号: { self.name } 师门任务结束")
                t.cancel()
                return 1
            else:
                self.start()

        except Exception as e:
            log(e, True)
            sys.exit(0)


if __name__ == "__main__":
    Shimen().start()
