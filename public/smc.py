import sys
sys.path.append('..')
from public.cutScreen import CScreen
from public.matchTem import Match
from public.btn import Btn
from time import sleep

class SMC(object):
    bb = (513, 202)
    gfbt = (647, 207)

    def __init__(self, hwnd=False):
        super(SMC, self).__init__()
        self.cutScreen = CScreen(hwnd).cutScreen
        self.matchTem = Match().matchTem
        self.B = Btn(hwnd)

    def smc(self, tem, infoKey="", simi=0.85, sleepT=0, count=1):
        self.cutScreen(infoKey=infoKey)
        Coor = self.matchTem(tem, simi=simi)
        if Coor != 0:
            if infoKey != '':
                imgCoor = getattr(self, infoKey)
                Coor = ((imgCoor[0] + Coor[0][0], imgCoor[1] + Coor[0][1]), Coor[1])
            self.B.LBtn(Coor, count=count)
            sleep(sleepT)
            return Coor
        return 0

if __name__ == '__main__':
    SMC().smc('bb_zzs')