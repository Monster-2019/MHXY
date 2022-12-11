from time import sleep
from datetime import datetime
from cutScreen import CScreen
from matchTem import Match
from zudui import Zudui
from btn import Btn
from glo import Glo
from smc import SMC
from log import log


class Zhuogui:
    def __init__(self):
        self.g = Glo()
        self.name = self.g.get('name')
        self.B = Btn()
        self.smc = SMC().smc
        self.matchTem = Match().matchTem
        self.cutScreen = CScreen().cutScreen
        self.index = self.g.get('screen')
        self.weekday = datetime.today().isoweekday()

    def leader(self):
        log(f"开始捉鬼任务")
        complete = True

        while self.smc('hd', count=0) == 0:
            self.B.RBtn()

        ZG_COUNT = int(self.g.getObj('config', 'ZG_COUNT'))
        if ZG_COUNT == 0:
            self.g.setObj('config', 'ZG_WC', True)
            return 1

        if not self.g.getObj('config', 'TeamStatus'):
            Zudui().start()

        self.B.Hotkey('hd')

        self.smc('rchd', sleepT=0.5)

        self.B.MBtn(590, 330)
        self.B.VBtn(1, 31)
        sleep(0.5)

        for n in range(31):
            if n % 10 == 0:
                sleep(0.5)
                self.cutScreen()
                res = self.matchTem('hd_zgrw')
                com = self.matchTem('zg_wc', simi=0.999)
                if com:
                    complete = True
                    break
                if res:
                    self.cutScreen()
                    temCoor = self.matchTem('hd_zgrw') or self.matchTem('hd_zgrw1')
                    if temCoor:
                        btnCoor = self.matchTem('cj',
                                                'imgTem/hd_zgrw') or self.matchTem(
                                                    'cj', 'imgTem/hd_zgrw1')
                        newCoor = ((temCoor[0][0] + btnCoor[0][0],
                                    temCoor[0][1] + btnCoor[0][1]), btnCoor[1])
                        if btnCoor:
                            self.B.LBtn(newCoor)
                            complete = False
                            break

            else:
                self.B.VBtn(-1)

        if not complete:
            complete = self.loop(ZG_COUNT)

        if complete:
            self.g.setObj('config', 'ZG_WC', True)
            log(f"捉鬼任务结束")
            return 1
        else:
            self.leader()

    def palyer(self):
        complete = False
        Zudui().start()
        while not self.g.getObj('config', 'ZG_WC'):
            # self.smc('xszk_gb')
            sleep(5)

        complete = True

        if complete:
            return 1
        else:
            self.palyer()

    def loop(self, loopCount=99):
        xlList = ['zg_zgrw', 'zg_zg', 'zg_zgwc']
        count = 0
        while count <= loopCount:
            for item in xlList:
                self.cutScreen()
                isHd = self.smc('hd', count=0)
                compare = self.g.compare()
                if item == 'zg_zg':
                    btnCoor = self.matchTem(item, simi=0.9)
                else:
                    btnCoor = self.matchTem(item, simi=0.99)

                if btnCoor and item == 'zg_zgwc':
                    if count < loopCount:
                        btnCoor = self.matchTem('qd')
                        if btnCoor:
                            self.B.LBtn(btnCoor)
                    else:
                        btnCoor = self.matchTem('qx')
                        if btnCoor:
                            self.B.LBtn(btnCoor)
                            log(f"捉鬼任务完成")
                            break
                
                elif isHd and btnCoor:
                    if item == 'zg_zgrw':
                        self.B.LBtn(btnCoor)
                        sleep(2)
                        self.B.RBtn()
                        count += 1
                        print(f'开始刷第{count}轮鬼')

                    elif item == 'zg_zg':
                        self.B.LBtn(btnCoor, sleepT=20)

                elif isHd:
                    if item == 'zg_zg':
                        self.B.MBtn(900, 300)
                        self.B.VBtn(1, 10)
        
        return 1

    def start(self):
        try:
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

            if res != 0:
                return 1
            else:
                self.start()

        except Exception as e:
            log(e, True)


if __name__ == '__main__':
    # Zhuogui().loop()
    Zhuogui().leader()