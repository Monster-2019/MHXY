from time import sleep


class Bangpai(object):

    def __init__(self, adb):
        for key, val in adb.items():
            self.__dict__[key] = val
        if adb["print"]:
            global print
            print = adb["print"]

    def check_in(self):
        while not self.smc('hd', is_click=False):
            self.btn.r()

        self.btn.hotkey('bp')

        step_list = ['bp_fl', 'bp_check_in', 'bp_check_finish']

        complete = False
        while not complete:
            for item in step_list:
                coor = self.smc(item)
                if coor and item == 'bp_check_finish':
                    complete = True
                    self.btn.r()
                    break

                sleep(1 / len(step_list))

        print(f'{self.name}签到完成')

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

                    sleep(0.2)

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
                btn_coor = self.match('cj', screen='imgTem/hd_bprw')
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
        processing = False

        while not self.smc('hd', is_click=False):
            self.btn.r()

        if self.task_finished('bp_wc'):
            return

        self.btn.m(900, 300)
        self.btn.v(1, 10)
        sleep(0.5)

        if self.smc.smc('bp_ql', simi=0.95, is_click=False):
            processing = True

        if not processing:
            processing = not self.changeTask(False)

        step_list = ["bp_ql", "gm", "gm_shanghui", "dh_bprw", "bp_bpwc"]

        count = 0
        while processing:
            for item in step_list:
                self.capture()
                if item == "bp_ql":
                    coor = self.match(item, simi=0.95)
                else:
                    coor = self.match(item)
                if coor:
                    count = 0
                    if item == 'gm' or item == "gm_shanghui":
                        sleep(0.5)
                        self.btn.l(coor)
                        res = self.smc(item, is_click=False)
                        if res:
                            self.btn.r()

                    elif item == "bp_bpwc":
                        processing = False
                        break

                    else:
                        self.btn.l(coor)

                    sleep(0.2)

                elif item == 'bp_ql':
                    self.btn.m(900, 300)
                    self.btn.v(1, 10)

                    sleep(1)

                    if self.smc('bp_ql'):
                        break
                    else:
                        count += 1

                    if count == 5:
                        complete = self.changeTask()
                        count = 0
                        if complete:
                            processing = False


if __name__ == "__main__":
    import win32gui
    from capture import CaptureScreen
    from match import Match
    from btn import Btn
    from smc import SMC
    from complex import Complex

    hwnd = win32gui.FindWindow(None, "梦幻西游：时空")
    screen = '0'
    capture = CaptureScreen(hwnd, screen)
    match = Match(screen)
    btn = Btn(hwnd)
    smc = SMC(capture, match, btn)

    adb = {
        'screen': screen,
        'hwnd': hwnd,
        'capture': capture,
        'match': match,
        'btn': btn,
        'smc': smc,
    }
    complex_task = Complex(adb)

    Bangpai(adb, complex_task.task_finished).start()
    # Bangpai(adb, complex_task.task_finished).check_in()