from time import sleep
from time import time
from public.cutScreen import CScreen
from public.matchTem import Match
from public.btn import Btn
from public.glo import Glo

class GengZhong:
    def __init__(self):
        self.g = Glo()
        self.B = Btn()
        self.cutScreen = CScreen().cutScreen
        self.matchTem = Match().matchTem

    def start(self):
        complete = False
        isTill = True
        
        while True:
            self.cutScreen()
            btnCoor = self.matchTem('hd')
            if btnCoor == 0:
                self.B.RBtn()
            else:
                break

        self.B.Hotkey('jy', sleepT=1)

        self.cutScreen()
        btnCoor = self.matchTem('jy_hj')
        if btnCoor != 0:
            self.B.LBtn(btnCoor, sleepT=3)

        self.cutScreen()
        btnCoor = self.matchTem('gz_sh')
        temCoor = self.matchTem('gz_td')
        if btnCoor == 0 and temCoor == 0:
            isTill = False
            complete = True

        xhList = ['gz_sh', 'sh', 'gz_td', 'gz_td1', 'gz_jyh', 'gz_lk', 'gz_zz']

        while isTill:
            for item in xhList:
                self.cutScreen()
                btnCoor = self.matchTem(item)
                if btnCoor != 0:
                    if item == 'gz_jyh' or item == 'gz_lk':
                        tCoor = self.matchTem('gz_prve')
                        if tCoor != 0:
                            self.B.LBtn(tCoor)
                        sleep(0.5)
                        temCoor = self.matchTem('gz_add', 'imgTem/gz_jyh')
                        newCoor = ((btnCoor[0][0] + temCoor[0][0], btnCoor[0][1] + temCoor[0][1]), temCoor[1])
                        while True:
                            self.cutScreen()
                            temCoor = self.matchTem('gz_max')
                            if temCoor == 0:
                                self.B.LBtn(newCoor)
                            else:
                                break
                    
                    elif item == 'gz_zz':
                        self.B.LBtn(btnCoor, sleepT=0.5)
                        self.cutScreen()
                        temCoor = self.matchTem('gf_nothl')
                        if temCoor != 0:
                            self.B.RBtn()
                        isTill = False
                        complete = True
                    
                    else:
                        self.B.LBtn(btnCoor)
                    sleep(0.4)

        if complete:
            return 1
        else:
            self.start()
