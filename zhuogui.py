from time import sleep
from datetime import datetime, date
from public.cutScreen import CScreen
from public.matchTem import Match
from public.zudui import Zudui
from public.btn import Btn
from public.glo import Glo
from public.smc import SMC
from public.log import log

class Zhuogui:
    def __init__(self):
        self.g = Glo()
        self.B = Btn()
        self.smc = SMC().smc
        self.matchTem = Match().matchTem
        self.cutScreen = CScreen().cutScreen
        self.index = self.g.get('windowClass')
        self.weekday = datetime.today().weekday()

    def leader(self):
        complete = False

        while True:
            self.cutScreen()
            btnCoor = self.matchTem('hd')
            if btnCoor == 0:
                self.B.RBtn()
            else:
                self.B.Hotkey('hd')
                break

        self.smc('rchd')

        self.B.MBtn(590, 330)

        self.B.VBtn(1, 21)

        for i in range(21):
            if i % 10 == 0:
                self.cutScreen()
                temCoor = self.matchTem('zg_wc', simi=0.98) or self.matchTem('zg_wc1', simi=0.98)
                if temCoor != 0:
                    complete = True
                    self.g.setObj('config', 'ZG_WC', True)
                    break
            self.B.VBtn(-1)
        
        self.B.VBtn(1, 21)

        if self.g.getObj('config', 'ZG_COUNT') == 0:
            complete = True
            self.g.setObj('config', 'ZG_WC', True)

        if not complete:
            if not self.g.getObj('config', 'TeamStatus'):
                Zudui().start()

        sleep(0.5)
        self.B.RBtn()

        self.B.Hotkey('hd')

        self.smc('rchd')

        self.B.MBtn(590, 330)

        self.B.VBtn(1, 21)

        # 匹配捉鬼任务
        if not complete and self.g.getObj('config', 'ZG_COUNT') != 0:
            while True:
                self.cutScreen()
                temCoor = self.matchTem('hd_zgrw') or self.matchTem('hd_zgrw1')
                if temCoor != 0:
                    btnCoor = self.matchTem('cj', 'imgTem/hd_zgrw') or self.matchTem('cj', 'imgTem/hd_zgrw1')
                    newCoor = ((temCoor[0][0] + btnCoor[0][0], temCoor[0][1] + btnCoor[0][1]), btnCoor[1])
                    if btnCoor != 0:
                        self.B.LBtn(newCoor)
                        break
                    
                else:
                    self.B.VBtn(-1 ,10)
                    sleep(0.5)

            xlList = ['zg_zgrw', 'zg_zg', 'zg_zgwc']
            count = 0
            if self.weekday >= 5:
                count -= 1
            else:
                count -= 0

            while not complete:
                for item in xlList:
                    self.cutScreen()
                    btnCoor = self.matchTem(item)
                    if btnCoor != 0:
                        if item == 'zg_zgrw':
                            self.B.LBtn(btnCoor)
                            count+=1
                            log(f'开始刷第{count}轮鬼')

                        elif item == 'zg_zgwc':
                            if count < int(self.g.getObj('config', 'ZG_COUNT')):
                                btnCoor = self.matchTem('qd')
                                if btnCoor != 0:
                                    self.B.LBtn(btnCoor)
                            else:
                                btnCoor = self.matchTem('qx')
                                if btnCoor != 0:
                                    self.B.LBtn(btnCoor)
                                    complete = True
                                    self.g.setObj('config', 'ZG_WC', True)
                                    break

                        elif item == 'zg_zg':
                            self.B.LBtn(btnCoor)
                            self.B.LBtn(btnCoor)
                            sleep(30)
                            
        else:
            self.B.RBtn()
            complete = True
            self.g.setObj('config', 'ZG_WC', True)

        if complete:
            return 1
        else:
            return 0

    def palyer(self):
        complete = self.g.getObj('config', 'ZG_WC')
        Zudui().start()
        while not complete:
            sleep(3)
            complete = self.g.getObj('config', 'ZG_WC')

        if complete:
            return 1
        else:
            return 0

    def start(self):
        complete = False
        res = 0
        if int(self.index) == 0:
            res = self.leader()
        else:
            while self.g.getObj('config', 'ZG_WC') == None:
                sleep(3)

            if not self.g.getObj('config', 'ZG_WC'):
                res = self.palyer()
            else:
                res = 1

        if res == 1:
            return 1
        else:
            raise