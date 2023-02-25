from time import sleep


class Bangpai(object):

    def __init__(self, adb, task_finished):
        for key, val in adb.items():
            self[key] = val
        self.task_finished = task_finished

    def changeTask(self, has_task=True):
        step_list = ["rw_dqrw", "rw_cgrw", "rw_bprw", "rw_fqrw", "qd"]

        if has_task:
            fq = False
            self.btn.hotkey("rw")

            while not fq:
                for item in step_list:
                    self.smc(item)
                    if item == 'qd':
                        fq = True
                        break

            self.btn.r()
            sleep(0.5)

        self.btn.hotkey("hd")
        self.smc("rchd", sleep_time=0.5)
        self.btn.m(590, 330)
        self.btn.v(1, 31)
        sleep(0.5)

        # 匹配帮派任务
        for n in range(31):
            if n % 10 == 0:
                self.capture()
                tem_coor = self.match("hd_bprw")
                btn_coor = self.match('cj', 'imgTem/hd_bprw')
                if tem_coor and btn_coor:
                    new_coor = ((tem_coor[0] + btn_coor[0],
                                 tem_coor[1] + btn_coor[1], btn_coor[2],
                                 btn_coor[3]))
                    self.btn.l(new_coor)
                    sleep(1)

                    while True:
                        if self.smc('bp_lqrw'):
                            return False

            else:
                self.btn.v(-1)

        return True

    def start(self):
        while not self.smc('hd', is_click=False):
            self.btn.r()

        if self.task_finished('bp_wc'):
            return

        self.btn.m(900, 300)
        self.btn.v(1, 10)
        sleep(0.5)

        if self.smc.smcs('bp_ql', is_click=False):
            processing = True

        if not processing:
            processing = not self.changeTask(False)

        step_list = ["bp_ql", "gm", "gm_shanghui", "dh_bprw", "bp_bpwc"]

        while processing:
            for item in step_list:
                self.capture()
                if item == "bp_ql":
                    coor = self.match.match_feature(item)
                else:
                    coor = self.match(item)
                if coor:
                    if item == "gm_shanghui":
                        sleep(1)
                        self.btn.l(coor, sleep_time=0.5)
                        res = self.smc(item, is_click=False)
                        if res:
                            self.btn.r()

                    elif item == "bp_bpwc":
                        processing = False
                        break

                    else:
                        self.btn.l(coor)

                else:
                    if item == "bp_ql":
                        if self.smc("hd", is_click=False):
                            self.btn.MBtn(900, 300)
                            self.btn.v(1, 10)

                            if self.smc("bp_ql", is_click=False):
                                if self.changeTas():
                                    processing = False
                                    break


if __name__ == "__main__":
    Bangpai().start()