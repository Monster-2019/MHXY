import time
from time import sleep
from public.cutScreen import CScreen
from public.btn import Btn
from public.matchTem import Match
from public.smc import SMC
from public.glo import Glo
from public.log import log

class Trading:
    def __init__(self):
        super(Trading, self).__init__()
        self.name = Glo().get('name')
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

    def reEnter(self, useXsl=False):
        self.smc('my_gb', sleepT=1)

        self.B.MBtn(900, 300)
        self.B.VBtn(-1, 10)
        sleep(0.5)
        
        self.smc('rw_cjmy', sleepT=5)
        if useXsl:
            while True:
                self.smc('my_xsl_sy', sleepT=0.5)
                res = self.smc('qd', sleepT=1)
                if res != 0:
                    return True
                else:
                    result = self.smc('dh_qx')
                    if result != 0:
                        return False

    def start(self):
        try:
            log(f"账号: { self.name } 开始初级贸易")
            complete = False
            processing = False
            tem = False

            while True:
                res = self.smc('hd', count=0)
                if res == 0:
                    self.B.RBtn()
                else:
                    sleep(0.5)
                    self.B.MBtn(900, 300)
                    self.B.VBtn(-1, 10)
                    sleep(0.5)

                    res = self.smc('rw_cjmy', count=0)
                    if res != 0:
                        print(f"账号: { self.name } 已领取初级贸易")
                        processing = True
                        tem = True
                    sleep(0.5)
                    break

            if not processing:
                complete = self.isComplete()

            if not complete:
                print(f"账号: { self.name } 初级贸易进行中")

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
                        temCoor = self.matchTem('hd_my')
                        if temCoor != 0:
                            btnCoor = self.matchTem('cj', 'imgTem/hd_my')
                            newCoor = ((temCoor[0][0] + btnCoor[0][0], temCoor[0][1] + btnCoor[0][1]), btnCoor[1])
                            if btnCoor != 0:
                                self.B.LBtn(newCoor)
                                sleep(2)

                                # temList = ['dh_bpmy', 'my_xsl_add', 'my_xsl_dh']

                                # status = False
                                # while not status:
                                #     for item in temList:
                                #         self.cutScreen()
                                #         btnCoor = self.matchTem(item)
                                #         if btnCoor != 0:
                                #             if item == 'my_xsl_dh':
                                #                 while True:
                                #                     self.B.LBtn(btnCoor)
                                #                     res = self.smc(['my_xsl_no', 'my_xsl_ten', 'my_xsl_max'])
                                #                     if res != 0:
                                #                         status = True
                                #                         self.B.RBtn()
                                #                         break
                                #                 break
                                #             else:
                                #                 self.B.LBtn(btnCoor)

                                temList = ['dh_bpmy', 'my_dt_dxs', 'my_dt_ljs', 'my_dt_csc', 'my_dt_jyc']

                                for item in temList:
                                    while True:
                                        res = self.smc(item, sleepT=0.5)
                                        if res != 0:
                                            res = self.smc('my_dt_xz')
                                            if res != 0 or item == 'dh_bpmy':
                                                break

                                while True:
                                    res = self.smc('my_start')
                                    if res != 0:
                                        res = self.smc('qd')
                                        if res != 0:
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
                    self.smc('rw_cjmy', sleepT=5)

                myList = ['hd', 'my_gb', 'my_kszd', 'gm', 'btgm', ['my_msyj', 'my_jlh', 'my_mgh', 'my_cwnd'], 'my_sj', 'my_qd', 'qd', 'sj']

                sTime = time.time()
                eTime = time.time()
                while processing:
                    for item in myList:
                        self.cutScreen()
                        btnCoor = self.matchTem(item)
                        if btnCoor != 0:
                            sTime = time.time()
                            eTime = time.time()
                            if item == 'hd':
                                complete = True
                                processing = False
                                break

                            elif item == 'my_gb':
                                pass

                            elif item == 'my_kszd':
                                self.B.LBtn(btnCoor, sleepT=3)

                                startTime = time.time()
                                endTime = time.time()
                                while True:
                                    res = self.smc('zd_qx', count=0)
                                    if res != 0:
                                        startTime = time.time()
                                        endTime = time.time()
                                        sleep(0.5)
                                    else:
                                        endTime = time.time()

                                        res = self.smc('zd_sb', count=0, sleepT=0.5)
                                        if res != 0:
                                            result = self.reEnter(True)
                                            if not result:
                                                complete = True
                                                processing = False
                                                tem = False

                                            break
                                        else:
                                            if endTime > startTime + 3:
                                                break

                            elif item == 'btgm':
                                sleep(1)
                                res = self.smc('my_jin')
                                if res != 0:
                                    self.B.RBtn()
                                    sleep(1)
                                    res = self.smc(['my_msyj', 'my_jlh', 'my_mgh', 'my_cwnd'])
                                    if res != 0:
                                        while True:
                                            self.smc('my_xsl_sy', sleepT=0.5)
                                            res = self.smc('qd', sleepT=0.5)
                                            if res != 0:
                                                break
                                            else:
                                                result = self.smc('dh_qx')
                                                if result != 0:
                                                    complete = True
                                                    processing = False
                                                    tem = False
                                                    break
                                    else:
                                        while True:
                                            self.smc('my_sj', sleepT=0.5)
                                            self.smc('my_btgm', sleepT=1)
                                            res = self.smc('btgm', sleepT=1)
                                            if res != 0:
                                                result = self.smc('xfqr')
                                                if result != 0:
                                                    count = 0
                                                    while True:
                                                        res = self.smc('hd', count=0)
                                                        if res == 0 and count < 10:
                                                            self.B.RBtn()
                                                            count += 1
                                                        else:
                                                            break
                                                break
                                else:
                                    self.B.LBtn(btnCoor, sleepT=3)
                                    result = self.smc('xfqr')
                                    if result != 0:
                                        count = 0
                                        while True:
                                            res = self.smc('hd', count=0)
                                            if res == 0 and count < 10:
                                                self.B.RBtn()
                                                count += 1
                                            else:
                                                break

                            else:
                                self.B.LBtn(btnCoor)

                            sleep(0.5)

                        else:
                            if item == 'my_gb':
                                eTime = time.time()

                                if eTime - sTime > 90:
                                    self.reEnter()
                                    sTime = time.time()
                                    eTime = time.time()

                self.smc('dh_cjmy')

                while True:
                    res = self.smc('hd', count=0)
                    if res == 0:
                        self.B.RBtn()
                    else:
                        break

            if tem:
                log(f"账号: { self.name } 初级贸易完成一次")
                complete = self.isComplete()

            if complete:
                log(f"账号: { self.name } 初级贸易结束")
                return 1
            else:
                self.start()
        
        except Exception as e:
            log(e, True)

if __name__ == "__main__":
    Trading().start()
