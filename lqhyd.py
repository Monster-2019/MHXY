from time import sleep
from public.cutScreen import CScreen
from public.matchTem import Match
from public.btn import Btn
from public.smc import SMC
from public.glo import Glo
from public.log import log

class LQHYD:
    def __init__(self):
        self.name = Glo().get('name')
        self.B = Btn()
        self.cutScreen = CScreen().cutScreen
        self.matchTem = Match().matchTem
        self.smc = SMC().smc

    def start(self):
        try:
            while self.smc('hd', count=0) == 0:
                self.B.RBtn()

            self.B.Hotkey('hd')

            xhList = ['hy_20', 'hy_40', 'hy_60', 'hy_80', 'hy_100']
            for item in xhList:
                while True:
                    res = self.smc(item, simi=0.95, sleepT=0.5)
                    if res:
                        res = self.smc('sygb', sleepT=0.2)
                            
                    if item == 'hy_100':
                        complete = True
                    break

            sleep(0.5)
            self.B.RBtn()

            if complete:
                log(f"账号: { self.name } 活跃度领取完成")
                return 1
            else:
                self.start()

        except Exception as e:
            log(e, True)
