import sys
sys.path.append('..')
from public.cutScreen import CScreen
from public.matchTem import Match
from public.btn import Btn
from time import sleep

class SMC(object):
    bb = (513, 202)

    def __init__(self):
        super(SMC, self).__init__()
        self.cutScreen = CScreen().cutScreen
        self.matchTem = Match().matchTem
        self.B = Btn()

    def smc(self, tem, infoKey="", simi=0.85, sleepT=0, count=1):
        self.cutScreen(infoKey=infoKey)
        Coor = self.matchTem(tem, simi=simi)
        if Coor != 0:
            if infoKey != '':
                Coor = ((self.bb[0] + Coor[0][0], self.bb[1] + Coor[0][1]), Coor[1])
            self.B.LBtn(Coor, count=count)
            sleep(sleepT)
            return 1
        return 0

if __name__ == '__main__':
    SMC().smc('bb_zzs')