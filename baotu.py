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
        sleep(1)
        # 打开背包
        self.logger.info(f'挖宝开始')
        cbt_coor = self.has_cbt()

        if cbt_coor:
            self.logger.info(f'挖宝进行中')
            self.btn.l(cbt_coor)
            self.btn.l(cbt_coor)

            sleep(5)

            while cbt_coor:
                is_hd = self.smc('hd', is_click=False)

                if is_hd:
                    for i in range(30):
                        coor = self.smc('sy', is_click=False)
                        if coor and coor[0] + coor[2] < 920:
                            self.btn.l(coor)
                            sleep(4)
                            break
                        sleep(1)
                    
                    if i == 29:
                        cbt_coor = self.has_cbt()

                sleep(3)

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

        processing = self.smc('rw_bt', simi=0.95)

        if not processing:
            self.logger.info(f'宝图领取')

            self.btn.hotkey("hd")
            self.smc("rchd", sleep_time=0.5)
            self.btn.m(590, 330)
            self.btn.v(1, 31)
            sleep(0.5)

            for n in range(31):
                if n % 10 == 0:
                    self.capture()
                    tem_coor = self.match("hd_btrw")
                    btn_coor = self.match("cj", screen="imgTem/hd_btrw")
                    if tem_coor and btn_coor:
                        new_coor = ((
                            tem_coor[0] + btn_coor[0],
                            tem_coor[1] + btn_coor[1],
                            btn_coor[2],
                            btn_coor[3],
                        ))
                        self.btn.l(new_coor)

                        sleep(5)

                        while True:
                            if self.smc('bt_ttwf'):
                                sleep(1)
                                self.btn.r()
                                sleep(1)
                                self.smc('rw_bt')
                                processing = True
                                break

                            sleep(5)

                        break
                else:
                    self.btn.v(-1)

        if processing:
            self.logger.info(f'宝图进行中')

            while processing:
                is_hd = self.smc('hd', is_click=False)

                if is_hd:
                    for i in range(6):
                        has_rw = self.smc('rw_bt', simi=0.95, is_click=False)
                        if has_rw:
                            break
                        sleep(5)
                    
                    if i == 5:
                        processing = False

                sleep(3)

        self.logger.info(f'宝图完成')
        self.dig()


if __name__ == '__main__':
    import win32gui
    from loguru import logger

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

    Baotu(adb).start()