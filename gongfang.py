from time import sleep

import win32gui
from public.cutScreen import CScreen
from public.btn import Btn
from public.matchTem import Match
from public.smc import SMC
from public.glo import Glo
from public.log import log
import time

class Gongfang:
    def __init__(self, hwnd):
        # self.g = Glo()
        # self.name = self.g.get('name')
        self.B = Btn(hwnd)
        self.cutScreen = CScreen(hwnd).cutScreen
        self.matchTem = Match().matchTem
        self.smc = SMC(hwnd).smc
        self.smca = SMC(hwnd).smca

    def kaogu(self):
        complete = False
        self.B.Hotkey('bb', sleepT=1)

        self.B.MBtn(707, 406)
        self.B.VBtn(1, 30)

        page = 0
        cz = 'bb_fjc'
        while True:
            r = self.smc(cz)
            if r != 0:
                self.B.LBtn(r)
                self.B.LBtn(r)
                sleep(1)

                r = self.smc('kg_not3')
                if r != 0:
                    cz = 'bb_lyc'
                    continue
                else:
                    break
                # raise
            else:
                self.B.MBtn(707, 406)
                page+=1
                self.B.VBtn(-1, 13)
                sleep(0.5)
                if page == 6:
                    self.B.RBtn()
                    return 0

        while True:
            r = self.smc('kg_ks', sleepT=1)
            if r != 0:
                break

        while True:
            r = self.smc('hd', count=0)
            if r == 0:
                self.B.RBtn()
            else:
                break

        stopTime1 = time.time()
        stopTime2 = time.time()
        for i in range(10):
            if not complete:
                while True:
                    self.cutScreen()
                    btnCoor = self.matchTem('wj')
                    if btnCoor != 0:
                        stopTime1 = time.time()
                        if btnCoor[0][0] + btnCoor[1][0] < 920:
                            self.B.LBtn(btnCoor, sleepT=3)
                            break

                    else:
                        stopTime2 = time.time()
                        if stopTime2 - stopTime1 >= 60:
                            complete = True
                            break
            else:
                break

        return 1

    def sell(self):
        # self.B.Hotkey('dt', sleepT=1)

        xhList = ['dt_lyc', 'zb_lyc', 'lyc_zhsr', 'kg_gdsm']

        isSell = False
        while not isSell:
            for item in xhList:
                r = self.smc(item)
                if r != 0 and item == 'kg_gdsm':
                    isSell = True
                    break

        xhList = ['kg_zp', 'kg_sm', 'kg_smwc']

        sell_status = False
        while not sell_status:
            for item in xhList:
                r = self.smc(item)
                if r != 0 and (item == 'kg_zp' or item == 'kg_smwc'):
                    sell_status = True
                    break
        
        while True:
            r = self.smc('hd', count=0)
            if r == 0:
                self.B.RBtn()
            else:
                break

        return 1

    def start(self):
        self.sell()

        return 0
        processing = False
        complete = False

        while True:
            res = self.smc('hd', count=0)
            if res == 0:
                self.B.RBtn()
            else:
                temCoor = self.matchTem('gf_kg', simi=0.7) or self.matchTem('gf_gf', simi=0.7)
                if temCoor != 0:
                    if temCoor[0][0] + temCoor[1][0] > 780:
                        processing = True
                sleep(0.5)
                break

        self.B.Hotkey('hd', sleepT=1)
        
        self.smc('jjxx')

        self.B.MBtn(590, 330)
        sleep(0.5)

        self.B.VBtn(1, 21)
        sleep(0.5)

        for n in range(3):
            res = self.smc('gf_wc', simi=0.95)
            if res != 0:
                complete = True
                break
            else:
                self.B.VBtn(-1, 10)

        self.B.VBtn(1, 21)
        sleep(0.5)

        if processing or not complete:
            if not processing:
                count = 0
                while not processing:
                    self.cutScreen()
                    temCoor = self.matchTem('hd_gfrw')
                    if temCoor != 0:
                        btnCoor = self.matchTem('cj', 'imgTem/hd_gfrw')
                        newCoor = ((temCoor[0][0] + btnCoor[0][0], temCoor[0][1] + btnCoor[0][1]), btnCoor[1])
                        if btnCoor != 0:
                            print(1, btnCoor)
                            self.B.LBtn(newCoor)
                            processing = True
                            break

                    else:
                        count += 1
                        self.B.VBtn(-1, 10)
                        sleep(0.5)
                        if count == 2:
                            complete = True
                            processing = True
                            break

            else:
                self.B.RBtn()

            xhList = ['gf_gfrwwc', 'gf_kg', 'gf_gf', 'gf_xz', 'dh', 'dhda', 'gfnot', 'gfgm', 'djjx', 'sy', 'sj']
            sTime = time.time()
            eTime = time.time()
            while not complete or processing:
                r = self.smc('hd', count=0)
                if r != 0:
                    for item in xhList:
                        self.cutScreen()
                        if item == 'gf_kg' or item == 'gf_gf':
                            btnCoor = self.matchTem(item, simi=0.7)
                        else:
                            btnCoor = self.matchTem(item)
                        if btnCoor != 0:
                            sTime = time.time()
                            if item == 'gf_gfrwwc':
                                complete = True
                                processing = False
                                break

                            elif item == 'gf_kg' or item == 'gf_gf':
                                if btnCoor[0][0] + btnCoor[1][0] > 780:
                                    self.B.LBtn(btnCoor)
                                elif btnCoor[0][0] + btnCoor[1][0] < 400:
                                    self.B.MBtn(200, 700)
                                    sleep(0.2)
                                    for i in range(5):
                                        self.B.VBtn(-1)

                            elif item == 'dh' or item == 'dhda':
                                while True:
                                    self.cutScreen()
                                    btnCoor = self.matchTem('dh') or self.matchTem('dhda')
                                    if btnCoor != 0:
                                        newCoor = ((btnCoor[0][0] + 14, btnCoor[0][1] + 64), (247, 41))
                                        self.B.LBtn(newCoor) 
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

                            elif item == 'gfgm':
                                self.B.LBtn(btnCoor)
                                self.cutScreen()
                                btnCoor = self.matchTem('gmsb')
                                if btnCoor != 0:
                                    newCoor = ((308, 245), (294, 75))
                                    self.B.LBtn(newCoor)
                                else:
                                    break

                            elif item == 'sy':
                                if (btnCoor[0][0] + btnCoor[1][0]) < 920:
                                    self.B.LBtn(btnCoor)

                            elif item == 'gfnot':
                                self.B.RBtn()
                                complete = True
                                processing = False
                                break

                            else:
                                self.B.LBtn(btnCoor)

                        else:
                            eTime = time.time()
                            if eTime - sTime > 60:
                                complete = True
                                sleep(1)
                                break
                else:
                    sTime = time.time()
                    eTime = time.time()

        else:
            self.B.RBtn()

        result = self.kaogu()
        if result == 1:
            self.sell()

        if complete:
            return 1
        else:
            self.start()

if __name__ == '__main__':
    hwnd = win32gui.FindWindow(None, '《梦幻西游》手游')
    Gongfang(hwnd).start()
