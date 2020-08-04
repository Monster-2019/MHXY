import sys
sys.path.append('..')
from time import sleep

from public.cutScreen import CScreen
from public.btn import Btn
from public.matchTem import Match
from public.glo import Glo
from public.smc import SMC

import random

class Lidui:
    def __init__(self):
        self.g = Glo()
        self.B = Btn()
        self.cutScreen = CScreen().cutScreen
        self.matchTem = Match().matchTem
        self.smc = SMC().smc
    
    def start(self):
        complete = False

        self.cutScreen()
        btnCoor = self.matchTem('sb')
        if btnCoor != 0:
            self.B.LBtn(btnCoor)

        while True:
            self.cutScreen()
            btnCoor = self.matchTem('hd')
            if btnCoor == 0:
                self.B.RBtn()
            else: 
                break

        self.B.Hotkey('dw')
        while True:
            self.smc('tcdw', sleepT=0.5)
            res = self.smc('cjdw', count=0)
            if res != 0:
                break

        self.B.RBtn()
        self.B.RBtn()
        complete = True

        if self.g.get('windowClass') == 0:
            self.g.setObj('config', 'TeamStatus', False)
        if complete:
            return 1
        else:
            return 0

if __name__ == '__main__':
    Lidui().start()