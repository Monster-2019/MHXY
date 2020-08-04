from time import sleep
from public.cutScreen import CScreen
from public.btn import Btn
from public.matchTem import Match

class Mijing:
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
                temCoor = self.matchTem('hd_mjxy', simi=0.97) or self.matchTem('hd_mjxy1', simi=0.98)
                if temCoor == 0:
                    complete = True
                    break
                else:
                    break
            self.B.VBtn(-1)

        for n in range(21):
            self.B.VBtn(1)
        sleep(0.5)

        # 匹配秘境降妖
        if not complete:
            isStart = False
            count = 0
            while True:
                self.cutScreen()
                temCoor = self.matchTem('hd_mjxy', simi=0.97) or self.matchTem('hd_mjxy1', simi=0.98)
                if temCoor != 0:

                    # 匹配秘境降妖的参加按钮
                    btnCoor = self.matchTem('cj', 'imgTem/hd_mjxy') or self.matchTem('cj', 'imgTem/hd_mjxy1')
                    newCoor = ((temCoor[0][0] + btnCoor[0][0], temCoor[0][1] + btnCoor[0][1]), btnCoor[1])
                    if btnCoor != 0:
                        self.B.LBtn(newCoor)
                        break

                else:
                    count += 1
                    for i in range(10):
                        self.B.VBtn(-1)
                    sleep(0.5)
                    if count == 2:
                        complete = True
                        isStart = True
                        break

            xhList = ['mj_mjxy', 'mj_mrh', 'mj_tz']
            while not isStart:
                for item in xhList:
                    self.cutScreen()
                    btnCoor = self.matchTem(item)
                    if btnCoor != 0:
                        if item == 'mj_tz':
                            self.B.LBtn(btnCoor, sleepT=1)
                            isStart = True
                            break

                        else:
                            self.B.LBtn(btnCoor, sleepT=0.5)

            xhList = ['hd', 'mj_17', 'sb', 'mj_mjxyrw', 'mj_jrzd', 'mj_lq', 'mj_gb']
            while not complete:
                for item in xhList:
                    self.cutScreen()
                    btnCoor = self.matchTem(item)
                    if btnCoor != 0:
                        if item == 'hd':
                            complete = True
                            sleep(1)
                            break
                            
                        elif item == 'sb':
                            self.B.LBtn(btnCoor)
                            sleep(1)

                            while True:
                                self.cutScreen()
                                btnCoor = self.matchTem('mj_lk')
                                if btnCoor != 0:
                                    self.B.LBtn(btnCoor, sleepT=0.5)
                                else:
                                    complete = True
                                    break

                        elif item == 'mj_17':
                            self.B.LBtn(((520, 380), (10, 10)))
                            while True:
                                self.cutScreen()
                                btnCoor = self.matchTem('mj_lk')
                                if btnCoor != 0:
                                    self.B.LBtn(btnCoor, sleepT=0.5)
                                else:
                                    complete = True
                                    break

                        elif item == 'mj_jrzd':
                            self.cutScreen()
                            tem = self.matchTem('mj_18')
                            if tem != 0:
                                while True:
                                    self.cutScreen()
                                    btnCoor = self.matchTem('mj_lk')
                                    if btnCoor != 0:
                                        self.B.LBtn(btnCoor, sleepT=0.5)
                                    else:
                                        complete = True
                                        break
                            else:
                                self.B.LBtn(btnCoor)

                        else:
                            self.B.LBtn(btnCoor)
                    
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
            sleep(0.5)

        if complete:
            return 1
        else:
            self.start()
        
if __name__ == '__main__':
    Mijing().start()