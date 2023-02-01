from time import sleep
from cutScreen import CScreen
from btn import Btn
from match import Match
from smc import SMC
from glo import Glo
from log import log


class Bangpai:
    def __init__(self):
        super(Bangpai, self).__init__()
        self.g = Glo()
        self.name = self.g.get("name")
        self.B = Btn()
        self.cutScreen = CScreen().cutScreen
        self.matchTem = Match().matchTem
        self.smc = SMC().smc
        self.smca = SMC().smca

    def changeTask(self):
        processList = ["rw_dqrw", "rw_cgrw", "rw_bprw", "rw_fqrw", "qd"]
        fq = False
        while not fq:
            self.B.Hotkey("rw")
            for item in processList:
                self.cutScreen()
                btnCoor = self.matchTem(item, simi=0.98)
                if btnCoor != 0:
                    if item == "qd":
                        self.B.LBtn(btnCoor)
                        fq = True
                    else:
                        self.B.LBtn(btnCoor)

                    sleep(0.5)

        self.B.RBtn()
        sleep(0.5)

        self.B.Hotkey("hd")

        self.smc('rchd', sleepT=0.5)

        self.B.MBtn(590, 330)
        self.B.VBtn(1, 31)

        # 匹配帮派任务
        page = 1
        while True:
            self.cutScreen()
            temCoor = self.matchTem("hd_bprw")
            if temCoor != 0:
                btnCoor = self.matchTem("cj", "imgTem/hd_bprw")
                newCoor = (
                    (temCoor[0][0] + btnCoor[0][0], temCoor[0][1] + btnCoor[0][1]),
                    btnCoor[1],
                )
                if btnCoor != 0:
                    self.B.LBtn(newCoor)
                    sleep(1)

                    while True:
                        res = self.smc("bp_lqrw")
                        if res:
                            processing = True
                            break
                        else:
                            if self.smc("hd_bprw", count=0):
                                self.B.LBtn(newCoor)

                    break

            else:
                page += 1
                self.B.VBtn(-1, 10)
                sleep(0.5)
                if page == 4:
                    self.B.RBtn()
                    return True
                    break

        return False

    def exchangeXsl(self):
        while True:
            res = self.smc("hd", count=0)
            if res == 0:
                self.B.RBtn()
            else:
                break

        self.B.Hotkey("hd")
        self.smc("jjxx", sleepT=0.5)
        page = 1
        while True:
            self.cutScreen()
            temCoor = self.matchTem("hd_my")
            if temCoor != 0:
                btnCoor = self.matchTem("cj", "imgTem/hd_my")
                newCoor = (
                    (temCoor[0][0] + btnCoor[0][0], temCoor[0][1] + btnCoor[0][1]),
                    btnCoor[1],
                )
                if btnCoor != 0:
                    self.B.LBtn(newCoor)
                    sleep(1)

                    temList = ["dh_bpmy", "my_xsl_add", "my_xsl_dh"]

                    status = False
                    while not status:
                        for item in temList:
                            self.cutScreen()
                            btnCoor = self.matchTem(item)
                            if btnCoor != 0:
                                if item == "my_xsl_dh":
                                    while True:
                                        self.B.LBtn(btnCoor)
                                        res = self.smca(
                                            ["my_xsl_no", "my_xsl_ten", "my_xsl_max"]
                                        )
                                        if res != 0:
                                            status = True
                                            self.B.RBtn()
                                            break
                                    break
                                else:
                                    self.B.LBtn(btnCoor)

                    break

            else:
                page += 1
                self.B.MBtn(590, 330)
                self.B.VBtn(-1, 10)
                sleep(0.5)
                if page == 4:
                    break

        self.B.RBtn()

        return 1

    def isComplete(self):
        complete = False
        self.B.Hotkey("hd")

        self.smc("rchd", sleepT=0.5)

        self.B.MBtn(590, 330)
        self.B.VBtn(1, 31)
        sleep(0.5)

        for n in range(31):
            if n % 10 == 0:
                sleep(0.5)
                res = self.smc("bp_wc", count=0)
                if res != 0:
                    log(f"账号: { self.name } 帮派任务已完成")
                    complete = True
                    break
            else:
                self.B.VBtn(-1)

        self.B.VBtn(1, 31)

        self.B.RBtn()

        return complete

    def start(self):
        log(f"账号: { self.name } 开始帮派任务")
        complete = False
        processing = False

        while True:
            res = self.smc("hd", count=0)
            if res == 0:
                self.B.RBtn()
            else:
                self.B.MBtn(900, 300)
                self.B.VBtn(1, 10)
                sleep(0.5)

                temCoor = self.matchTem("bp_ql", simi=0.95)
                if temCoor != 0:
                    print(f"账号: { self.name } 已领取帮派任务")
                    processing = True
                sleep(0.5)
                break

        if not processing:
            complete = self.isComplete()

        if not complete:
            print(f"账号: { self.name } 帮派任务进行中")

            if not processing:
                self.B.Hotkey("hd")
                self.smc("rchd", sleepT=0.5)
                page = 1
                while True:
                    self.cutScreen()
                    temCoor = self.matchTem("hd_bprw")
                    if temCoor != 0:
                        btnCoor = self.matchTem("cj", "imgTem/hd_bprw")
                        newCoor = (
                            (
                                temCoor[0][0] + btnCoor[0][0],
                                temCoor[0][1] + btnCoor[0][1],
                            ),
                            btnCoor[1],
                        )
                        if btnCoor != 0:
                            self.B.LBtn(newCoor)
                            sleep(1)

                            while True:
                                res = self.smc("bp_lqrw")
                                if res:
                                    processing = True
                                    break

                            break

                    else:
                        page += 1
                        self.B.VBtn(-1, 10)
                        sleep(0.5)
                        if page == 4:
                            break

            bpList = ["bp_ql", "gm", "gm_shanghui", "dh_bprw", "bp_bpwc"]

            while processing:
                for item in bpList:
                    self.cutScreen()
                    btnCoor = self.matchTem(item)
                    if item == "bp_ql":
                        btnCoor = self.matchTem(item, simi=0.95)
                    if btnCoor != 0:
                        if item == "gm_shanghui":
                            print("购买宝石")
                            sleep(2)
                            self.B.LBtn(btnCoor, sleepT=0.5)
                            res = self.smc(item, count=0)
                            if res != 0:
                                self.B.RBtn()

                        elif item == "dh_bprw":
                            # newCoor = ((btnCoor[0][0] + 14, btnCoor[0][1] + 64), (247, 41))
                            self.B.LBtn(btnCoor)
                        elif item == "bp_bpwc":
                            complete = True
                            processing = False
                            break
                        else:
                            self.B.LBtn(btnCoor)

                        sleep(0.5)

                    else:
                        if item == "bp_ql":
                            res = self.smc("hd", count=0, sleepT=1)
                            if res != 0:
                                self.B.MBtn(900, 300)
                                self.B.VBtn(1, 10)

                                self.cutScreen()
                                compareResult = self.g.compare()
                                if compareResult:
                                    res = self.smc("bp_ql")
                                    if res == 0:
                                        complete = self.changeTask()
                                        if complete:
                                            processing = False

            sleep(2)
            self.exchangeXsl()

        if complete:
            log(f"账号: { self.name } 帮派任务结束")
            return 1
        else:
            self.start()


if __name__ == "__main__":
    Bangpai().start()
