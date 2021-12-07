from time import sleep
from time import time
from datetime import datetime
from public.cutScreen import CScreen
from public.matchTem import Match
from public.smc import SMC
from public.btn import Btn
from public.glo import Glo
from public.log import log
import traceback


class GengZhong:
    def __init__(self):
        self.g = Glo()
        self.name = self.g.get('name')
        self.B = Btn()
        CScreenOjb = CScreen()
        self.cutScreen = CScreenOjb.cutScreen
        self.customCutScreen = CScreenOjb.customCutScreen
        self.matchTem = Match().matchTem
        self.smc = SMC().smc
        self.weekday = datetime.today().isoweekday()

    def sell(self):
        while True:
            res = self.smc('hd', count=0)
            if res == 0:
                self.B.RBtn()
            else:
                break

        self.B.Hotkey('bb')
        self.smc('bb_zl', sleepT=0.5)
        self.B.MBtn(720, 440)
        self.B.VBtn(1, 30)
        sleep(0.5)

        page = 1
        while True:
            res = self.smc('bb_jyh', sleepT=0.5)
            if res != 0:
                self.smc('bb_gd', sleepT=0.5)
                self.smc('bb_gfbt', sleepT=1)
                self.B.RBtn()
                break

            else:
                self.B.MBtn(720, 440)
                self.B.VBtn(-1, 6)
                page += 1
                if page == 6:
                    log(f"账号: { self.name } 无金银花")
                    self.B.RBtn()
                    break

        complete = False
        count = 0
        while not complete:
            res = self.smc('gfbt_gq', sleepT=0.5)
            if res != 0:
                self.smc('gfbt_cxsj', sleepT=0.5)
                self.smc('bzts', sleepT=0.5)
                self.smc('qd', sleepT=0.5)
                count += 1
            else:
                complete = True
                break
        log(f"账号：{self.name} 重新上架{count}组金银花")

        complete = False
        count = 0
        while not complete:
            self.customCutScreen('gfbt')
            res = self.matchTem('gfbt_jyh')
            if res:
                Coor = ((647 + res[0][0], 207 + res[0][1]), res[1])
                self.B.LBtn(Coor, sleepT=0.5)
            # res = self.smc('gfbt_jyh', infoKey='gfbt', sleepT=0.5)
            # if res != 0:
                self.smc('gfbt_sj', sleepT=0.5)
                res = self.smc('gfbt_max', sleepT=0.5)
                if res != 0:
                    complete = True
                    break
                self.smc('bzts', sleepT=0.5)
                self.smc('qd', sleepT=0.5)
                count += 1
            else:
                complete = True
                break

        self.B.RBtn()
        self.B.RBtn()

        log(f"账号：{self.name} 上架{count}组金银花")

        return complete

    def start(self, isSell=False):
        try:
            log(f"账号: { self.name } 开始耕种")
            complete = False
            isTill = True

            while True:
                res = self.smc('hd', count=0)
                if res == 0:
                    self.B.RBtn()
                else:
                    break

            self.B.Hotkey('jy', sleepT=1)

            self.smc('jy_hj', sleepT=3)

            while not self.smc('hd', count=0):
                sleep(1)

            self.cutScreen()
            btnCoor = self.matchTem('gz_sh')
            temCoor = self.matchTem('gz_td', simi=0.999)
            if btnCoor == 0 and temCoor == 0:
                isTill = False
                complete = True

            xhList = [
                'gz_sh', 'sh', 'gz_td', 'gz_prve', 'gz_jyh', 'gz_zz'
            ]

            count = 0
            while isTill:
                for item in xhList:
                    self.cutScreen()
                    btnCoor = self.matchTem(item, simi=0.998)
                    if btnCoor != 0:
                        if item == 'gz_jyh':
                            temCoor = self.matchTem('gz_add', 'imgTem/gz_jyh')
                            newCoor = ((btnCoor[0][0] + temCoor[0][0],
                                        btnCoor[0][1] + temCoor[0][1]),
                                       temCoor[1])
                            for n in range(10):
                                self.B.LBtn(newCoor)
                                sleep(0.1)

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

                    else:
                        if item == 'gz_td':
                            count+=1

                    sleep(0.5)

                if count == 5:
                    isTill = False
                    complete = True
                    break

            if ((self.weekday - 1) % 2 == 0) or isSell:
                self.sell()

            if complete:
                log(f"账号: { self.name } 耕种完成")
                return 1
            else:
                self.start()
        except Exception as e:
            # print(e)
            # traceback.print_exc()
            log(e, True)


if __name__ == "__main__":
    GengZhong().start(True)