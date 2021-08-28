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
            complete = False
            self.cutScreen()

            while True:
                res = self.smc('hd', count=0)
                if res == 0:
                    self.B.RBtn()
                else: 
                    break


            if not complete:
                self.B.Hotkey('hd')

                xhList = ['hy_20', 'hy_40', 'hy_60', 'hy_80', 'hy_100']
                for item in xhList:
                    while True:
                        res = self.smc(item, simi=0.95, sleepT=0.5)
                        if res != 0:
                            res = self.smc('sygb', sleepT=0.2)
                                
                        if item == 'hy_100':
                            complete = True
                        break

            sleep(0.5)
            # count = self.smc('hy_max', count=0, simi=0.98)
            self.B.RBtn()

            # hy_str = ''
            # if count != 0:
            #     hy_str = '----------------------------------------------------已满'
            # else:
            #     hy_str = '------------------------未满'

            if complete:
                log(f"账号: { self.name } 活跃度领取完成")
                return 1
            else:
                self.start()

        except Exception as e:
            log(e, True)
