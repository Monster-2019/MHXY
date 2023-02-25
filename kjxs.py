from time import sleep


class KJ(object):

    def __init__(self, adb, task_finished):
        for key, val in adb.items():
            self.__dict__[key] = val
        self.task_finished = task_finished

    def start(self):
        while not self.smc('hd', is_click=False):
            self.btn.r()

        if self.task_finished('kj_wc'):
            return

        self.btn.hotkey("hd")
        self.smc("rchd", sleep_time=0.5)
        self.btn.m(590, 330)
        self.btn.v(1, 31)
        sleep(0.5)

        processing = False

        for n in range(31):
            if n % 10 == 0:
                self.capture()
                tem_coor = self.match('hd_kjxs') or self.match('hd_kjxs2')
                if tem_coor:
                    btn_coor = self.match(
                        'cj', screen='imgTem/hd_kjxs') or self.match(
                            'cj', screen='imgTem/hd_kjxs2')
                    new_coor = ((tem_coor[0] + btn_coor[0],
                                 tem_coor[1] + btn_coor[1], btn_coor[2],
                                 btn_coor[3]))
                    if btn_coor:
                        self.btn.l(new_coor, sleep_time=1)
                        while True:
                            if self.smc('kj_start', is_click=False):
                                processing = True
                                break

            else:
                self.btn.v(-1)

        if processing:
            while processing:
                res = self.smc('kj_dw', is_click=False)
                if res:
                    self.btn.r()
                    processing = False
                    break
                else:
                    self.btn.l((375, 390, 250, 50), sleep_time=0.5)


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
    KJ(adb, complex_task.task_finished).start()