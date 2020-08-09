from time import sleep
from time import time
from datetime import datetime
from public.cutScreen import CScreen
from public.matchTem import Match
from public.smc import SMC
from public.btn import Btn
from public.glo import Glo
from public.log import log

class GengZhong:
    def __init__(self):
        self.g = Glo()
        self.name = self.g.get('name')
        self.B = Btn()
        self.cutScreen = CScreen().cutScreen
        self.matchTem = Match().matchTem
        self.smc = SMC().smc
        self.weekday = datetime.today().weekday()

    def sell(self):
        while True:
            self.cutScreen()
            btnCoor = self.matchTem('hd')
            if btnCoor == 0:
                self.B.RBtn()
            else:
                break

        self.B.Hotkey('bb')
        sleep(0.5)
        self.smc('bb_zl', sleepT=0.5)
        self.B.MBtn(720, 440)
        self.B.VBtn(1, 30)
        sleep(0.5)

        page = 1
        while True:
            self.cutScreen()
            btnCoor = self.matchTem('bb_jyh')
            if btnCoor != 0:
                self.B.LBtn(btnCoor, sleepT=0.5)

                self.smc('bb_gd')

                self.smc('bb_gfbt', sleepT=1)
                self.B.RBtn()

                break
            else:
                self.B.MBtn(720, 440)
                self.B.VBtn(-1, 6)
                page += 1
                if page == 4:
                    log(f"账号: { self.name } 无金银花")
                    self.B.RBtn()
                    break

        complete = False
        count = 0
        while not complete:
            res = self.smc('gfbt_gq', simi=0.9, sleepT=0.5)
            if res != 0:
                self.smc('gfbt_cxsj', simi=0.9, sleepT=0.5)
                self.smc('bzts', simi=0.9, sleepT=0.5)
                self.smc('qd', simi=0.9, sleepT=0.5)
                count += 1
            else:
                complete = True
                break
        log(f"账号：{self.name} 重新上架{count}组金银花")

        complete = False
        count = 0
        while not complete:
            res = self.smc('gfbt_jyh', simi=0.9, infoKey='gfbt', sleepT=0.5)
            if res != 0:
                self.smc('gfbt_sj', simi=0.9, sleepT=0.5)
                res = self.smc('gfbt_max', sleepT=0.5)
                if res != 0:
                    complete = True
                    break
                self.smc('bzts', simi=0.9, sleepT=0.5)
                self.smc('qd', simi=0.9, sleepT=0.5)
                count += 1
            else:
                complete = True
                break
        log(f"账号：{self.name} 上架{count}组金银花")

        return complete

    def start(self):
        complete = False
        isTill = True
        
        while True:
            self.cutScreen()
            btnCoor = self.matchTem('hd')
            if btnCoor == 0:
                self.B.RBtn()
            else:
                break

        self.B.Hotkey('jy', sleepT=1)

        self.cutScreen()
        btnCoor = self.matchTem('jy_hj')
        if btnCoor != 0:
            self.B.LBtn(btnCoor, sleepT=3)

        self.cutScreen()
        btnCoor = self.matchTem('gz_sh')
        temCoor = self.matchTem('gz_td')
        if btnCoor == 0 and temCoor == 0:
            isTill = False
            complete = True

        xhList = ['gz_sh', 'sh', 'gz_td', 'gz_td1', 'gz_jyh', 'gz_lk', 'gz_zz']

        while isTill:
            for item in xhList:
                self.cutScreen()
                btnCoor = self.matchTem(item)
                if btnCoor != 0:
                    if item == 'gz_jyh' or item == 'gz_lk':
                        tCoor = self.matchTem('gz_prve')
                        if tCoor != 0:
                            self.B.LBtn(tCoor)
                        sleep(0.5)
                        temCoor = self.matchTem('gz_add', 'imgTem/gz_jyh')
                        newCoor = ((btnCoor[0][0] + temCoor[0][0], btnCoor[0][1] + temCoor[0][1]), temCoor[1])
                        while True:
                            self.cutScreen()
                            temCoor = self.matchTem('gz_max')
                            if temCoor == 0:
                                self.B.LBtn(newCoor)
                            else:
                                break
                    
                    elif item == 'gz_zz':
                        self.B.LBtn(btnCoor, sleepT=0.5)
                        self.cutScreen()
                        temCoor = self.matchTem('gf_nothl')
                        if temCoor != 0:
                            self.B.RBtn()
                        isTill = False
                        complete = True
                    
                    else:
                        self.B.LBtn(btnCoor)
                    sleep(0.4)

        if self.weekday == 3 or self.weekday == 6:
            self.sell()

        if complete:
            return 1
        else:
            self.start()

if __name__ == "__main__":
    GengZhong().sell()