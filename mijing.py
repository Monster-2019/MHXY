from time import sleep


class Mijing:

    def __init__(self, adb, task_finished):
        for key, val in adb.items():
            self.__dict__[key] = val
        self.task_finished = task_finished

    def start(self):
        while not self.smc('hd', is_click=False):
            self.btn.r()

        if self.task_finished('mj_wc'):
            return

        self.btn.hotkey("hd")
        self.smc("rchd", sleep_time=0.5)
        self.btn.m(590, 330)
        self.btn.v(1, 31)
        sleep(0.5)

        for n in range(31):
            if n % 10 == 0:
                self.capture()
                tem_coor = self.match('hd_mjxy') or self.match('hd_mjxy1')
                btn_coor = self.match('cj',
                                      screen='imgTem/hd_mjxy') or self.match(
                                          'cj', screen='imgTem/hd_mjxy1')
                if tem_coor and btn_coor:
                    new_coor = ((tem_coor[0] + btn_coor[0],
                                 tem_coor[1] + btn_coor[1], btn_coor[2],
                                 btn_coor[3]))
                    self.btn.l(new_coor, sleep_time=3)
                    break

            else:
                self.btn.v(-1)

        join_list = ['mj_mjxy', 'mj_jr', 'qd', 'mj_one', 'mj_tz']
        # 'mj_mrh', 'mj_yjf', 'mj_esg',

        join = False
        while not join:
            for item in join_list:
                coor = self.smc(item, is_click=False)
                if coor:
                    if item == 'mj_one':
                        self.btn.l(
                            (coor[0] + 46, coor[1] - 60, coor[2], coor[3]))

                    elif item == 'mj_jr':
                        self.btn.l(coor, max_x=500)

                    elif item == 'mj_tz':
                        self.btn.l(coor)
                        join = True
                        break

                    else:
                        self.btn.l(coor)

                    sleep(0.5)

        step_list = ['sb', 'mj_tg', 'mj_mjxyrw', 'mj_lb', 'mj_jrzd', 'mj_gb']
        # # , 'mj_lq', 'mj_gb'

        sleep(3)
        processing = True

        while processing:
            for item in step_list:
                is_hd = self.smc('hd', is_click=False)
                if is_hd:
                    processing = False
                    break

                coor = self.match(item)

                if coor:
                    if item == 'sb' or item == 'mj_tg':
                        self.btn.l(coor)
                        # self.btn.l(((520, 380), (10, 10)))
                        processing = False
                        break

                    elif item == 'mj_mjxyrw':
                        self.btn.l(coor, sleep_time=2, min_x=700)

                    else:
                        self.btn.l(coor, min_x=350)

                    sleep(0.1)
                else:
                    sleep(0.2)

        while not self.smc('hd', is_click=False):
            self.smc('mj_lk')


if __name__ == '__main__':
    import win32gui
    from capture import CaptureScreen
    from match import Match
    from btn import Btn
    from smc import SMC
    from complex import Complex

    hwnd = win32gui.FindWindow(None, "《梦幻西游》手游")
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

    Mijing(adb, complex_task.task_finished).start()