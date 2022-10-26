from time import sleep
from cutScreen import CScreen
from btn import Btn
from matchTem import Match
from smc import SMC
from glo import Glo


class Upgrade:
    def __init__(self):
        self.name = Glo().get("name")
        self.B = Btn()
        self.cutScreen = CScreen().cutScreen
        self.matchTem = Match().matchTem
        self.smc = SMC().smc
        self.smca = SMC().smca
        self.complete = False
        self.processing = False

    def nextTask(self):
        self.B.Hotkey("rw")
        xhList = ["rw_dqrw", "rw_zxrw"]
        for item in xhList:
            r = self.smc(item)
            if r and item == "rw_zxrw":
                if self.smc("rw_notask"):
                    self.complete = True
                    break
                else:
                    if self.smc("rw_mscs"):
                        break

        return self.complete

    def start(self):
        try:
            print(f"账号: { self.name } 开始任务")

            while self.smc("hd", count=0) == 0:
                self.B.RBtn()

            self.nextTask()

            xhList = ["dh", "djjx", "djtg"]

            while not self.complete:
                for item in xhList:
                    self.cutScreen()
                    isHd = self.smc("hd", count=0)
                    compare = self.g.compare()
                    if item == "dh":
                        btnCoor = self.matchTem(item, simi=0.94)
                    else:
                        btnCoor = self.matchTem(item)

                    if isHd and btnCoor:
                        if item == "dh":
                            while True:
                                self.cutScreen()
                                btnCoor = self.matchTem("dh", simi=0.94)
                                if btnCoor:
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
                            
                            sleep(1)

                        else:
                            self.B.LBtn(btnCoor)
                    
                    elif isHd and compare:
                        res = False
                        for i in range(10):
                            sleep(1)
                            self.cutScreen()
                            res = self.g.compare()

                        if res:
                            self.nextTask()

            if self.complete:
                print(f"账号: { self.name } 任务结束")
                return 1
            else:
                self.start()

        except Exception as e:
            print(e)


if __name__ == "__main__":
    Upgrade().start()
