from time import sleep
from public.cutScreen import CScreen
from public.btn import Btn
from public.matchTem import Match


class Upgrade(object):

    def __init__(self):
        self.B = Btn()
        C = CScreen()
        self.cutScreen = C.cutScreen
        M = Match()
        self.matchTem = M.matchTem

    def matchTeam(self):
        self.B.Hotkey('dw')
        sleep(0.5)

        xhList = ['jq_select_target', 'target_zg']

        self.cutScreen()
        btnCoor = self.matchTem('cjdw')
        if btnCoor != 0:
            self.B.LBtn(btnCoor)

            complete = False
            while not complete:
                self.cutScreen()
                for item in xhList:
                    btnCoor = self.matchTem(item)
                    if btnCoor != 0:
                        self.B.LBtn(btnCoor)

                        if item == 'target_zg':
                            sleep(1)
                            # 选择等级
                            for i in range(3):
                                self.B.DBtn((560, 380), (560, 190))
                                sleep(1)

                            for i in range(5):
                                self.B.DBtn((660, 380), (660, 190))
                                sleep(1)

                            self.cutScreen()
                            btnCoor = self.matchTem('qdmb')
                            if btnCoor != 0:
                                self.B.LBtn(btnCoor, sleepT=0.5)
                                self.B.RBtn()
                                complete = True
                                break
        else:
            self.B.RBtn()

    def start(self):
        notTask = False
        
        while True:
            self.cutScreen()
            tem = self.matchTem('hd')
            if tem == 0:
                self.B.RBtn()
            else:
                break

        sleep(1)
        self.cutScreen()
        tem = self.matchTem('jq_jssj', simi=0.75) or self.matchTem('sjjq', simi=0.75) or self.matchTem('jqqd', simi=0.75)
        if tem != 0:
            notTask = True

        if not notTask:
            self.matchTeam()

            xhList = ['jq_jssj','sjjq', 'jqqd', 'hcsl', 'rwjm', 'djtgjq', 'djjx', 'dh', 'qd', 'zd']

            while not notTask:
                for item in xhList:
                    self.cutScreen()
                    if item == 'hcsl' or item == 'jq_jssj' or item == 'sjjq' or item == 'jqqd':
                        btnCoor = self.matchTem(item, simi=0.75)
                    else:
                        btnCoor = self.matchTem(item)
                    if btnCoor != 0:
                        if item == 'jq_jssj' or item == 'sjjq' or item == 'jqqd':
                            self.B.Hotkey('dw')
                            while True:
                                self.cutScreen()
                                btnCoor = self.matchTem('tcdw')
                                if btnCoor != 0:
                                    self.B.LBtn(btnCoor)
                                    self.B.RBtn()
                                    self.B.RBtn()

                                    notTask = True
                                    break

                        elif item == 'hcsl':
                            self.B.RBtn()
                            self.B.LBtn(((808, 163), (204, 75)))

                        elif item == 'rwjm':
                            self.B.RBtn()
                            sleep(0.5)
                            self.B.LBtn(((808, 163), (204, 75)))
                            sleep(1)

                        elif item == 'djtgjq' or item == 'djjx':
                            while True:
                                self.cutScreen()
                                btnCoor = self.matchTem(item)
                                if btnCoor != 0:
                                    self.B.LBtn(btnCoor)
                                else:
                                    break

                        elif item == 'dh':
                            while True:
                                self.cutScreen()
                                btnCoor = self.matchTem(item)
                                if btnCoor != 0:
                                    newCoor = ((btnCoor[0][0] + 14, btnCoor[0][1] + 64), (247, 41))
                                    self.B.LBtn(newCoor)
                                    sleep(0.3)
                                else:
                                    break

                        else:
                            self.B.LBtn(btnCoor)
                    else:
                        if item == 'hcsl':
                            self.cutScreen()
                            btnCoor = self.matchTem('hd')
                            if btnCoor != 0:
                                temCoor = self.matchTem('rw')
                                if temCoor != 0:
                                    self.B.Hotkey('dw')
                                    sleep(0.5)

                                    self.cutScreen()
                                    btnCoor = self.matchTem('zdpp', simi=0.95)
                                    if btnCoor != 0:
                                        self.B.LBtn(btnCoor)

                                    self.B.RBtn()
                                    sleep(0.5)

                                    self.cutScreen()
                                    btnCoor = self.matchTem('rw')
                                    if btnCoor != 0:
                                        self.B.LBtn(btnCoor)
                                else:
                                    self.B.LBtn(((808, 163), (204, 75)))

        if notTask:
            return 1
        else:
            self.start()

if __name__ == '__main__':
    Upgrade().start()