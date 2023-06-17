from time import sleep
from datetime import datetime


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
                    week = datetime.now().isoweekday()
                    if week == 2:
                        self.smc('bp_lqfh')
                        sleep(1)
                        self.smc('bp_lq')
                        sleep(1)
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
            sleep(1)
            self.logger.info(f'已放弃帮派')

        self.btn.hotkey("hd")
        self.smc("rchd", sleep_time=0.5)
        self.btn.m(590, 330)
        self.btn.v(1, 31)
        sleep(1)

        # 匹配帮派任务
        self.logger.info(f'帮派领取中')
        for n in range(31):
            if n % 10 == 0:
                self.capture()
                complete = self.match('bp_wc', simi=0.995)
                if complete:
                    return True
                tem_coor = self.match("hd_bprw", simi=0.995)
                btn_coor = self.match('cj',
                                      screen='imgTem/hd_bprw',
                                      simi=0.995)
                if tem_coor and btn_coor:
                    new_coor = ((tem_coor[0] + btn_coor[0],
                                 tem_coor[1] + btn_coor[1], btn_coor[2],
                                 btn_coor[3]))
                    self.btn.l(new_coor)
                    sleep(1)

                    while True:
                        if self.smc('bp_lqrw'):
                            self.logger.info(f'帮派已更换')
                            sleep(1)
                            self.btn.r()
                            return False
                        sleep(1)

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
        sleep(1)

        if self.smc.smc('bp_ql', simi=0.95):
            self.logger.info(f'帮派已领取')
            processing = True

        if not processing:
            processing = not self.changeTask(False)

        self.logger.info(f'帮派进行中')
        step_list = ["gm", "gm_1", "dh_bprw", "bp_bpwc", "qltzg"]

        count = 0
        while processing:
            # is_hd = self.smc('hd', is_click=False)
            # if is_hd:
            #     for i in range(5):
            #         has_ql = self.smc('bp_ql', simi=0.95, is_click=False)
            #         if has_ql:
            #             break
            #         sleep(2)
                
            #     if i == 4:
            #         processing = not self.changeTask()
            for item in step_list:
                self.capture()
                coor = self.match(item)
                if coor:
                    count = 0
                    if item == 'gm' or item == "gm_1":
                        sleep(1)
                        self.btn.l(coor)
                        res = self.smc(item, is_click=False)
                        if res:
                            self.btn.r()

                    elif item == "bp_bpwc":
                        processing = False
                        break

                    elif item == 'qltzg':
                        self.smc('bp_ql', simi=0.95)

                    else:
                        self.btn.l(coor)

                    sleep(0.2)

                sleep(1 / len(step_list))
            else:
                count += 1
                print('count', count)
                if count < 15:
                    continue
            
            count = 0
            is_still = self.is_still()
            if is_still:
                sleep(1)
                has_ql = self.smc('bp_ql', simi=0.95)
                if not has_ql:
                    while True:
                        processing = not self.changeTask()
                        has_ql = self.smc('bp_ql', simi=0.95, is_click=False)
                        if not processing or has_ql:
                            break
                        sleep(1)


        self.logger.info(f'帮派完成')

        return 1
    
if __name__ == "__main__":
    import win32gui
    

    from btn import Btn
    from capture import CaptureScreen
    from complex import Complex
    from match import Match
    from smc import SMC
    import logging

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
        'logger': logging
    }
    complex_task = Complex(adb)
    adb['task_finished'] = complex_task.task_finished
    adb['is_still'] = complex_task.is_still

    Bangpai(adb).start()
    # Bangpai(adb, complex_task.task_finished).check_in()