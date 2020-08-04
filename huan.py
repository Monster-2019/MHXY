from time import sleep
from public.cutScreen import CScreen
from public.btn import Btn
from public.matchTem import Match
from public.ocr import OCR
from public.glo import Glo

class Huan:
    def __init__(self):
        self.g = Glo()
        self.GM_AMOUNT = self.g.getObj('config', 'GM_AMOUNT')
        self.MAX_AMOUNT = self.g.getObj('config', 'MAX_AMOUNT')
        self.B = Btn()
        self.ocr = OCR().ocr
        self.cutScreen = CScreen().cutScreen
        self.matchTem = Match().matchTem

    def getLegend(self):
        self.cutScreen()
        temCoor = self.matchTem('h_wp1')
        if temCoor == 0:
            temCoor = self.matchTem('h_sysj')
            if temCoor != 0:
                self.B.Hotkey('gj')
                sleep(1)
                self.cutScreen()
                btnCoor = self.matchTem('h_dymg1gj', simi=0.95) or self.matchTem('h_hdmg3gj', simi=0.95) or self.matchTem(
                    'h_hdmg2gj', simi=0.95) or self.matchTem('h_hdmg4gj', simi=0.95)
                if btnCoor != 0:
                    self.B.LBtn(btnCoor, sleepT=0.5)

                    self.cutScreen()
                    btnCoor = self.matchTem('qr') or self.matchTem('qd')
                    if btnCoor != 0:
                        self.B.LBtn(btnCoor)

                while True:
                    self.cutScreen()
                    temCoor = self.matchTem('hd')
                    if temCoor != 0:
                        temCoor = self.matchTem('h_wp1')
                        if temCoor != 0:
                            return True

                        temCoor = self.matchTem('h_sysj')
                        if temCoor == 0:
                            self.B.LBtn(((519, 402), (2, 2)))
                            return False

            else:
                return False
        else:
            return True

    def start(self):
        complete = False
        ylq = False
        self.cutScreen()

        while True:
            btnCoor = self.matchTem('hd')
            if btnCoor == 0:
                self.B.RBtn()
                self.cutScreen()
            else:
                temCoor = self.matchTem('h_jyl', simi=0.8)
                if temCoor != 0:
                    ylq = True
                self.B.LBtn(btnCoor)
                sleep(0.5)
                break

        self.cutScreen()
        btnCoor = self.matchTem('jjxx')
        if btnCoor != 0:
            self.B.LBtn(btnCoor)

        self.B.MBtn(590, 330)

        for n in range(21):
            self.B.VBtn(1)
        sleep(0.5)

        for n in range(21):
            if n % 10 == 0:
                self.cutScreen()
                temCoor = self.matchTem('h_wc', simi=0.95)
                if temCoor != 0:
                    complete = True
                    break
            self.B.VBtn(-1)

        for n in range(21):
            self.B.VBtn(1)
        sleep(0.5)

        if ylq or not complete:
            if not ylq:
                while not ylq:
                    self.cutScreen()
                    temCoor = self.matchTem('hd_jyl')
                    if temCoor != 0:
                        btnCoor = self.matchTem('cj', 'imgTem/hd_jyl')
                        newCoor = (
                            (temCoor[0][0] + btnCoor[0][0], temCoor[0][1] + btnCoor[0][1]), btnCoor[1])
                        if btnCoor != 0:
                            self.B.LBtn(newCoor)
                            sleep(0.5)

                            xhList = ['h_lqrwl', 'h_lq', 'qd']

                            while not ylq:
                                for item in xhList:
                                    self.cutScreen()
                                    btnCoor = self.matchTem(item)
                                    if btnCoor != 0:
                                        if item == 'qd':
                                            self.B.LBtn(btnCoor)
                                            ylq = True
                                            break
                                        else:
                                            self.B.LBtn(btnCoor)

                    else:
                        for i in range(10):
                            self.B.VBtn(-1)
                        sleep(0.5)

            else:
                self.B.RBtn()

            xhList = ['h_200wc', 'h_200wc1', 'xfqr', 'h_jyl', 'gm', 'btgm', 'qd', 'dh', 'sj']

            gj = False
            legend = False
            amount = 0
            while not complete or ylq:
                for item in xhList:
                    self.cutScreen()
                    btnCoor = self.matchTem(item, simi=0.8)
                    if btnCoor != 0:
                        if item == 'h_200wc' or item == 'h_200wc1' or item == 'xfqr':
                            self.B.RBtn()
                            self.B.RBtn()
                            complete = True
                            ylq = False
                            break
                        elif item == 'h_jyl':
                            self.B.LBtn(btnCoor)
                            sleep(1)

                        elif item == 'btgm':
                            temCoor = self.matchTem('h_jin')
                            if temCoor != 0:
                                if not gj:
                                    while True:
                                        self.cutScreen()
                                        tem = self.matchTem('btgm')
                                        if tem != 0:
                                            break
                                        else:
                                            sleep(0.5)
                                    sleep(1)
                                    self.cutScreen('btgm')
                                    amount = int(self.ocr())
                                if not legend:
                                    #  or (gj and not legend and amount <= self.MAX_AMOUNT)
                                    if (amount != 0 and amount <= self.GM_AMOUNT): 
                                        while True:
                                            self.cutScreen()
                                            btnCoor = self.matchTem('btgm')
                                            if btnCoor != 0:
                                                self.B.LBtn(btnCoor)
                                                legend = True
                                                gj = False

                                                self.cutScreen()
                                                btnCoor = self.matchTem('qr')
                                                if btnCoor != 0:
                                                    self.B.LBtn(btnCoor)

                                                self.cutScreen()
                                                btnCoor = self.matchTem('gmsb')
                                                if btnCoor != 0:
                                                    newCoor = ((308, 245), (294, 75))
                                                    self.B.LBtn(newCoor)

                                            else:
                                                break

                                    elif gj and not legend:
                                        self.B.RBtn()
                                        complete = True
                                        ylq = False
                                        gj = False
                                        break
                                        
                                    else:
                                        self.B.RBtn()
                                        legend = self.getLegend()
                                        gj = True
                            else:
                                self.B.LBtn(btnCoor)

                        elif item == 'dh':
                            while True:
                                self.cutScreen()
                                btnCoor = self.matchTem('dh')
                                if btnCoor != 0:
                                    newCoor = (
                                        (btnCoor[0][0] + 14, btnCoor[0][1] + 64), (247, 41))
                                    self.B.LBtn(newCoor, sleepT=0.4)
                                else:
                                    break

                        elif item == 'sj':
                            legend = False
                            gj = False
                            self.B.LBtn(btnCoor)

                        else:
                            self.B.LBtn(btnCoor)

        else:
            self.B.RBtn()

        if complete:
            return 1
        else:
            self.start()

if __name__ == '__main__':
    Huan().start()
