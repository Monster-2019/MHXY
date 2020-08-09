from time import sleep
from public.cutScreen import CScreen
from public.btn import Btn
from public.matchTem import Match
from public.log import log
from public.glo import Glo

class Guajiang:
    def __init__(self):
        self.name = Glo().get('name')
        self.B = Btn()
        self.cutScreen = CScreen().cutScreen
        self.matchTem = Match().matchTem

    def start(self):
        log(f"账号: { self.name } 开始刮奖")
        while True:
            self.cutScreen()
            btnCoor = self.matchTem('fl_dkggl')
            if btnCoor != 0:
                self.B.LBtn(btnCoor)
                sleep(1)
                break
            else:
                btnCoor = self.matchTem('fl')
                if btnCoor != 0:
                    self.B.LBtn(btnCoor)
                    sleep(0.5)

                self.cutScreen()
                btnCoor = self.matchTem('fl_mrfl')
                if btnCoor != 0:
                    self.B.LBtn(btnCoor)
                    sleep(0.5)

        self.B.DBtn((533, 396), (850, 485))

        xhList = [((655, 567), (66, 66)), ((550, 567), (66, 66)), ((760, 567), (66, 66)), ((865, 567), (66, 66))]
        for Coor in xhList:
            self.B.LBtn(Coor)
            sleep(0.5)

            self.cutScreen()
            btnCoor = self.matchTem('sygb')
            if btnCoor != 0:
                self.B.LBtn(btnCoor)
                sleep(0.3)

        sleep(0.5)
        self.B.RBtn()
        self.B.RBtn()
        self.B.RBtn()

        while True:
            self.cutScreen()
            temCoor = self.matchTem('hd')
            if temCoor == 0:
                self.B.RBtn()
            else: 
                break
        
        log(f"账号: { self.name } 刮奖完成")

if __name__ == '__main__':
    Guajiang().start()