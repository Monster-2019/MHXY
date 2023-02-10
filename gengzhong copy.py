from time import sleep


class GengZhong(object):

    def __init__(self, adb, task_finished):
        for key, val in adb.items():
            self[key] = val
        self.task_finished = task_finished

    def sell(self):
        while True:
            res = self.smc('hd', count=0)
            if res == 0:
                self.btn.r()
            else:
                break

        self.btn.hotkey('bb')
        self.smc('bb_zl', sleep_time=0.5)
        self.B.MBtn(720, 440)
        self.B.VBtn(1, 30)
        sleep(0.5)

        page = 1
        while True:
            res = self.smc('bb_jyh', sleep_time=0.5)
            if res != 0:
                self.smc('bb_gd', sleep_time=0.5)
                self.smc('bb_gfbt', sleep_time=1)
                self.btn.r()
                break

            else:
                self.B.MBtn(720, 440)
                self.B.VBtn(-1, 6)
                page += 1
                if page == 6:
                    log(f"账号: { self.name } 无金银花")
                    self.btn.r()
                    break

        complete = False
        count = 0
        while not complete:
            res = self.smc('gfbt_gq', sleep_time=0.5)
            if res != 0:
                self.smc('gfbt_cxsj', sleep_time=0.5)
                self.smc('bzts', sleep_time=0.5)
                self.smc('qd', sleep_time=0.5)
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
                self.btn.l(Coor, sleep_time=0.5)
                # res = self.smc('gfbt_jyh', infoKey='gfbt', sleep_time=0.5)
                # if res != 0:
                self.smc('gfbt_sj', sleep_time=0.5)
                res = self.smc('gfbt_max', sleep_time=0.5)
                if res != 0:
                    complete = True
                    break
                self.smc('bzts', sleep_time=0.5)
                self.smc('qd', sleep_time=0.5)
                count += 1
            else:
                complete = True
                break

        self.btn.r()
        self.btn.r()

        log(f"账号：{self.name} 上架{count}组金银花")

        return complete

    def start(self, isSell=False):
        while not self.smc('hd', is_click=False):
            self.btn.r()

        self.btn.hotkey('jy', sleep_time=2)

        self.smc('jy_hj', sleep_time=3)

        while not self.smc('hd', count=0):
            sleep(1)

        self.capture()
        btnCoor = self.match('gz_sh')
        temCoor = self.match.match_tem_list(['gz_td', 'gz_td_l', 'gz_td_r'],
                                            simi=0.999)
        if btnCoor == 0 and temCoor == 0:
            isTill = False
            complete = True

        xhList = [
            'gz_sh', 'sh', 'gz_td', 'gz_td_l', 'gz_td_r', 'gz_prve', 'gz_jyh',
            'gz_zz'
        ]

        count = 0
        while isTill:
            for item in xhList:
                self.cutScreen()
                btnCoor = self.match(item, simi=0.998)
                if btnCoor != 0:
                    if item == 'gz_jyh':
                        temCoor = self.match('gz_add', 'imgTem/gz_jyh')
                        newCoor = ((btnCoor[0][0] + temCoor[0][0],
                                    btnCoor[0][1] + temCoor[0][1]), temCoor[1])
                        for n in range(10):
                            self.btn.l(newCoor)
                            sleep(0.1)
 
                    elif item == 'gz_zz':
                        self.btn.l(btnCoor, sleep_time=0.5)
                        self.cutScreen()
                        temCoor = self.matchTem('gf_nothl')
                        if temCoor != 0:
                            self.btn.r()
                        isTill = False
                        complete = True

                    else:
                        self.btn.l(btnCoor)

                else:
                    if item == 'gz_td' or item == 'gz_td_l' or item == 'gz_td_r':
                        count += 1

                sleep(0.5)

            if count == 5:
                isTill = False
                complete = True
                break

        if ((self.weekday - 1) % 2 == 0) or isSell:
            self.sell()


if __name__ == "__main__":
    GengZhong().start(True)