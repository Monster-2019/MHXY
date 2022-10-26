import sys
sys.path.append('..')
from cutScreen import CScreen
from matchTem import Match
from btn import Btn
from time import sleep

class SMC(object):
    def __init__(self, hwnd=False):
        super(SMC, self).__init__()
        self.cutScreen = CScreen(hwnd).cutScreen
        self.matchTem = Match().matchTem
        self.matchArrTem = Match().matchArrTem
        self.B = Btn(hwnd)

    def smc(self, tem, simi=0, sleepT=0, count=1):
        self.cutScreen()
        Coor = self.matchTem(tem, simi=simi)
        if Coor != 0:
            self.B.LBtn(Coor, count=count)
            sleep(sleepT)
            return Coor
        return 0

    def smca(self, tem, simi=0, sleepT=0, count=1):
        self.cutScreen()
        Coor = self.matchArrTem(tem, simi=simi)
        if Coor != 0:
            self.B.LBtn(Coor, count=count)
            sleep(sleepT)
            return Coor
        return 0

if __name__ == '__main__':
    SMC().smc('bt_wc')