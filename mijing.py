from time import sleep
from public.cutScreen import CScreen
from public.btn import Btn
from public.matchTem import Match
from public.smc import SMC
from public.glo import Glo
from public.log import log

class Mijing:
    def __init__(self):
        self.name = Glo().get('name')
        self.B = Btn()
        self.cutScreen = CScreen().cutScreen
        self.matchTem = Match().matchTem
        self.smc = SMC().smc

    def isComplete(self):
        complete = False
        self.B.Hotkey('hd')

        self.cutScreen()
        btnCoor = self.matchTem('rchd')
        if btnCoor != 0:
            self.B.LBtn(btnCoor)

        self.B.MBtn(590, 330)
        self.B.VBtn(1, 21)
        sleep(0.5)

        for n in range(21):
            if n % 10 == 0:
                sleep(0.5)
                self.cutScreen()
                temCoor = self.matchTem('hd_mjxy', simi=0.97) or self.matchTem('hd_mjxy1', simi=0.98)
                if temCoor == 0:
                    log(f"账号: { self.name } 秘境任务已完成")
                    complete = True
                    break
                else:
                    break
            self.B.VBtn(-1)

        self.B.VBtn(1, 21)

        self.B.RBtn()

        return complete

    def start(self):
        try:
            log(f"账号: { self.name } 开始秘境任务")
            complete = False
            processing = False

            while True:
                res = self.smc('hd', count=0)
                if res == 0:
                    self.B.RBtn()
                else:
                    break

            complete = self.isComplete()

            # 匹配秘境降妖
            if not complete:
                log(f"账号: { self.name } 秘境任务进行中")

                self.B.Hotkey('hd')
                self.smc('rchd', sleepT=0.5)
                page = 1
                while True:
                    self.cutScreen()
                    temCoor = self.matchTem('hd_mjxy', simi=0.97) or self.matchTem('hd_mjxy1', simi=0.98)
                    if temCoor != 0:
                        btnCoor = self.matchTem('cj', 'imgTem/hd_mjxy') or self.matchTem('cj', 'imgTem/hd_mjxy1')
                        newCoor = ((temCoor[0][0] + btnCoor[0][0], temCoor[0][1] + btnCoor[0][1]), btnCoor[1])
                        if btnCoor != 0:
                            self.B.LBtn(newCoor)
                            processing = True
                            break

                    else:
                        page += 1
                        self.B.VBtn(-1, 10)
                        sleep(0.5)
                        if page == 4:
                            break
                if not processing:
                    self.B.RBtn()

                xhList = ['mj_mjxy', 'mj_mrh', 'mj_tz']
                if processing:
                    while processing:
                        for item in xhList:
                            res = self.smc(item, sleepT=1)
                            if res != 0 and item == 'mj_tz':
                                processing = False
                                break

                    processing = True

                xhList = ['hd', 'mj_17', 'sb', 'mj_mjxyrw', 'mj_jrzd', 'mj_lq', 'mj_gb']
                
                while processing:
                    for item in xhList:
                        self.cutScreen()
                        btnCoor = self.matchTem(item, simi=0.8)
                        if btnCoor != 0:
                            if item == 'hd':
                                complete = True
                                processing = False
                                break
                                
                            elif item == 'sb' or item == 'mj_17':
                                if item == 'sb':
                                    self.B.LBtn(btnCoor)
                                    sleep(0.5)

                                # self.B.LBtn(((520, 380), (10, 10)))
                                while True:
                                    res = self.smc('mj_lk', sleepT=0.5)
                                    if res == 0:
                                        break

                            elif item == 'mj_jrzd':
                                sleep(0.5)
                                res = self.smc('mj_18')
                                if res != 0:
                                    while True:
                                        res = self.smc('mj_lk', sleepT=0.5)
                                        if res == 0:
                                            break

                                else:
                                    self.B.LBtn(btnCoor)

                            else:
                                self.B.LBtn(btnCoor)

                            sleep(5)

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
                log(f"账号: { self.name } 秘境任务结束")
                return 1
            else:
                self.start()
        except Exception as e:
            log(e, True)
        
if __name__ == '__main__':
    Mijing().start()