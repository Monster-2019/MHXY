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
                res = self.smc("sm_wc", simi=0.97, count=0)
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

            while True:
                res = self.smc("hd", simi=0.9, count=0)
                if res == 0:
                    self.B.RBtn()
                else:
                    self.B.Hotkey("zz")
                    self.B.LBtn("zr1")
                    sleep(0.5)
                    self.B.RBtn()
                    sleep(0.5)
                    break

            while True:
                res = self.smc("sygb", sleepT=0.5)
                if res == 0:
                    break

            # self.complete = self.isComplete()

            if not self.complete:
                print(f"账号: { self.name } 师门任务未完成")

                if not processing:
                    self.B.Hotkey("hd")
                    self.smc("rchd", sleepT=0.5)
                    page = 1
                    while True:
                        self.cutScreen()
                        temCoor = self.matchTem("hd_smrw") or self.matchTem(
                            "hd_smrw1")
                        if temCoor != 0:
                            btnCoor = self.matchTem(
                                "cj", "imgTem/hd_smrw") or self.matchTem(
                                    "cj", "imgTem/hd_smrw1")
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
                                    btnCoor = self.matchTem(
                                        "sm_qwc", simi=0.95) or self.matchTem(
                                            "sm_jxrw", simi=0.95)
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

                # smList = [
                #     "sm_mpgx",
                #     "hd",
                #     "sm_sm",
                #     "djjx",
                #     "dh",
                #     "dhda",
                #     "gm",
                #     "btgm",
                #     "gfgm",
                #     "sj",
                #     "sy",
                #     "sm_hdwp",
                #     "sm_rwdh",
                #     "jm_gb",
                # ]
                smList = [{
                    'tem': 'sm_mpgx',
                    'simi': 0.9
                }, {
                    'tem': 'hd',
                    'simi': 0
                }, {
                    'tem': 'sm_sm',
                    'simi': 0.8
                }, {
                    'tem': 'djjx',
                    'simi': 0.9
                }, {
                    'tem': 'dh',
                    'simi': 0.8
                }, {
                    'tem': 'dhda',
                    'simi': 0.8
                }, {
                    'tem': 'gm',
                    'simi': 0
                }, {
                    'tem': 'btgm',
                    'simi': 0.9
                }, {
                    'tem': 'gfgm',
                    'simi': 0
                }, {
                    'tem': 'sj',
                    'simi': 0.94
                }, {
                    'tem': 'sy',
                    'simi': 0
                }, {
                    'tem': 'sm_hdwp',
                    'simi': 0
                }, {
                    'tem': 'sm_rwdh',
                    'simi': 0
                }, {
                    'tem': 'jm_gb',
                    'simi': 0
                }]

                cleanBB = False
                while processing:
                    for item in smList:
                        self.cutScreen()
                        btnCoor = self.matchTem(item['tem'], simi=item['simi'])
                        tem = item['tem']
                        if btnCoor != 0:
                            if tem == "hd":
                                if self.g.compare() == True:
                                    self.B.RBtn()

                            elif tem == "dh" or tem == "dhda":
                                while True:
                                    self.cutScreen()
                                    btnCoor = self.matchTem(
                                        "dh", simi=0.84) or self.matchTem("dhda", simi=0.84)
                                    if btnCoor != 0:
                                        newCoor = (
                                            (btnCoor[0][0],
                                             btnCoor[0][1] + 69),
                                            (87, 22),
                                        )
                                        self.B.LBtn(newCoor)
                                        sleep(0.3)
                                    else:
                                        break

                            elif tem == "djjx":
                                while True:
                                    res = self.smc("djjx", simi=0.9, sleepT=0.3)
                                    if res == 0:
                                        break

                            elif tem == "btgm" or tem == "gfgm":
                                newCoor = ((308, 245), (294, 75))
                                self.B.LBtn(newCoor)
                                self.B.LBtn(btnCoor)

                            elif tem == "sy":
                                if (btnCoor[0][0] + btnCoor[1][0]) < 920:
                                    self.B.LBtn(btnCoor)

                            elif tem == "sm_mpgx":
                                self.B.RBtn()
                                print(f"账号: { self.name } 师门任务完成")
                                processing = False
                                self.complete = True
                                break

                            else:
                                self.B.LBtn(btnCoor)

                            sleep(1)

                        else:
                            if tem == "sm_sm":
                                if self.smc("hd", simi=0.9, count=0) != 0:
                                    self.B.RBtn()
                                    self.B.MBtn(900, 300)
                                    self.B.VBtn(1, 10)

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
