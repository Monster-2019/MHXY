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
        complete = False
        self.B.Hotkey('hd')
        self.smc('rchd', sleepT=0.5)
        self.B.MBtn(590, 330)
        self.B.VBtn(1, 21)
        sleep(0.5)

        for n in range(21):
            if n % 10 == 0:
                sleep(0.5)
                self.cutScreen()
                res = self.matchTem('hd_zgrw') or self.matchTem('hd_zgrw1')
                if res != 0:
                    self.cutScreen(res)
                    res = self.matchTem('hd_no', simi=0.95)
                    if res == 0:
                        complete = True
                        log(f"捉鬼任务已完成")
                        self.g.setObj('config', 'ZG_WC', True)
                        break
                else:
                    res = self.smc('zg_wc') or self.smc('zg_wc1')
                    if res != 0:
                        complete = True
                        log(f"捉鬼任务已完成")
                        self.g.setObj('config', 'ZG_WC', True)
                        break
            self.B.VBtn(-1)

        self.B.VBtn(1, 21)
        self.B.RBtn()

        return complete

    def leader(self):
        log(f"开始捉鬼任务")
        complete = False
        processing = False

        while True:
            res = self.smc('hd', count=0)
            if res == 0:
                self.B.RBtn()
            else:
                break

        complete = self.isComplete()

        ZG_COUNT = int(self.g.getObj('config', 'ZG_COUNT'))

        if ZG_COUNT == 0:
            complete = True
            self.g.setObj('config', 'ZG_WC', True)

        if not complete:
            if not self.g.getObj('config', 'TeamStatus'):
                Zudui().start()

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
                        break
            if not processing:
                self.B.RBtn()

            xlList = ['zg_zg', 'zg_zgwc']
            count = 0
            total = 0
            totalMax = 0
            start = False
            if self.weekday > 5 and ZG_COUNT < 2:
                totalMax = 5

            while processing:
                if not start:
                    res = self.smc('zg_zgrw')
                    if res != 0:
                        self.B.RBtn()
                        self.B.RBtn()
                        count = 0
                        total += 1
                        start = True

                else:
                    for item in xlList:
                        self.cutScreen()
                        btnCoor = self.matchTem(item)
                        if btnCoor != 0:
                            if item == 'zg_zg':
                                count += 1
                                if total > ZG_COUNT and count > totalMax:
                                    self.B.LBtn(((511, 384), (2, 2)))
                                    self.B.LBtn(((511, 384), (2, 2)))
                                    isHC = False
                                    while True:
                                        self.B.Hotkey('dt')
                                        hc = self.smc('dt_cac', sleepT=2)
                                        isHC = isHC == True or (isHC == False
                                                                and hc != 0)
                                        res = self.smc('hd', count=0)
                                        if hc and res != 0:
                                            break

                                    sleep(3)

                                    complete = True
                                    processing = False
                                    self.g.setObj('config', 'ZG_WC', True)
                                    log(f"捉鬼任务完成")
                                    sleep(2)
                                    break

                                else:
                                    self.B.LBtn(btnCoor)
                                    print(f'开始刷第{count}次鬼')
                                    sleep(30)

                            elif item == 'zg_zgwc':
                                if total < ZG_COUNT or (total == ZG_COUNT
                                                        and totalMax != 0):
                                    btnCoor = self.matchTem('qd')
                                    if btnCoor != 0:
                                        self.B.LBtn(btnCoor)
                                        start = False

                                else:
                                    btnCoor = self.matchTem('qx')
                                    if btnCoor != 0:
                                        self.B.LBtn(btnCoor)
                                        complete = True
                                        processing = False
                                        self.g.setObj('config', 'ZG_WC', True)
                                        log(f"捉鬼任务完成")
                                        break

                        else:
                            if item == 'zg_zg' and start == True:
                                res = self.smc('hd', count=0)
                                if res != 0:
                                    # self.B.LBtn(((511, 384), (2, 2)))
                                    # self.B.LBtn(((511, 384), (2, 2)))
                                    tem = self.smc('fb_tgjq', count=0)
                                    if tem != 0:
                                        self.B.Hotkey('dt')
                                        self.smc('dt_cac', sleepT=1)
                                    else:
                                        self.B.MBtn(900, 300)
                                        self.B.VBtn(1, 10)

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
                if btnCoor != 0:
                    if item == 'zg_zgrw':
                        self.B.LBtn(btnCoor)
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
                        self.B.LBtn(btnCoor)
                        sleep(30)

                else:
                    if item == 'zg_zg':
                        self.B.MBtn(900, 300)
                        self.B.VBtn(1, 10)

    def start(self):
        try:
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

            if res != 0:
                return 1
            else:
                self.start()

        except Exception as e:
            log(e, True)


if __name__ == '__main__':
    Zhuogui().start()