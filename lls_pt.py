from time import sleep
from public.cutScreen import CScreen
from public.matchTem import Match
from public.zudui import Zudui
from public.btn import Btn
from public.glo import Glo
from public.smc import SMC
from public.log import log

class LLSPT:
    def __init__(self):
        self.g = Glo()
        self.name = self.g.get('name')
        self.B = Btn()
        self.smc = SMC().smc
        self.matchTem = Match().matchTem
        self.cutScreen = CScreen().cutScreen
        self.index = self.g.get('windowClass')

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
                res = self.smc(['fb_llspt_wc', 'fb_llspt_wc1'], simi=0.95, count=0)
                if res != 0:
                    complete = True
                    self.g.setObj('config', 'FB_WC', True)
                    log(f"副本任务已完成")
                    break
            else:
                self.B.VBtn(-1)

        self.B.VBtn(1, 21)
        self.B.RBtn()

        return complete

    def leader(self):
        log(f"开始副本任务")
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
            if not self.g.getObj('config', 'TeamStatus'):
                Zudui().start()

        self.B.Hotkey('zz', sleepT=1)
        self.B.LBtn('zr1', sleepT=0.5)
        self.B.LBtn('zr2', sleepT=0.5)
        self.B.RBtn()

        if not complete:
            log(f"副本任务进行中")

            self.B.Hotkey('hd')
            self.smc('rchd', sleepT=0.5)
            page = 1
            while True:
                self.cutScreen()
                temCoor = self.matchTem('hd_lls_pt') or self.matchTem('hd_lls_pt1')
                if temCoor != 0:
                    btnCoor = self.matchTem('cj', 'imgTem/hd_lls_pt') or self.matchTem('cj', 'imgTem/hd_lls_pt1')
                    newCoor = ((temCoor[0][0] + btnCoor[0][0], temCoor[0][1] + btnCoor[0][1]), btnCoor[1])
                    if btnCoor != 0:
                        self.B.LBtn(newCoor)

                        while True:
                            res = self.smc('fb_xzfb')
                            if res != 0:
                                break
                        
                        clickStatus = False
                        while True:
                            self.cutScreen()
                            temCoor = self.matchTem('fb_lls_pt')
                            if temCoor != 0:
                                btnCoor = self.matchTem('fb_jr', 'imgTem/fb_lls_pt')
                                newCoor = ((temCoor[0][0] + btnCoor[0][0], temCoor[0][1] + btnCoor[0][1]), btnCoor[1])
                                if btnCoor != 0:
                                    self.B.LBtn(newCoor)
                                    processing = True
                                    clickStatus = True

                            elif temCoor == 0 and clickStatus:
                                break

                        break

                else:
                    page += 1
                    self.B.VBtn(-1 ,10)
                    sleep(0.5)
                    if page == 4:
                        break
            if not processing:
                self.B.RBtn()

            fbList = ['sb', 'hd', 'fb_tgjq', 'fb_lls', 'dh', 'djjx']

            while processing:
                for item in fbList:
                    self.cutScreen()
                    btnCoor = self.matchTem(item)
                    if btnCoor != 0:
                        if item == 'sb':
                            self.B.LBtn(btnCoor)
                            self.B.Hotkey('dt')
                            self.smc('dt_cac', sleepT=0.5)
                            break

                        elif item == 'hd':
                            complete = True
                            processing = False
                            self.g.setObj('config', 'FB_WC', True)
                            log(f"副本任务完成")
                            break

                        elif item == 'fb_lls':
                            self.B.LBtn(btnCoor, sleepT=3)

                        elif item == 'dh':
                            while True:
                                self.cutScreen()
                                btnCoor = self.matchTem('dh')
                                if btnCoor != 0:
                                    newCoor = ((btnCoor[0][0] + 14, btnCoor[0][1] + 64), (247, 41))
                                    self.B.LBtn(newCoor)
                                    sleep(0.3)
                                else:
                                    break

                        elif item == 'djjx':
                            while True:
                                res = self.smc('djjx', sleepT=0.3)
                                if res == 0:
                                    break

                        else:
                            self.B.LBtn(btnCoor)

        if complete:
            log(f"副本任务结束")
            return 1
        else:
            self.leader()

    def palyer(self):
        complete = False
        Zudui().start()
        while not self.g.getObj('config', 'FB_WC'):
            sleep(5)

        complete = True

        if complete:
            return 1
        else:
            self.palyer()

    def start(self):
        try:
            complete = False
            res = 0
            if int(self.index) == 0:
                res = self.leader()
            else:
                while self.g.getObj('config', 'FB_WC') == None:
                    sleep(3)
                    
                if not self.g.getObj('config', 'FB_WC'):
                    res = self.palyer()
                else:
                    res = 1

            if res != 0:
                return 1
            else:
                self.start()

        except Exception as e:
            log(e, True)

if __name__ == "__main__":
    LLSPT().start()