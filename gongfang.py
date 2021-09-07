from public.cutScreen import CScreen
from public.btn import Btn
from public.matchTem import Match
from public.smc import SMC
from public.glo import Glo
from public.log import log
from time import sleep


class Gongfang:
    def __init__(self, hwnd=False):
        super(Gongfang, self).__init__()
        self.g = Glo()
        self.name = self.g.get("name")
        self.B = Btn(hwnd)
        self.cutScreen = CScreen(hwnd).cutScreen
        self.matchTem = Match().matchTem
        self.smc = SMC(hwnd).smc
        self.complete = False
        self.processing = False

    def kaogu(self):
        isStart = False
        self.B.Hotkey("bb", sleepT=1)

        self.B.MBtn(707, 406)
        self.B.VBtn(1, 30)

        page = 0
        # cz = 'bb_fjc'
        cz = "bb_lyc"
        while True:
            r = self.smc(cz)
            if r != 0:
                self.B.LBtn(r)
                self.B.LBtn(r)
                isStart = True
                sleep(1)
                break

            else:
                page += 1
                self.B.MBtn(707, 406)
                self.B.VBtn(-1, 13)
                sleep(0.5)
                if page == 6:
                    self.B.RBtn()
                    return isStart

        while True:
            r = self.smc("kg_ks", sleepT=1)
            if r != 0:
                self.B.RBtn()
                self.B.RBtn()
                break

        for i in range(10):
            while True:
                self.cutScreen()
                btnCoor = self.matchTem("wj")
                if btnCoor != 0:
                    if btnCoor[0][0] + btnCoor[1][0] < 920:
                        self.B.LBtn(btnCoor, sleepT=3)
                        break

        return isStart

    def sell(self):
        self.B.Hotkey("dt", sleepT=2)

        xhList = ["dt_lyc", "zb_lyc", "lyc_zhsr", "kg_gdsm"]

        isSell = False
        while not isSell:
            for item in xhList:
                r = 0
                while True:
                    r = self.smc(item)
                    print(item, r)
                    if r != 0:
                        if item == "lyc_zhsr":
                            sleep(15)
                        break

                if r != 0 and item == "kg_gdsm":
                    isSell = True
                    break

        xhList = ["kg_zp", "kg_sm", "kg_smwc"]

        sell_status = False
        while not sell_status:
            for item in xhList:
                r = self.smc(item)
                if r != 0 and (item == "kg_zp" or item == "kg_smwc"):
                    sell_status = True
                    self.B.RBtn()
                    self.B.RBtn()
                    break

        return 1

    def isComplete(self):
        while True:
            res = self.smc("hd", count=0)
            if res == 0:
                self.B.RBtn()
            else:
                self.B.MBtn(900, 300)
                self.B.VBtn(-1, 20)
                sleep(0.5)

                r = self.smc('gf_kg', simi=0.92, count=0) or self.smc('gf_gf', simi=0.92, count=0)
                if r != 0:
                    if r[0][0] + r[1][0] > 780:
                        log(f"账号: { self.name } 已领取工坊任务")
                        self.processing = True
                sleep(0.5)
                break

        if self.processing:
            return False

        self.B.Hotkey("hd")

        self.smc("jjxx", sleepT=0.5)

        self.B.MBtn(590, 330)
        self.B.VBtn(1, 21)
        sleep(0.5)

        for n in range(21):
            if n % 10 == 0:
                sleep(0.5)
                res = self.smc("gf_wc", simi=0.999, count=0)
                if res != 0:
                    log(f"账号: { self.name } 工坊任务已完成")
                    self.complete = True
                    break
            else:
                self.B.VBtn(-1)

        self.B.VBtn(1, 21)

        self.B.RBtn()

    def start(self):
        self.sell()

        return 0
        log(f"账号: { self.name } 开始工坊任务")

        self.isComplete()

        if self.processing or not self.complete:
            print(f"账号: { self.name } 工坊任务进行中")

            if not self.processing:
                self.B.Hotkey("hd")
                self.smc("jjxx", sleepT=0.5)
                page = 1
                while not self.processing:
                    self.cutScreen()
                    temCoor = self.matchTem("hd_gfrw", simi=0.998)
                    if temCoor != 0:
                        btnCoor = self.matchTem("cj", "imgTem/hd_gfrw")
                        newCoor = (
                            (
                                temCoor[0][0] + btnCoor[0][0],
                                temCoor[0][1] + btnCoor[0][1],
                            ),
                            btnCoor[1],
                        )
                        if btnCoor != 0:
                            self.B.LBtn(newCoor)
                            self.processing = True

                            while True:
                                r = self.smc("gf_lqrw")
                                sleep(1)
                                if r != 0:
                                    break

                            break

                    else:
                        page += 1
                        self.B.MBtn(590, 330)
                        self.B.VBtn(-1, 10)
                        sleep(0.5)
                        if page == 4:
                            break

            xhList = [
                "gf_kg",
                "gf_xz",
                "dh",
                "dhda",
                "gfnot",
                "gfgm",
                "djjx",
                "sy",
                "sj",
            ]

            while not self.complete or self.processing:
                for item in xhList:
                    self.cutScreen()
                    btnCoor = self.matchTem(item)
                    isHd = self.matchTem('hd')
                    if item == 'gf_kg' or item == 'dh':
                        btnCoor = self.matchTem(item, simi=0.9)
                    if btnCoor != 0:
                        if item == 'gf_kg':
                            if btnCoor[0][0] > 780:
                                self.B.LBtn(btnCoor)
                            else:
                                self.B.RBtn()
                                self.B.MBtn(157, 686)
                                self.B.VBtn(-1, 10)

                        elif item == "dh" or item == "dhda":
                            while True:
                                self.cutScreen()
                                btnCoor = self.matchTem("dh", simi=0.9) or self.matchTem("dhda", simi=0.9)
                                if btnCoor != 0:
                                    newCoor = (
                                        (btnCoor[0][0] + 14, btnCoor[0][1] + 64),
                                        (247, 41),
                                    )
                                    self.B.LBtn(newCoor)
                                    sleep(0.3)
                                else:
                                    break

                        elif item == "djjx":
                            while True:
                                res = self.smc("djjx", sleepT=0.3)
                                if res == 0:
                                    break

                        elif item == "gfgm":
                            sleep(0.5)
                            self.B.LBtn(btnCoor)
                            res = self.smc("gm_sb", count=0)
                            if res == 0:
                                newCoor = ((308, 245), (294, 75))
                                self.B.LBtn(newCoor)

                        elif item == "sy":
                            if (btnCoor[0][0] + btnCoor[1][0]) < 920:
                                self.B.LBtn(btnCoor)

                        elif item == "gfnot":
                            self.B.RBtn()
                            self.complete = True
                            self.processing = False
                            break

                        else:
                            self.B.LBtn(btnCoor)

                    else:
                        if item == "gf_kg" and isHd:
                            self.B.RBtn()
                            self.B.MBtn(900, 300)
                            self.B.VBtn(-1, 20)

                            res = self.smc('gf_kg', simi=0.9) or self.smc('gf_gf', simi=0.9)
                            if res == 0:
                                sleep(2)
                                compare = False
                                for i in range(5):
                                    self.cutScreen()
                                    compare = self.g.compare()
                                    if compare:
                                        break
                                    sleep(0.5)

                                if compare:
                                    self.processing = False
                                    self.isComplete()

        res = self.kaogu()
        if res:
            self.sell()

        if self.complete:
            print(f"账号: { self.name } 工坊任务结束")
            return 1
        else:
            self.start()


if __name__ == "__main__":
    Gongfang().start()
