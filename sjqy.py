from time import sleep
from public.cutScreen import CScreen
from public.btn import Btn
from public.matchTem import Match
from public.smc import SMC
from public.glo import Glo
from public.log import log

class SJQY:
    def __init__(self):
        self.name = Glo().get('name')
        self.B = Btn()
        self.cutScreen = CScreen().cutScreen
        self.matchTem = Match().matchTem
        self.smc = SMC().smc

    def isComplete(self):
        complete = False
        self.B.Hotkey('hd')

        self.smc('rchd', sleepT=0.5)

        self.B.MBtn(590, 330)
        self.B.VBtn(1, 21)
        sleep(0.5)

        for n in range(21):
            if n % 10 == 0:
                sleep(0.5)
                res = self.smc(['sj_wc', 'sj_wc1'], simi=0.95, count=0)
                if res != 0:
                    log(f"账号: { self.name } 三界奇缘任务已完成")
                    complete = True
                    break
            else:
                self.B.VBtn(-1)

        self.B.VBtn(1, 21)

        self.B.RBtn()

        return complete

    def start(self):
        try:
            log(f"账号: { self.name } 开始三界奇缘任务")
            complete = False
            processing = False

            while True:
                res = self.smc('hd', count=0)
                if res == 0:
                    self.B.RBtn()
                else:
                    break

            complete = self.isComplete()

            if not complete:
                log(f"账号: { self.name } 三界奇缘任务进行中")

                self.B.Hotkey('hd')
                self.smc('rchd', sleepT=0.5)
                page = 1
                while True:
                    self.cutScreen()
                    temCoor = self.matchTem('hd_sjqy', simi=0.95) or self.matchTem('hd_sjqy1', simi=0.95)
                    if temCoor != 0:
                        btnCoor = self.matchTem('cj', 'imgTem/hd_sjqy') or self.matchTem('cj', 'imgTem/hd_sjqy1')
                        newCoor = ((temCoor[0][0] + btnCoor[0][0], temCoor[0][1] + btnCoor[0][1]), btnCoor[1])
                        if btnCoor != 0:
                            self.B.LBtn(newCoor)
                            processing = True
                            sleep(2)
                            break
                    else:
                        page += 1
                        self.B.VBtn(-1, 10)
                        sleep(0.5)
                        if page == 4:
                            break
                if not processing:
                    self.B.RBtn()

                while processing:
                    res = self.smc('sj_dw', count=0)
                    if res != 0:
                        self.B.RBtn()
                        complete = True
                        processing = False
                        break
                    else:
                        self.B.LBtn(((380, 230), (170, 240)), sleepT=0.5)

                sleep(0.5)
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
                log(f"账号: { self.name } 三界奇缘任务结束")
                return 1
            else:
                self.start()

        except Exception as e:
            log(e, True)

if __name__ == '__main__':
    SJQY().start()
