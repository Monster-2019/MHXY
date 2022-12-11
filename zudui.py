from time import sleep
import sys

from cutScreen import CScreen
from btn import Btn
from matchTem import Match
from glo import Glo
from smc import SMC
from config import user

class Zudui(object):
    def __init__(self):
        super(Zudui, self).__init__()
        self.g = Glo()
        self.index = self.g.get('screen')
        self.B = Btn()
        self.cutScreen = CScreen().cutScreen
        self.matchTem = Match().matchTem
        self.smc = SMC().smc

    def leader(self):
        if not self.g.getObj('config', 'TeamStatus'):
            while True:
                self.cutScreen()
                tem = self.matchTem('hd')
                if tem == 0:
                    self.B.RBtn()
                else:
                    break

            self.B.Hotkey('dw')

            self.smc('cjdw', sleepT=0.5)
            if self.g.getObj('config', 'ZG_WC') == None:
                self.g.setObj('config', 'ZG_WC', False)
            if self.g.getObj('config', 'FB_WC') == None:
                self.g.setObj('config', 'FB_WC', False)

            self.smc('dw_sq')

            n = 0
            while n < len(user.ACCTZU[0]['acctList']) - 1:
                res = self.smc('dw_js', sleepT=1)
                if res != 0:
                    n+=1
                sleep(0.5)

            self.g.setObj('config', 'TeamStatus', True)

            self.B.RBtn()
            self.B.RBtn()

        return 1

    def player(self):
        if not self.g.getObj('config', 'TeamStatus'):
            while True:
                self.cutScreen()
                tem = self.matchTem('hd')
                if tem == 0:
                    self.B.RBtn()
                else:
                    break

            # n = 0
            while True:
                self.B.Hotkey('hy')
                self.smc('lxr', sleepT=0.5)

                self.cutScreen()
                temCoor = self.matchTem('dz')
                if temCoor != 0:
                    btnCoor = self.matchTem('jt', 'imgTem/dz')
                    if btnCoor != 0:
                        newCoor = ((temCoor[0][0] + btnCoor[0][0], temCoor[0][1] + btnCoor[0][1]), btnCoor[1])
                        self.B.LBtn(newCoor, sleepT=1)

                        res = self.smc('sqrd') or self.smc('sqrd1')
                        if res != 0:
                            break

                # else:
                #     n+=1
                #     self.B.MBtn(260, 440)
                #     self.B.VBtn(-1, 5)
                #     sleep(0.5)

            self.B.RBtn()
            self.B.RBtn()

        return 1

    def start(self):
        res = 0
        if int(self.index) == 0:
            res = self.leader()
        else:
            res = self.player()

        return res

if __name__ == '__main__':
    Zudui().start()