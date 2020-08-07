from time import sleep
from public.cutScreen import CScreen
from public.btn import Btn
from public.matchTem import Match
from public.smc import SMC

class Shimen:
    def __init__(self):
        self.B = Btn()
        self.cutScreen = CScreen().cutScreen
        self.matchTem = Match().matchTem
        self.smc = SMC().smc

    def start(self):
        complete = False
        processing = False
        self.cutScreen()

        while True:
            btnCoor = self.matchTem('hd')
            if btnCoor == 0:
                self.B.RBtn()
                self.cutScreen()
            else:
                self.B.MBtn(900, 300)
                self.B.VBtn(1, 10)
                sleep(0.5)

                while True:
                    self.cutScreen()
                    temCoor = self.matchTem('sygb')
                    if temCoor != 0:
                        self.B.LBtn(temCoor, sleepT=0.5)
                    else:
                        break
                self.B.Hotkey('zz')
                self.B.LBtn('zr1')
                sleep(0.5)
                self.B.RBtn()
                sleep(0.5)
                self.B.Hotkey('hd')
                break

        self.cutScreen()
        btnCoor = self.matchTem('rchd')
        if btnCoor != 0:
            self.B.LBtn(btnCoor)

        self.B.MBtn(590, 330)

        self.B.VBtn(1, 21)
        sleep(0.5)

        for n in range(21):
            if n % 10 == 0:
                self.cutScreen()
                temCoor = self.matchTem('sm_wc', simi=0.95) or self.matchTem('sm_wc1', simi=0.95)
                if temCoor != 0:
                    complete = True
                    break
            else:
                self.B.VBtn(-1)
        
        self.B.VBtn(1, 21)
        sleep(0.5)

        if not complete:
            count = 0
            while not processing:
                self.cutScreen()
                temCoor = self.matchTem('hd_smrw', simi=0.95) or self.matchTem('hd_smrw1', simi=0.95)
                if temCoor != 0:
                    btnCoor = self.matchTem('cj', 'imgTem/hd_smrw') or self.matchTem('cj', 'imgTem/hd_smrw1')
                    newCoor = ((temCoor[0][0] + btnCoor[0][0], temCoor[0][1] + btnCoor[0][1]), btnCoor[1])
                    if btnCoor != 0:
                        self.B.LBtn(newCoor)

                    # 去完成或继续任务
                    while True:
                        self.cutScreen()
                        btnCoor = self.matchTem('sm_qwc') or self.matchTem('sm_jxrw')
                        if btnCoor != 0:
                            self.B.LBtn(btnCoor)
                            processing = True
                            break

                    break
                else:
                    self.B.VBtn(-1, 10)
                    count+=1
                    sleep(0.5)
                    if count == 2:
                        complete = True
                        processing = True
                        break

            smList = ['sm_gb', 'sm_sm', 'djjx', 'dh', 'dhda', 'gm', 'btgm', 'gfgm', 'sj', 'sy', 'sm_hdwp', 'sm_rwdh']

            while not complete:
                for item in smList:
                    self.cutScreen()
                    btnCoor = self.matchTem(item)
                    if btnCoor != 0:
                        if item == 'sm_sm':
                            self.B.LBtn(btnCoor, sleepT=1)
                            
                        elif item == 'dh' or item == 'dhda':
                            while True:
                                self.cutScreen()
                                btnCoor = self.matchTem('dh') or self.matchTem('dhda')
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

                        elif item == 'btgm' or item == 'gfgm':
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

                        elif item == 'sm_gb':
                            self.B.LBtn(btnCoor)
                            complete = True
                            break

                        else:
                            self.B.LBtn(btnCoor)

        else:
            self.B.RBtn()

        sleep(1)
            
        while True:
            self.cutScreen()
            temCoor = self.matchTem('hd')
            btnCoor = self.matchTem('sy')
            if temCoor != 0 and btnCoor != 0:
                self.B.LBtn(btnCoor, sleepT=0.5)
            elif temCoor != 0 and btnCoor == 0:
                break
            else:
                self.B.RBtn()
            sleep(0.5)

        if complete:
            return 1
        else:
            self.start()
