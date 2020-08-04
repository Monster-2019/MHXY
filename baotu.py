from time import sleep
from public.cutScreen import CScreen
from public.btn import Btn
from public.matchTem import Match
import time

class Baotu:
    def __init__(self):
        self.B = Btn()
        C = CScreen()
        self.cutScreen = C.cutScreen
        M = Match()
        self.matchTem = M.matchTem

    def start(self):
        complete = False
        processing = False

        while True:
            self.cutScreen()
            btnCoor = self.matchTem('hd')
            if btnCoor == 0:
                self.B.RBtn()
            else:
                temCoor = self.matchTem('bt_btrw')
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

        self.B.VBtn(1, 21)
        sleep(0.5)

        for n in range(21):
            if n % 10 == 0:
                self.cutScreen()
                temCoor = self.matchTem('bt_wc', simi=0.95) or self.matchTem('bt_wc1', simi=0.95)
                if temCoor != 0:
                    complete = True
                    break
            self.B.VBtn(-1)
        
        self.B.VBtn(1, 21)
        sleep(0.5)

        # 匹配宝图任务的参加按钮
        if not complete:
            if not processing:
                count = 0
                while True:
                    self.cutScreen()
                    temCoor = self.matchTem('hd_btrw', simi=0.95)
                    if temCoor != 0:
                        btnCoor = self.matchTem('cj', 'imgTem/hd_btrw')
                        newCoor = ((temCoor[0][0] + btnCoor[0][0], temCoor[0][1] + btnCoor[0][1]), btnCoor[1])
                        if btnCoor != 0:
                            self.B.LBtn(newCoor)
                            break
                    else:
                        count += 1
                        self.B.VBtn(-1, 10)
                        sleep(0.5)
                        if count == 2:
                            complete = True
                            break
            else:
                self.B.RBtn()

            xhList = ['bt_cbthdwc', 'bt_ttwf', 'bt_btrw']
            sTime = time.time()
            eTime = time.time()
            while not complete:
                self.cutScreen()
                temCoor = self.matchTem('hd')
                if temCoor != 0:
                    for item in xhList:
                        self.cutScreen()
                        btnCoor = self.matchTem(item)
                        if btnCoor != 0:
                            sTime = time.time()
                            if item == 'bt_cbthdwc':
                                complete = True
                                sleep(1)
                                break

                            elif item == 'bt_ttwf':
                                self.B.LBtn(btnCoor)
                                xhList.remove('bt_ttwf')

                            elif item == 'bt_btrw':
                                self.B.LBtn(btnCoor)
                                self.B.LBtn(btnCoor)
                                sleep(20)

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

        # 打开背包
        useComplete = False
        self.B.Hotkey("bb")
        sleep(0.5)

        self.cutScreen()
        btnCoor = self.matchTem('bb_zl')
        if btnCoor != 0:
            self.B.LBtn(btnCoor)

        self.B.MBtn(720, 440)

        self.B.VBtn(1, 30)
        sleep(1)

        page = 0
        while True:
            self.cutScreen()
            btnCoor = self.matchTem('bb_cbt')
            if btnCoor != 0:
                while True:
                    self.cutScreen()
                    btnCoor = self.matchTem('bb_cbt')
                    if btnCoor != 0:
                        self.B.LBtn(btnCoor)
                        self.B.LBtn(btnCoor)
                        sleep(1)
                    else:
                        break

                break
            else:
                self.B.MBtn(700, 400)
                self.B.VBtn(-1, 6)
                page += 1
                if page == 2:
                    useComplete = True
                    self.B.RBtn()
                    break

        startTime = time.time()
        endTime = time.time()
        while not useComplete:
            self.cutScreen()
            temCoor = self.matchTem('hd')
            if temCoor != 0:
                endTime = time.time()

                self.cutScreen()
                btnCoor = self.matchTem('sy')
                if btnCoor != 0:
                    if btnCoor[0][0] + btnCoor[1][0] < 920:
                        self.B.LBtn(btnCoor, sleepT=0)
                        timer1 = time.time()
                        timer2 = time.time()
                        while True:
                            self.cutScreen()
                            temCoor = self.matchTem('hd')
                            if temCoor != 0:
                                timer2 = time.time()

                                self.cutScreen()
                                btnCoor = self.matchTem('bt_xyz')
                                if btnCoor != 0:
                                    startTime = time.time()
                                    endTime = time.time()
                                    break

                            else:
                                timer1 = time.time()
                                timer2 = time.time()

                            if timer2 - timer1 >= 5:
                                useComplete = True
                                break

            else:
                startTime = time.time()
                endTime = time.time()

            if endTime - startTime >= 60:
                useComplete = True
                break

        if complete:
            return 1
        else:
            self.start()

if __name__ == '__main__':
    Baotu().start()
