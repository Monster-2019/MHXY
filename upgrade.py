from time import sleep
from public.cutScreen import CScreen
from public.btn import Btn
from public.matchTem import Match
from public.smc import SMC
from public.glo import Glo
from public.log import log


class Upgrade(object):
    def __init__(self):
        super(Upgrade, self).__init__()
        self.g = Glo()
        self.name = Glo().get('name')
        self.B = Btn()
        self.cutScreen = CScreen().cutScreen
        self.matchTem = Match().matchTem
        self.smc = SMC().smc
        self.smca = SMC().smca
        self.complete = False

    def start(self):
        log(f"账号: { self.name } 开始剧情任务")
        self.smc('hd', count=0)

        xhList = ['jqqd', 'dh', 'hd', 'djjx', 'djtg', 'up_mscs']

        while not self.complete:
            for item in xhList:
                btn = self.smc(item, count=0)
                # print(btn)
                if btn != 0:
                    if item == 'jqqd':
                        self.complete = True
                        break

                    elif item == 'dh':
                        coor = self.smc('dh', count=0)
                        newCoor = ((coor[0][0] + 14, coor[0][1] + 64), (247,
                                                                        41))
                        self.B.LBtn(newCoor, sleepT=0.5)

                        self.smc('qd')

                    elif item == 'hd':
                        if self.g.compare() == True:
                            self.B.Hotkey('rw', sleepT=1)

                            while True:
                                res = self.smc('up_zx')
                                if res != 0:
                                    break
                                else:
                                    self.smc('rw_dqrw')
                                    self.smc('up_zxjq')

                            self.smc('up_mscs')
                            self.smc('rw_gb')
                            sleep(1)

                    elif item == 'djjx':
                        while True:
                            res = self.smc(item, sleepT=0.2)
                            if res == 0:
                                break

                    elif item == 'djtg':
                        self.smc(item, count=2)

                    elif item == 'up_mscs':
                        self.B.RBtn()

        log(f"账号: { self.name } 剧情任务完成")


if __name__ == '__main__':
    Upgrade().start()