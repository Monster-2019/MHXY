from time import sleep

from loguru import logger

COUNT = 2


class Zhuogui(object):

    def __init__(self, adb):
        for key, val in adb.items():
            self.__dict__[key] = val
        if adb["print"]:
            global print
            print = adb["print"]

    def leader(self):
        while not self.smc('hd', is_click=False):
            self.btn.r()

        complete = self.task_finished('zg_wc')

        if complete:
            return

        self.btn.hotkey('hd')
        self.smc('rchd', sleep_time=0.5)
        self.btn.m(590, 330)
        self.btn.v(1, 31)
        sleep(0.5)

        for n in range(31):
            if n % 10 == 0:
                self.capture()
                tem_x, tem_y, tem_w, tem_h = self.match('hd_zgrw')
                if tem_x:
                    x, y, w, h = self.match('cj', screen='imgTem/hd_zgrw')
                    new_coor = (tem_x + x, tem_y + y, w, h)
                    if x:
                        self.btn.l(new_coor)
                        break

            else:
                self.btn.v(-1)

        self.loop(COUNT)

        logger.info(f"捉鬼任务结束")

    def player(self):
        pass

    def loop(self, count=99):
        step_list = ['zg_zgrw', 'zg_zg', 'zg_zgwc']
        cur_count = 0
        while cur_count < count:
            for item in step_list:
                self.capture()
                isHd = self.match('hd')
                if item == 'zg_zg':
                    coor = self.match(item, simi=0.9)
                else:
                    coor = self.match(item)

                if coor and item == 'zg_zgwc':
                    if cur_count < count:
                        self.smc('qd')
                    else:
                        result = self.smc('qx')
                        if result:
                            logger.info('完成')
                            break

                elif coor and item == 'zg_zgrw':
                    self.btn.l(coor)
                    sleep(2)
                    self.btn.r()
                    cur_count += 1
                    print(f'开始刷第{cur_count}轮鬼')

                elif isHd and not coor and item == 'zg_zg':
                    self.btn.m(900, 300)
                    self.btn.v(1, 10)

                else:
                    self.btn.l(coor)

                sleep(0.1)

        return 1


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

    Zhuogui(adb, complex_task.task_finished).loop()
    # Zhuogui().leader()