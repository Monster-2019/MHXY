import sys


from cutScreen import CScreen
from btn import Btn
from match import Match
from glo import Glo
from smc import SMC

class Lidui:
    def __init__(self):
        self.g = Glo()
        self.B = Btn()
        self.cutScreen = CScreen().cutScreen
        self.matchTem = Match().matchTem
        self.smc = SMC().smc
    
    def start(self):
        complete = False

        while True:
            self.smc('sb')
            res = self.smc('hd', count=0)
            if res == 0:
                self.B.RBtn()
            else: 
                break

        while True:
            self.B.Hotkey('dw')
            self.smc('tcdw', sleepT=1)
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