import time
from time import sleep
from public.cutScreen import CScreen
from public.btn import Btn
from public.matchTem import Match
from public.smc import SMC
from public.glo import Glo
from public.log import log

class Ring:
    def __init__(self):
        super(Ring, self).__init__()
        self.g = Glo()
        self.name = self.g.get('name')
        self.B = Btn()
        self.cutScreen = CScreen().cutScreen
        self.matchTem = Match().matchTem
        self.smc = SMC().smc

    def isComplete(self):
        complete = False
        self.B.Hotkey('hd')

        self.smc('jjxx', sleepT=0.5)

        self.B.MBtn(590, 330)
        self.B.VBtn(1, 21)
        sleep(0.5)

        for n in range(21):
            if n % 10 == 0:
                sleep(0.5)
                res = self.smc('my_wc', simi=0.98, count=0)
                if res != 0:
                    log(f"账号: { self.name } 初级贸易已完成")
                    complete = True
                    break
            else:
                self.B.VBtn(-1)

        self.B.VBtn(1, 21)

        self.B.RBtn()

        return complete

    def compare(self, s):
        sleep(1)
        self.cutScreen()
        status = True
        sTime = time.time()
        eTime = time.time()
        while eTime - sTime < s:
            self.cutScreen()
            res = self.g.compare()
            if not res:
                status = False
                break

            else:
                eTime = time.time()

        return status

    def start(self):
        try:
            log(f"账号: { self.name } 开始初级贸易")
            complete = False
            processing = False

            while True:
                res = self.smc('hd', count=0)
                if res == 0:
                    self.B.RBtn()
                else:
                    sleep(0.5)
                    self.B.MBtn(900, 300)
                    self.B.VBtn(-1, 10)
                    sleep(0.5)

                    res = self.smc('rw_ring', simi=0.8, count=0)
                    if res != 0:
                        print(f"账号: { self.name } 已领取经验链")
                        processing = True
                    sleep(0.5)
                    break

            # if not processing:
                # complete = self.isComplete()

            if not complete:
                print(f"账号: { self.name } 经验链进行中")

                self.B.Hotkey('zz')
                sleep(1)
                self.B.LBtn('zr1')
                sleep(0.5)
                self.B.RBtn()
                sleep(0.5)

                if not processing:
                    self.B.Hotkey('hd')
                    self.smc('jjxx', sleepT=0.5)
                    page = 1
                    while True:
                        self.cutScreen()
                        temCoor = self.matchTem('hd_ring')
                        if temCoor != 0:
                            btnCoor = self.matchTem('cj', 'imgTem/hd_ring')
                            newCoor = ((temCoor[0][0] + btnCoor[0][0], temCoor[0][1] + btnCoor[0][1]), btnCoor[1])
                            if btnCoor != 0:
                                self.B.LBtn(newCoor)
                                sleep(1)

                                getList = ['dh_ring', 'dh_get_ring', 'qd_1']

                                while not processing:
                                    for item in getList:
                                        res = self.smc(item, sleepT=0.5)
                                        if res != 0:
                                            if item == 'qd_1':
                                                sleep(0.5)
                                                self.B.RBtn()
                                                processing = True
                                                break

                                break

                        else:
                            page += 1
                            self.B.MBtn(590, 330)
                            self.B.VBtn(-1, 10)
                            sleep(0.5)
                            if page == 4:
                                break

                else:
                    self.smc('rw_ring', simi=0.8, sleepT=1)

                myList = ['gm_1', 'gm_2', 'sj_1', 'sj_2', 'dh']

                while processing:
                    res = self.smc('zd_qx', count=0)
                    # 战斗状态判断
                    if res == 0:
                        self.cutScreen()
                        compareResult = self.compare(0.5)
                        # 站立状态判断
                        print(compareResult)
                        if compareResult:
                            sleep(0.5)
                            operating = False
                            for item in myList:
                                self.cutScreen()
                                btnCoor = self.matchTem(item)
                                if btnCoor != 0:
                                    if item == 'dh':
                                        newCoor = ((btnCoor[0][0] + 14, btnCoor[0][1] + 64), (247, 41))
                                        self.B.LBtn(newCoor)
                                    
                                    elif item == 'gm_2':
                                        self.B.LBtn(btnCoor)
                                        res = self.smc('gm_sb', count=0)
                                        if res == 0:
                                            newCoor = ((308, 245), (294, 75))
                                            self.B.LBtn(newCoor)

                                    else:
                                        self.B.LBtn(btnCoor)

                                    operating = True
                                    sleep(0.5)
                                    break

                            print(f'operating {operating}')
                            if not operating:
                                res = self.smc('hd', count=0)
                                if res == 0:
                                    break

                                else:
                                    sleep(0.5)
                                    self.B.MBtn(900, 300)
                                    self.B.VBtn(-1, 10)
                                    sleep(0.5)
                                    res = self.smc('rw_ring', simi=0.8)
                                    if res == 0:
                                        complete = True
                                        processing = False
                                        log(f"账号: { self.name } 经验链完成")
                                        break

            # complete = self.isComplete()

            if complete:
                log(f"账号: { self.name } 经验链结束")
                return 1
            else:
                self.start()
        
        except Exception as e:
            log(e, True)

if __name__ == "__main__":
    Ring().start()
