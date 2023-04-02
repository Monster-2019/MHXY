from time import sleep


class Yunbiao(object):

    def __init__(self, adb):
        for key, val in adb.items():
            self.__dict__[key] = val
        if adb["print"]: 
            global print 
            print = adb["print"]

    def start(self):
        print(f'{self.name}开始运镖')
        while not self.smc('hd', is_click=False):
            self.btn.r()

        if self.task_finished('yb_wc'):
            print(f'{self.name}运镖已完成')
            self.btn.r()
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
                tem_coor = self.match('hd_yb1') or self.match('hd_yb')
                btn_coor = self.match('cj', screen='imgTem/hd_yb')
                if tem_coor and btn_coor:
                    new_coor = ((tem_coor[0] + btn_coor[0],
                                 tem_coor[1] + btn_coor[1], btn_coor[2],
                                 btn_coor[3]))
                    if btn_coor:
                        self.btn.l(new_coor)
                        processing = True
                        break

            else:
                self.btn.v(-1)

        count = 0
        step_list = ['yb_ys', 'qd']
        print(f'{self.name}运镖进行中')
        while processing:
            is_hd = self.smc('hd', is_click=False)
            if count >= 3 and is_hd:
                processing = False
                break

            for item in step_list:
                res = self.smc(item)
                if res and item == 'qd':
                    count += 1
                    sleep(20)

            sleep(1)

        print(f'{self.name}完成运镖')


if __name__ == '__main__':
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

    Yunbiao(adb, complex_task.task_finished).start()