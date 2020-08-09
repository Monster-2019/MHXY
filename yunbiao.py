from time import sleep
from public.cutScreen import CScreen
from public.btn import Btn
from public.matchTem import Match
from public.glo import Glo
from public.log import log

class Yunbiao:
    def __init__(self):
        self.name = Glo().get('name')
        self.B = Btn()
        self.cutScreen = CScreen().cutScreen
        self.matchTem = Match().matchTem

    def start(self):
        log(f"账号: { self.name } 开始运镖任务")
        complete = False

        while True:
            self.cutScreen()
            btnCoor = self.matchTem('hd')
            if btnCoor == 0:
                self.B.RBtn()
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
                temCoor = self.matchTem('yb_wc', simi=0.95) or self.matchTem('yb_wc1', simi=0.95)
                if temCoor != 0:
                    log(f"账号: { self.name } 运镖任务已完成")
                    complete = True
                    break
            self.B.VBtn(-1)
        
        for n in range(21):
            self.B.VBtn(1)
        sleep(0.5)

        if not complete:
            log(f"账号: { self.name } 运镖任务进行中")
            count = 0
            while True:
                self.cutScreen()
                temCoor = self.matchTem('hd_yb', simi=0.95)
                if temCoor != 0:
                    btnCoor = self.matchTem('cj', 'imgTem/hd_yb')
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
                        break

            count = 0
            xhList = ['yb_ys', 'qd']
            while True:
                self.cutScreen()
                temCoor = self.matchTem('hd')
                if temCoor != 0:
                    btnCoor = self.matchTem('yb_ys')
                    if btnCoor != 0:
                        ysStatus = False
                        while not ysStatus:
                            for item in xhList:
                                self.cutScreen()
                                btnCoor = self.matchTem(item)
                                if btnCoor != 0:
                                    if item == 'qd':
                                        while True:
                                            self.cutScreen()
                                            btnCoor = self.matchTem(item)
                                            if btnCoor != 0:
                                                self.B.LBtn(btnCoor, sleepT=0.5)
                                            else:
                                                count+=1
                                                ysStatus = True
                                                log(f'账号: { self.name } 正在进行第{ count }轮运镖')
                                                sleep(2)
                                                break

                                        while True:
                                            self.cutScreen()
                                            temCoor = self.matchTem('hd')
                                            if temCoor != 0:
                                                break

                                    else:
                                        self.B.LBtn(btnCoor, sleepT=0.5)

                    else:
                        if count != 0:
                            temCoor = self.matchTem('hd')
                            if temCoor != 0:
                                btnCoor = self.matchTem('yb_ys')
                                if btnCoor == 0:
                                    log(f"账号: { self.name } 运镖任务完成")
                                    complete = True
                                    break
                sleep(1)

        else:
            self.B.RBtn()

        if complete:
            log(f"账号: { self.name } 运镖任务结束")
            return 1
        else:
            self.start()
