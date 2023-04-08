from time import sleep


class Bangpai(object):

    def __init__(self, adb):
        for key, val in adb.items():
            self.__dict__[key] = val

    def check_in(self):
        self.logger.info(f'签到开始')
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

                elif not coor and item == 'bp_fl':
                    self.btn.hotkey('bp')
                    continue

                sleep(1 / len(step_list))

        self.logger.info(f'签到完成')

    def changeTask(self, has_task=True):
        step_list = ["rw_dqrw", "rw_cgrw", "rw_bprw", "rw_fqrw", "qd"]

        if has_task:
            self.logger.info(f'帮派已领取，非青龙')
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
            self.logger.info(f'已放弃帮派')

        self.btn.hotkey("hd")
        self.smc("rchd", sleep_time=0.5)
        self.btn.m(590, 330)
        self.btn.v(1, 31)
        sleep(0.5)

        # 匹配帮派任务
        self.logger.info(f'帮派领取中')
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
                            self.logger.info(f'帮派已更换')
                            return False
                        sleep(0.5)

            else:
                self.btn.v(-1)

        self.logger.info(f'帮派已完成')
        return True

    def start(self):
        self.logger.info(f'帮派开始')
        processing = False

        while not self.smc('hd', is_click=False):
            self.btn.r()

        if self.task_finished('bp_wc'):
            self.logger.info(f'帮派完成')
            self.btn.r()
            return

        self.btn.m(900, 300)
        self.btn.v(1, 10)
        sleep(0.5)

        if self.smc.smc('bp_ql', simi=0.95, is_click=False):
            self.logger.info(f'帮派已领取')
            processing = True

        if not processing:
            processing = not self.changeTask(False)

        if processing:
            self.logger.info(f'帮派进行中')
            step_list = ["bp_ql", "gm", "gm_shanghui", "dh_bprw", "bp_bpwc"]

            count = 0
            while processing:
                for item in step_list:
                    self.capture()
                    is_hd = self.match('hd')
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

                    else:
                        if item == 'bp_ql' and is_hd:
                            count += 1

                            if count == 10:
                                self.logger.info(f'非青龙，切换任务')
                                while True:
                                    complete = self.changeTask()
                                    sleep(0.5)
                                    self.btn.r()
                                    print(complete)
                                    sleep(0.5)
                                    if complete:
                                        processing = False
                                        break
                                    elif self.smc('bp_ql', simi=0.95):
                                        break
                                    
                                    sleep(0.5)

                    sleep(1 / len(step_list))

        self.logger.info(f'帮派完成')

        return 1


if __name__ == "__main__":
    import win32gui
    from capture import CaptureScreen
    from match import Match
    from btn import Btn
    from smc import SMC
    from complex import Complex
    from loguru import logger

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
        'logger': logger
    }
    complex_task = Complex(adb)
    adb['task_finished'] = complex_task.task_finished

    Bangpai(adb).start()
    # Bangpai(adb, complex_task.task_finished).check_in()