from time import sleep


class Baotu(object):

    def __init__(self, adb):
        for key, val in adb.items():
            self.__dict__[key] = val

    def has_cbt(self):
        while not self.smc('hd', is_click=False):
            self.btn.r()

        self.btn.hotkey("bb")

        self.smc('bb_zl')
        self.btn.m(720, 440)
        self.btn.v(1, 50)
        sleep(1)

        page = 1
        while True:
            has_cbt = self.smc('bb_cbt', is_click=False)
            if has_cbt:
                return has_cbt

            else:
                self.btn.m(700, 400)
                self.btn.v(-1, 6)
                page += 1
                if page == 6:
                    self.btn.r()
                    break

            sleep(0.2)

        return ()

    def dig(self):
        # 打开背包
        self.logger.info(f'挖宝开始')
        cbt_coor = self.has_cbt()

        if cbt_coor:
            self.logger.info(f'挖宝进行中')
            self.btn.l(cbt_coor)
            self.btn.l(cbt_coor)

            sleep(5)

            while cbt_coor:
                self.capture()
                is_hd = self.match('hd')
                coor = self.match('sy')

                if is_hd:
                    count = 0
                    while True:
                        coor = self.smc('sy', is_click=False)
                        if coor:
                            break
                        else:
                            count += 1

                        if count == 12:
                            cbt_coor = self.has_cbt()
                            break

                        sleep(5)

                    if coor and coor[0] + coor[2] < 920:
                        self.btn.l(coor)
                        sleep(4)
                        count = 0

        self.logger.info(f'挖宝完成')
        return 1

    def start(self):
        self.logger.info(f'宝图开始')
        while not self.smc('hd', is_click=False):
            self.btn.r()

        if self.task_finished('bt_wc'):
            self.logger.info(f'宝图完成')
            self.dig()
            return

        self.btn.hotkey("hd")
        self.smc("rchd", sleep_time=0.5)
        self.btn.m(590, 330)
        self.btn.v(1, 31)
        sleep(0.5)

        processing = self.smc('rw_bt', simi=0.95)

        if not processing:
            self.logger.info(f'宝图领取')
            for n in range(31):
                if n % 10 == 0:
                    self.capture()
                    tem_coor = self.match("hd_btrw") or self.match("hd_btrw1")
                    if tem_coor:
                        btn_coor = self.match(
                            "cj", screen="imgTem/hd_btrw") or self.match(
                                "cj", screen="imgTem/hd_btrw1")
                        new_coor = ((
                            tem_coor[0] + btn_coor[0],
                            tem_coor[1] + btn_coor[1],
                            btn_coor[2],
                            btn_coor[3],
                        ))
                        if btn_coor:
                            self.btn.l(new_coor)
                            processing = True
                            sleep(5)

                            count = 0
                            while True:
                                if self.smc('bt_ttwf'):
                                    sleep(0.5)
                                    self.btn.r()
                                    break
                                else:
                                    count += 1

                                sleep(2)

                                if count == 15:
                                    processing = False
                                    self.logger.info('退出宝图')
                                    return

                            break
                else:
                    self.btn.v(-1)

        self.btn.r()

        if processing:
            self.logger.info(f'宝图进行中')
            step_list = ['bt_cbthdwc', 'rw_bt']

            while processing:
                for item in step_list:
                    self.capture()
                    is_hd = self.match('hd')
                    if item == 'rw_bt':
                        coor = self.match(item, simi=0.9)
                    else:
                        coor = self.match(item)
                    if coor and is_hd:
                        if item == 'bt_cbthdwc':
                            processing = False
                            break

                        else:
                            self.btn.l(coor, min_x=800)
                            sleep(5)

                    elif item == 'rw_bt' and not coor and is_hd:
                        count = 0
                        while True:
                            is_hd = self.smc('hd', is_click=False)
                            if not is_hd:
                                count = 0
                            else:
                                count += 1

                            if count == 12:
                                processing = False
                                break

                            sleep(5)

        self.logger.info(f'宝图完成')
        self.dig()


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
        'name': "debug",
        'screen': screen,
        'hwnd': hwnd,
        'capture': capture,
        'match': match,
        'btn': btn,
        'smc': smc,
    }
    complex_task = Complex(adb)

    Baotu(adb, complex_task.task_finished).start()