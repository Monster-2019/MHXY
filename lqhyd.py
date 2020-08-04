from time import sleep
from public.cutScreen import CScreen
from public.btn import Btn
from public.matchTem import Match

class LQHYD:
    def __init__(self):
        self.B = Btn()
        C = CScreen()
        self.cutScreen = C.cutScreen
        M = Match()
        self.matchTem = M.matchTem

    def start(self):
        complete = False
        self.cutScreen()

        while True:
            btnCoor = self.matchTem('hd')
            if btnCoor == 0:
                self.B.RBtn()
                self.cutScreen()
            else: 
                self.B.Hotkey('hd')
                sleep(0.5)
                break

        if not complete:
            xhList = ['hy_20', 'hy_40', 'hy_60', 'hy_80', 'hy_100']
            for item in xhList:
                while True:
                    self.cutScreen()
                    btnCoor = self.matchTem(item)
                    if btnCoor != 0:
                        self.B.LBtn(btnCoor, sleepT=0.5)
                        
                        self.cutScreen()
                        btnCoor = self.matchTem('sygb')
                        if btnCoor != 0:
                            self.B.LBtn(btnCoor, sleepT=0.2)
                            
                    if item == 'hy_100':
                        complete = True
                        
                    break
        else:
            self.B.RBtn()

        while True:
            self.cutScreen()
            btnCoor = self.matchTem('hd')
            if btnCoor == 0:
                self.B.RBtn()
            else: 
                break

        if complete:
            return 1
        else:
            self.start()
