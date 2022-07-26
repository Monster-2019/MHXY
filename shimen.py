from time import sleep
from public.cutScreen import CScreen
from public.btn import Btn
from public.matchTem import Match
from public.smc import SMC
from public.glo import Glo
from public.log import log
from sendMsg import SendMsg
import threading


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
        self.processing = False

    def timing(self):
        self.complete = True
        self.processing = False

    def start(self):
        try:
            t = threading.Timer(900, self.timing)
            t.start()
            log(f"账号: { self.name } 开始师门任务")

            while self.smc("hd", count=0) == 0:
                self.B.RBtn()

            while True:
                res = self.smc("sygb", sleepT=0.5)
                if res == 0:
                    break

            self.B.Hotkey("hd")

            self.smc("rchd", sleepT=0.5)

            self.B.MBtn(590, 330)
            self.B.VBtn(1, 31)
            sleep(0.5)

            for n in range(31):
                if n % 10 == 0:
                    sleep(0.5)
                    if self.smc("sm_wc", simi=0.999, count=0) != 0:
                        log(f"账号: { self.name } 师门任务已完成")
                        self.complete = True
                        self.B.RBtn()
                        break

                    else:
                        self.cutScreen()
                        temCoor = self.matchTem("hd_smrw", simi=0.999) or self.matchTem("hd_smrw1", simi=0.999)
                        if temCoor:
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
                            if btnCoor:
                                self.B.LBtn(newCoor, sleepT=1)

                                # 去完成或继续任务
                                while True:
                                    self.cutScreen()
                                    btnCoor = self.matchTem("sm_qwc") or self.matchTem(
                                        "sm_jxrw"
                                    )
                                    if btnCoor != 0:
                                        self.B.LBtn(btnCoor, sleepT=1)
                                        self.processing = True
                                        break

                                break
                else:
                    self.B.VBtn(-1)

            self.B.RBtn()

            if not self.complete:
                print(f"账号: { self.name } 师门任务未完成")

                smList = [
                    "sm_mpgx",
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
                while self.processing:
                    for item in smList:
                        self.cutScreen()
                        isHd = self.smc('hd', count=0)
                        compare = self.g.compare()
                        if item == "dh" or item == "sm_sm":
                            btnCoor = self.matchTem(item, simi=0.94)
                        else:
                            btnCoor = self.matchTem(item)
                        if btnCoor:
                            if item == "dh" or item == "dhda":
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
                                    res = self.smc("djjx", simi=0.9, sleepT=0.1)
                                    if res == 0:
                                        break
                                
                                sleep(3)

                            elif item == "btgm" or item == "gfgm":
                                sleep(3)
                                newCoor = ((308, 245), (294, 75))
                                self.B.LBtn(newCoor, sleepT=0.5)
                                self.B.LBtn(btnCoor, sleepT=1)
                                if self.smca(['btgm', 'gfgm']):
                                    self.B.RBtn()

                            elif item == "sy":
                                if (btnCoor[0][0] + btnCoor[1][0]) < 920:
                                    self.B.LBtn(btnCoor)

                            elif item == "sm_mpgx":
                                self.smc("sm_jl")
                                self.B.RBtn()
                                print(f"账号: { self.name } 师门任务完成")
                                self.processing = False
                                self.complete = True
                                break

                            elif item == 'sm_sm' and isHd:
                                self.B.LBtn(btnCoor)

                            else:
                                self.B.LBtn(btnCoor)

                            count = 0

                            sleep(0.5)

                        elif isHd:
                            if item == "sm_sm":
                                if self.smc("hd", count=0) != 0:
                                    self.B.RBtn()
                                    self.B.MBtn(900, 300)
                                    self.B.VBtn(1, 10)
                                    count += 1

                            if count == 5:
                                print(f"账号: { self.name } 师门任务完成1")
                                self.processing = False
                                self.complete = True
                                break

                        sleep(0.1)

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


if __name__ == "__main__":
    Shimen().start()
