from time import sleep


class Shimen(object):

    def __init__(self, adb):
        for key, val in adb.items():
            self.__dict__[key] = val

    def start(self):
        self.logger.info(f'师门开始')
        while not self.smc('hd', is_click=False):
            self.btn.r()

        while True:
            if not self.smc("sygb", sleep_time=0.5):
                break

        if self.task_finished('sm_wc'):
            self.logger.info(f'师门完成')
            self.btn.r()
            return

        # self.btn.hotkey('zz', sleep_time=1)
        # self.btn.l('zr1', sleep_time=0.5)
        # self.btn.r()

        self.btn.hotkey("hd")
        self.smc("rchd", sleep_time=0.5)
        self.btn.m(590, 330)
        self.btn.v(1, 31)

        processing = self.smc('sm_sm')

        if not processing:
            self.logger.info(f'师门领取')
            for n in range(31):
                if n % 10 == 0:
                    self.capture()
                    tem_coor = self.match("hd_smrw")
                    btn_coor = self.match("cj", screen="imgTem/hd_smrw")
                    if tem_coor and btn_coor:
                        new_coor = ((tem_coor[0] + btn_coor[0],
                                     tem_coor[1] + btn_coor[1], btn_coor[2],
                                     btn_coor[3]))
                        self.btn.l(new_coor, sleep_time=1)

                        is_not_auto = self.smc('sm_zd', is_click=False, simi=0.999)

                        if is_not_auto:
                            self.btn.l((is_not_auto[0], is_not_auto[1], 16, 16))

                        # 去完成或继续任务
                        while True:
                            self.capture()
                            btn_coor = self.match("sm_qwc") or self.match(
                                "sm_jxrw")
                            if btn_coor:
                                self.btn.l(btn_coor, sleep_time=1)
                                processing = True
                                break

                        break
                else:
                    self.btn.v(-1)

        if processing:
            self.logger.info(f'师门进行中')
            while True:
                if self.smc("sm_wc_qd"):
                    break
                sleep(3)

            self.btn.r()
            sleep(1)
            self.btn.r()

            while True:
                coor = self.smc('sy')
                if not coor:
                    break

        self.logger.info(f'师门完成')
        return 1


if __name__ == "__main__":
    import win32gui
    

    from btn import Btn
    from capture import CaptureScreen
    from complex import Complex
    from match import Match
    from smc import SMC

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

    Shimen(adb).start()
