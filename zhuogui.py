from time import sleep

from loguru import logger

COUNT = 2


class Zhuogui(object):

    def __init__(self, adb):
        for key, val in adb.items():
            self.__dict__[key] = val

    def leader(self):
        self.logger.info(f"捉鬼开始")
        while not self.smc('hd', is_click=False):
            self.btn.r()

        if self.task_finished('zg_wc'):
            self.logger.info(f"捉鬼完成")
            self.btn.r()
            return

        self.btn.hotkey('hd')
        self.smc('rchd', sleep_time=0.5)
        self.btn.m(590, 330)
        self.btn.v(1, 31)
        sleep(0.5)

        self.logger.info(f"捉鬼领取")
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

        self.logger.info(f"捉鬼完成")

    def player(self):
        pass

    def loop(self, count=99):
        self.logger.info(f"捉鬼进行中")
        step_list = ['zg_zgrw', 'zg_zg', 'zg_zgwc']
        cur_count = 0
        while cur_count <= count:
            for item in step_list:
                self.capture()
                is_hd = self.match('hd')
                if item == 'zg_zg':
                    coor = self.match(item, simi=0.9)
                else:
                    coor = self.match(item)

                if coor:
                    if item == 'zg_zg':
                        self.btn.l(coor, min_x=380)

                    if item == 'zg_zgwc':
                        self.logger.info(f'结束第{cur_count}轮鬼')
                        if cur_count < count:
                            self.smc('qd')
                        else:
                            result = self.smc('qx')
                            if result:
                                cur_count = 3
                                break

                    if item == 'zg_zgrw':
                        self.btn.l(coor)
                        sleep(2)
                        self.btn.r()
                        cur_count += 1
                        self.logger.info(f'开始刷第{cur_count}轮鬼')

                sleep(1 / len(step_list))

        return 1


if __name__ == '__main__':
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
    }
    complex_task = Complex(adb)

    Zhuogui(adb, complex_task.task_finished).loop()
    # Zhuogui().leader()