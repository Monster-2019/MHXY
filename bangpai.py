from time import sleep
from public.cutScreen import CScreen
from public.btn import Btn
from public.matchTem import Match

class Bangpai:
    def __init__(self):
        self.B = Btn()
        C = CScreen()
        self.cutScreen = C.cutScreen
        M = Match()
        self.matchTem = M.matchTem

    def changeTask(self):
        processList = ['rw_dqrw', 'rw_cgrw', 'rw_bprw', 'rw_fqrw', 'qd']
        fq = False
        while not fq:
            self.B.Hotkey('rw')
            for item in processList:
                self.cutScreen()
                btnCoor = self.matchTem(item)
                if btnCoor != 0:
                    if item == 'qd':
                        self.B.LBtn(btnCoor)
                        fq = True
                    else:
                        self.B.LBtn(btnCoor)
                    sleep(0.8)

        self.B.RBtn()
        sleep(0.5)

        self.B.Hotkey('hd')
        sleep(1)

        # 匹配帮派任务
        self.cutScreen()
        temCoor = self.matchTem('hd_bprw')
        if temCoor != 0:
            self.cutScreen()
            btnCoor = self.matchTem('cj', 'imgTem/hd_bprw')
            newCoor = ((temCoor[0][0] + btnCoor[0][0], temCoor[0][1] + btnCoor[0][1]), btnCoor[1])
            if btnCoor != 0:
                self.B.LBtn(newCoor)
                processing = True

        else:
            return True

        while True:
            self.cutScreen()
            btnCoor = self.matchTem('dh')
            if btnCoor != 0:
                newCoor = ((btnCoor[0][0] + 14, btnCoor[0][1] + 64), (247, 41))
                self.B.LBtn(newCoor)
                break

        return False

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
                temCoor = self.matchTem('bp_ql')
                if temCoor != 0:
                    processing = True
                self.B.LBtn(btnCoor)
                sleep(0.5)
                break

        self.cutScreen()
        btnCoor = self.matchTem('rchd')
        if btnCoor != 0:
            self.B.LBtn(btnCoor)

        self.B.MBtn(590, 330)

        for n in range(21):
            self.B.VBtn(1)
        sleep(0.5)

        for n in range(21):
            if n % 10 == 0:
                self.cutScreen()
                temCoor = self.matchTem('bp_wc', simi=0.98)
                if temCoor != 0:
                    complete = True
                    break
            self.B.VBtn(-1)

        for n in range(21):
            self.B.VBtn(1)
        sleep(0.5)

        if not complete:
            if not processing:
                count = 0
                while not processing:
                    self.cutScreen()
                    temCoor = self.matchTem('hd_bprw')
                    if temCoor != 0:
                        while True:
                            self.cutScreen()
                            btnCoor = self.matchTem('cj', 'imgTem/hd_bprw')
                            newCoor = ((temCoor[0][0] + btnCoor[0][0], temCoor[0][1] + btnCoor[0][1]), btnCoor[1])
                            if btnCoor != 0:
                                self.B.LBtn(newCoor)

                                while True:
                                    self.cutScreen()
                                    btnCoor = self.matchTem('dh')
                                    if btnCoor != 0:
                                        newCoor = ((btnCoor[0][0] + 14, btnCoor[0][1] + 64), (247, 41))
                                        self.B.LBtn(newCoor)
                                        processing = True
                                        break
                                break

                    else:
                        count += 1
                        for i in range(10):
                            self.B.VBtn(-1)
                        sleep(0.5)
                        if count == 2:
                            complete = True
                            processing = True
                            break

            else:
                self.B.RBtn()
            
            bpList = ['gm', 'bp_shgm', 'dh', 'bp_bpwc']

            while not complete:
                self.cutScreen()
                temCoor = self.matchTem('hd')
                if temCoor != 0:
                    btnCoor = self.matchTem('bp_ql')
                    if btnCoor == 0:
                        sleep(2)
                        self.cutScreen()
                        temCoor = self.matchTem('hd')
                        if temCoor != 0:
                            btnCoor = self.matchTem('bp_ql')
                            if btnCoor == 0:
                                complete = self.changeTask()
                    else:
                        self.B.LBtn(btnCoor)

                for item in bpList:
                    self.cutScreen()
                    btnCoor = self.matchTem(item)
                    if btnCoor != 0:
                        if item == 'dh':
                            newCoor = ((btnCoor[0][0] + 14, btnCoor[0][1] + 64), (247, 41))
                            self.B.LBtn(newCoor)
                        elif item == 'bp_bpwc':
                            complete = True
                            break
                        else:
                            self.B.LBtn(btnCoor)

        else:
            self.B.RBtn()

        if complete:
            return 1
        else:
            self.start()
