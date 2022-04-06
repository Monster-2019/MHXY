from time import sleep
from datetime import datetime
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
        self.name = self.g.get('name')
        self.B = Btn()
        self.smc = SMC().smc
        self.matchTem = Match().matchTem
        self.cutScreen = CScreen().cutScreen
        self.index = self.g.get('screen')
        self.weekday = datetime.today().isoweekday()

    def isComplete(self):
        complete = True
        self.B.Hotkey('hd')
        self.smc('rchd', sleepT=0.5)
        self.B.MBtn(590, 330)
        self.B.VBtn(1, 31)
        sleep(0.5)

        for n in range(31):
            if n % 10 == 0:
                sleep(0.5)
                self.cutScreen()
                res = self.matchTem('hd_zgrw', simi=0.999)
                if res != 0:
                    complete = False
                    break

            else:
                self.B.VBtn(-1)

        self.B.VBtn(1, 31)
        self.B.RBtn()

        if complete:
            log('捉鬼任务已完成')
        self.g.setObj('config', 'ZG_WC', complete)
        return complete

    def leader(self):
        log(f"开始捉鬼任务")
        complete = False
        processing = False

        while self.smc('hd', count=0) == 0:
            self.B.RBtn()

        ZG_COUNT = int(self.g.getObj('config', 'ZG_COUNT'))
        if ZG_COUNT == 0:
            complete = True
            self.g.setObj('config', 'ZG_WC', True)
        else:
            complete = self.isComplete()

        if not complete:
            if not self.g.getObj('config', 'TeamStatus'):
                Zudui().start()

        self.B.Hotkey('zz', sleepT=1)
        self.B.LBtn('zr1', sleepT=0.5)
        self.B.LBtn('zr1', sleepT=0.5)
        self.B.RBtn()

        # 匹配捉鬼任务
        if not complete and ZG_COUNT != 0:
            print(f"捉鬼任务进行中")

            self.B.Hotkey('hd')
            self.smc('rchd', sleepT=0.5)
            page = 1
            while True:
                self.cutScreen()
                temCoor = self.matchTem('hd_zgrw') or self.matchTem('hd_zgrw1')
                if temCoor != 0:
                    btnCoor = self.matchTem('cj',
                                            'imgTem/hd_zgrw') or self.matchTem(
                                                'cj', 'imgTem/hd_zgrw1')
                    newCoor = ((temCoor[0][0] + btnCoor[0][0],
                                temCoor[0][1] + btnCoor[0][1]), btnCoor[1])
                    if btnCoor != 0:
                        self.B.LBtn(newCoor)
                        processing = True
                        break

                else:
                    page += 1
                    self.B.VBtn(-1, 10)
                    sleep(0.5)
                    if page == 4:
                        self.B.VBtn(1, 30)

            xlList = ['zg_zg', 'zg_zgwc']
            total = 0
            start = False
            end = False

            for i in range(ZG_COUNT):
                while not start:
                    res = self.smc('zg_zgrw')
                    if res != 0:
                        self.B.RBtn()
                        self.B.RBtn()
                        total += 1
                        print(f'开始第{total}轮捉鬼')
                        start = True
                        end = False
                    else:
                        while self.smc('hd', count=0) == 0:
                            self.B.RBtn()

                        self.B.MBtn(900, 300)
                        self.B.VBtn(1, 10)

                while not end:
                    for item in xlList:
                        self.cutScreen()
                        if item == 'zg_zg':
                            btnCoor = self.matchTem(item, simi=0.9)
                        else:
                            btnCoor = self.matchTem(item)
                        if btnCoor != 0:
                            if item == 'zg_zg':
                                self.B.LBtn(btnCoor)
                                sleep(30)

                            elif item == 'zg_zgwc':
                                if total < ZG_COUNT:
                                    if self.smc('qd') != 0:
                                        start = False
                                        end = True

                                else:
                                    if self.smc('qx') != 0:
                                        complete = True
                                        processing = False
                                        start = False
                                        end = True
                                        self.g.setObj('config', 'ZG_WC', True)
                                        log(f"捉鬼任务完成")
                                        break

                        else:
                            if item == 'zg_zg' and start == True:
                                res = self.smc('hd', count=0)
                                if res != 0:
                                    self.B.MBtn(900, 300)
                                    self.B.VBtn(1, 20)


        if complete:
            log(f"捉鬼任务结束")
            return 1
        else:
            self.leader()

    def palyer(self):
        complete = False
        Zudui().start()
        while not self.g.getObj('config', 'ZG_WC'):
            self.smc('xszk_gb')
            sleep(3)

        complete = True

        if complete:
            return 1
        else:
            self.palyer()

    def loop(self):
        print('开始捉鬼')
        complete = False
        xlList = ['zg_zgrw', 'zg_zg', 'zg_zgwc']
        count = 0
        while not complete:
            for item in xlList:
                self.cutScreen()
                btnCoor = self.matchTem(item)
                if item == 'zg_zg':
                    btnCoor = self.matchTem(item, simi=0.9)
                # compare = self.g.compare()
                if btnCoor != 0:
                    if item == 'zg_zgrw':
                        self.B.LBtn(btnCoor)
                        sleep(1)
                        self.B.RBtn()
                        count += 1
                        print(f'开始刷第{count}轮鬼')

                    elif item == 'zg_zgwc':
                        if count < 25:
                            btnCoor = self.matchTem('qd')
                            if btnCoor != 0:
                                self.B.LBtn(btnCoor)
                        else:
                            btnCoor = self.matchTem('qx')
                            if btnCoor != 0:
                                self.B.LBtn(btnCoor)
                                complete = True
                                self.g.setObj('config', 'ZG_WC', True)
                                log(f"捉鬼任务完成")
                                break

                    elif item == 'zg_zg':
                        self.B.LBtn(btnCoor)
                        # if compare:
                        #     self.B.RBtn()
                        sleep(20)

                else:
                    if item == 'zg_zg':
                        self.B.MBtn(900, 300)
                        self.B.VBtn(1, 10)

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
    # Zhuogui().start()
    Zhuogui().loop()