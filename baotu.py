from time import sleep


class Baotu:

    def __init__(self, adb, task_finished):
        for key, val in adb.items():
            self[key] = val
        self.task_finished = task_finished

    def empty(self):
        while not self.smc('hd', is_click=False):
            self.btn.r()

        self.btn.hotkey("bb")

        self.smc('bb_zl')
        self.btn.m(720, 440)
        self.btn.v(1, 50)
        sleep(1)

        page = 1
        while True:
            has_cbt = self.smc('bb_cbt', is_click=False)
            if has_cbt:
                return has_cbt

            else:
                self.btn.m(700, 400)
                self.btn.v(-1, 6)
                page += 1
                if page == 6:
                    self.btn.r()
                    break

            sleep(0.2)

        return ()

    def dig(self):
        # 打开背包
        cbt_coor = self.empty()

        if cbt_coor:
            self.btn.l(cbt_coor, sleep_time=5)

            while cbt_coor:
                self.capture()
                is_hd = self.match('hd')
                coor = self.match('sy')

                if is_hd:
                    count = 0
                    while True:
                        coor = self.smc('sy')
                        if coor:
                            break
                        else:
                            count += 1

                        if count == 12:
                            cbt_coor = self.empty()
                            break

                    if coor[0] + coor[2] < 920:
                        self.btn.l(coor)
                        sleep(4)
                        count = 0

        return 1

    def start(self):
        while not self.smc('hd', is_click=False):
            self.btn.r()

        # 已领取
        # self.btn.MBtn(900, 300)
        # self.btn.v(1, 20)
        # sleep(0.5)

        # if self.matchTem('bt_btrw', simi=0.95):
        #     print(f"账号: { self.name } 已领取宝图任务")
        #     processing = True
        # sleep(0.5)

        if self.task_finished('bt_wc'):
            return

        self.btn.hotkey("hd")
        self.smc("rchd", sleep_time=0.5)
        self.btn.m(590, 330)
        self.btn.v(1, 31)
        sleep(0.5)

        processing = self.smc('bt_btrw', simi=0.95)

        if not processing:
            for n in range(31):
                if n % 10 == 0:
                    self.capture()
                    tem_coor = self.match("hd_btrw") or self.match("hd_btrw1")
                    if tem_coor:
                        btn_coor = self.match("cj",
                                              "imgTem/hd_btrw") or self.match(
                                                  "cj", "imgTem/hd_btrw1")
                        new_coor = ((
                            tem_coor[0] + btn_coor[0],
                            tem_coor[1] + btn_coor[1],
                            btn_coor[2],
                            btn_coor[3],
                        ))
                        if btn_coor:
                            self.btn.l(new_coor)
                            processing = True
                            sleep(5)

                            while True:
                                if self.smc('bt_ttwf'):
                                    break

                                sleep(2)

                            break
                else:
                    self.btn.v(-1)

        self.btn.r()

        if processing:
            step_list = ['bt_cbthdwc', 'bt_btrw']

            while processing:
                for item in step_list:
                    self.capture()
                    is_hd = self.match('hd')
                    coor = self.smc.smcs(item)
                    if coor and is_hd:
                        if item == 'bt_cbthdwc':
                            processing = False
                            break

                        else:
                            self.btn.l(coor, min_x=800)
                            sleep(5)

                    elif item == 'bt_btrw' and not coor and is_hd:
                        count = 0
                        while True:
                            is_hd = self.smc('hd', is_click=False)
                            if not is_hd:
                                count = 0
                            else:
                                count += 1

                            if count == 12:
                                processing = False
                                break

                            sleep(5)

        self.dig()


if __name__ == '__main__':
    Baotu().start()