from time import sleep


class Mijing:

    def __init__(self, adb):
        for key, val in adb.items():
            self.__dict__[key] = val

    def start(self):
        self.logger.info(f'秘境开始')
        while not self.smc('hd', is_click=False):
            self.btn.r()

        if self.task_finished('mj_wc'):
            self.logger.info(f"秘境已完成")
            self.btn.r()
            return

        self.btn.hotkey("hd")
        self.smc("rchd", sleep_time=0.5)
        self.btn.m(590, 330)
        self.btn.v(1, 31)
        sleep(1)

        self.logger.info(f'秘境领取')
        for n in range(31):
            if n % 10 == 0:
                self.capture()
                tem_coor = self.match('hd_mjxy')
                btn_coor = self.match('cj', screen='imgTem/hd_mjxy')
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
        count = 0

        while not join:
            for item in join_list:
                coor = self.smc(item, is_click=False)
                if coor:
                    count = 0
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

                    sleep(1)

                elif item == 'mj_one':
                    count += 1

                if count == 5:
                    self.logger.info(f'秘境已经挑战过')
                    self.btn.r()
                    return

                sleep(1 / len(join_list))

        step_list = ['mj_jrzd', 'mj_lb', 'mj_gb']
        # # , 'mj_lq', 'mj_gb'

        processing = True
        self.logger.info(f'秘境进行中')

        sleep(3)

        self.smc('mj_mjxyrw')

        while processing:
            is_end = self.smc('sb') or self.smc('mj_tg') or self.smc('hd')
            if is_end:
                processing = False
                break

            is_lk = self.smc('mj_lk', is_click=False)
            if not is_lk:
                sleep(3)
                continue
            
            for item in step_list:
                coor = self.smc(item, is_click=False)

                if coor:
                    if item == 'mj_lb':
                        self.btn.l(coor)
                        sleep(3)
                        self.btn.r()
                        sleep(1)
                        self.smc('mj_mjxyrw')

                    else:
                        self.btn.l(coor)

                sleep(1)
            sleep(3)

        while not self.smc('hd', is_click=False):
            self.smc('mj_lk')
            sleep(1)

        self.logger.info(f'秘境完成')
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
        'logger': logger
    }
    complex_task = Complex(adb)
    adb['task_finished'] = complex_task.task_finished
    adb['is_still'] = complex_task.is_still

    Mijing(adb).start()