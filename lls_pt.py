from time import sleep
from public.cutScreen import CScreen
from public.matchTem import Match
from public.zudui import Zudui
from public.btn import Btn
from public.glo import Glo
from public.smc import SMC


class LLSPT:
    def __init__(self):
        self.g = Glo()
        self.B = Btn()
        self.smc = SMC().smc
        self.matchTem = Match().matchTem
        self.cutScreen = CScreen().cutScreen
        self.index = self.g.get('windowClass')

    def leader(self):
        complete = False

        while True:
            self.cutScreen()
            btnCoor = self.matchTem('hd')
            if btnCoor == 0:
                self.B.RBtn()
            else: 
                self.B.Hotkey('hd')
                break

        self.smc('rchd')
            
        self.B.MBtn(590, 330)

        self.B.VBtn(1, 21)

        for i in range(21):
            if i % 10 == 0:
                self.cutScreen()
                temCoor = self.matchTem('fb_llspt_wc', simi=0.95) or self.matchTem('fb_llspt_wc1', simi=0.95)
                if temCoor != 0:
                    complete = True
                    self.g.setObj('config', 'FB_WC', True)
                    break
            self.B.VBtn(-1)

        self.B.VBtn(1, 21)
        self.B.RBtn()

        if not complete:
            if not self.g.getObj('config', 'TeamStatus'):
                Zudui().start()

        self.B.Hotkey('zz')

        self.B.LBtn('zr1')
        self.B.LBtn('zr2')

        sleep(0.5)
        self.B.RBtn()

        self.B.Hotkey('hd')

        self.smc('rchd')

        self.B.MBtn(590, 330)

        self.B.VBtn(1, 21)

        if not complete:
            while True:
                self.cutScreen()
                temCoor = self.matchTem('hd_lls_pt') or self.matchTem('hd_lls_pt1')
                if temCoor != 0:
                    btnCoor = self.matchTem('cj', 'imgTem/hd_lls_pt') or self.matchTem('cj', 'imgTem/hd_lls_pt1')
                    newCoor = ((temCoor[0][0] + btnCoor[0][0], temCoor[0][1] + btnCoor[0][1]), btnCoor[1])
                    if btnCoor != 0:
                        self.B.LBtn(newCoor)

                        while True:
                            self.cutScreen()
                            btnCoor = self.matchTem('fb_xzfb')
                            if btnCoor != 0:
                                self.B.LBtn(btnCoor, sleepT=0.5)
                                break
                        
                        while True:
                            self.cutScreen()
                            temCoor = self.matchTem('fb_lls_pt')
                            if temCoor != 0:
                                btnCoor = self.matchTem('fb_jr', 'imgTem/fb_lls_pt')
                                newCoor = ((temCoor[0][0] + btnCoor[0][0], temCoor[0][1] + btnCoor[0][1]), btnCoor[1])
                                if btnCoor != 0:
                                    self.B.LBtn(newCoor)
                                    break

                        break

                else:
                    self.B.VBtn(-1 ,10)
                    sleep(0.5)

            fbList = ['sb', 'fb_tgjq', 'fb_lls', 'dh', 'djjx', 'hd']

            while not complete:
                for item in fbList:
                    self.cutScreen()
                    btnCoor = self.matchTem(item)

                    if btnCoor != 0:
                        if item == 'fb_lls':
                            self.B.LBtn(btnCoor, sleepT=3)

                        elif item == 'hd':
                            complete = True
                            self.g.setObj('config', 'FB_WC', True)
                            break

                        elif item == 'dh':
                            while True:
                                self.cutScreen()
                                btnCoor = self.matchTem('dh')
                                if btnCoor != 0:
                                    newCoor = ((btnCoor[0][0] + 14, btnCoor[0][1] + 64), (247, 41))
                                    self.B.LBtn(newCoor)
                                    sleep(0.3)
                                else:
                                    break

                        elif item == 'djjx':
                            while True:
                                self.cutScreen()
                                btnCoor = self.matchTem('djjx')
                                if btnCoor != 0:
                                    self.B.LBtn(btnCoor)
                                else:
                                    break

                        else:
                            self.B.LBtn(btnCoor)

        else:
            self.B.RBtn()

        if complete:
            return 1
        else:
            return 0

    def palyer(self):
        complete = False
        Zudui().start()
        while not complete:
            sleep(3)
            complete = self.g.getObj('config', 'FB_WC')

        if complete:
            return 1
        else:
            return 0

    def start(self):
        complete = False
        res = 0
        if int(self.index) == 0:
            res = self.leader()
        else:
            while self.g.getObj('config', 'FB_WC') == None:
                sleep(3)

            if not self.g.getObj('config', 'FB_WC'):
                res = self.palyer()
            else:
                res = 1

        if res == 1:
            return 1
        else:
            raise