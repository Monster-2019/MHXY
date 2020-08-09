from time import sleep
from public.cutScreen import CScreen
from public.btn import Btn
from public.matchTem import Match
from public.glo import Glo
from public.log import log

class SJQY:
    def __init__(self):
        self.name = Glo().get('name')
        self.B = Btn()
        self.cutScreen = CScreen().cutScreen
        self.matchTem = Match().matchTem

    def start(self):
        log(f"账号: { self.name } 开始三界奇缘任务")
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
                temCoor = self.matchTem('sj_wc', simi=0.95) or self.matchTem('sj_wc1', simi=0.95)
                if temCoor != 0:
                    log(f"账号: { self.name } 三界奇缘任务已完成")
                    complete = True
                    break
            else:
                self.B.VBtn(-1)

        for n in range(21):
            self.B.VBtn(1)
        sleep(0.5)
        
        if not complete:
            log(f"账号: { self.name } 三界奇缘任务进行中")
            count = 0
            while True:
                self.cutScreen()
                temCoor = self.matchTem('hd_sjqy', simi=0.95) or self.matchTem('hd_sjqy1', simi=0.95)
                if temCoor != 0:
                    btnCoor = self.matchTem('cj', 'imgTem/hd_sjqy') or self.matchTem('cj', 'imgTem/hd_sjqy1')
                    newCoor = ((temCoor[0][0] + btnCoor[0][0], temCoor[0][1] + btnCoor[0][1]), btnCoor[1])
                    if btnCoor != 0:
                        self.B.LBtn(newCoor)
                        sleep(2)
                        break
                else:
                    count += 1
                    for i in range(10):
                        self.B.VBtn(-1)
                    sleep(0.5)
                    if count == 2:
                        log(f"账号: { self.name } 三界奇缘任务完成")
                        complete = True
                        break

            while not complete:
                self.cutScreen()
                temCoor = self.matchTem('sj_dw')
                if temCoor != 0:
                    self.B.RBtn()
                    complete = True
                    break
                else:
                    self.B.LBtn(((380, 230), (170, 240)), sleepT=0.5)
        else:
            self.B.RBtn()

        while True:
            self.cutScreen()
            temCoor = self.matchTem('hd')
            btnCoor = self.matchTem('sy')
            if temCoor != 0 and btnCoor != 0:
                self.B.LBtn(btnCoor)
            elif temCoor != 0 and btnCoor == 0:
                break
            else:
                self.B.RBtn()
            sleep(0.5)

        if complete:
            log(f"账号: { self.name } 三界奇缘任务结束")
            return 1
        else:
            self.start()

if __name__ == '__main__':
    SJQY().start()
