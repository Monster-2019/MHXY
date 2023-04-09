from time import sleep


class Gongfang(object):

    def __init__(self, adb):
        for key, val in adb.items():
            self.__dict__[key] = val

    def kaogu(self):
        self.logger.info('考古开始')
        self.btn.hotkey("bb", sleep_time=1)
        self.btn.m(707, 406)
        self.btn.v(1, 30)

        # cz = 'bb_fjc'
        cz = "bb_lyc"
        for i in range(6):
            has_cz = self.smc(cz, is_click=False)
            if has_cz:
                self.logger.info('考古进行中')
                self.btn.l(has_cz)
                self.btn.l(has_cz)
                sleep(1)
                break
            else:
                self.btn.m(707, 406)
                self.btn.v(-1, 13)
                sleep(0.3)

            if i == 5:
                self.logger.info('没有铲子，考古结束')
                self.btn.r()
                return False

        while True:
            r = self.smc("kg_ks", sleep_time=1)
            if r:
                self.btn.r()
                self.btn.r()
                break

        self.logger.info('已考古0次')
        for i in range(10):
            while True:
                coor = self.smc('wj', is_click=False)
                if coor:
                    if coor[0] + coor[2] < 920:
                        self.logger.info(f'已考古{i + 1}次')
                        self.btn.l(coor, sleep_time=3)
                        break

        self.logger.info('考古结束')
        return True

    def sell(self):
        self.logger.info('考古售卖开始')
        self.btn.hotkey('bb')

        for i in range(6):
            has_gd = self.smc('bb_gf', is_click=False)
            if has_gd:
                self.logger.info('考古售卖进行中')
                self.btn.l(has_gd)
                self.btn.l(has_gd)
                sleep(0.5)
                self.btn.r()
                break
            else:
                self.btn.m(707, 406)
                self.btn.v(-1, 13)
                sleep(0.3)

            if i == 5:
                self.logger.info('没有古董，售卖结束')
                self.btn.r()
                return False

        step_list = ["kg_zp", "kg_sm", "kg_smwc"]

        self.logger.info('考古正在售卖')
        sell_status = False
        while not sell_status:
            for item in step_list:
                r = self.smc(item)
                if r != 0 and (item == "kg_zp" or item == "kg_smwc"):
                    sell_status = True
                    self.btn.r()
                    self.btn.r()
                    break

        self.logger.info('考古售卖完成')

        return True

    def start(self):
        self.logger.info(f'工坊开始')
        while not self.smc('hd', is_click=False):
            self.btn.r()

        processing = self.smc('rw_kg', is_click=False, simi=0.9) or self.smc('rw_gf', is_click=False, simi=0.9)

        if not processing:
            if self.task_finished('gf_wc', 'jjxx'):
                self.logger.info(f'工坊已完成')
                self.btn.r()
                return

            self.logger.info(f'工坊领取中')

            self.btn.hotkey("hd")
            self.smc("jjxx", sleep_time=0.5)
            self.btn.m(590, 330)
            self.btn.v(1, 31)
            sleep(0.5)

            for n in range(31):
                if n % 10 == 0:
                    sleep(1)
                    self.capture()
                    tem_coor = self.match("hd_gfrw")
                    btn_coor = self.match("cj", screen="imgTem/hd_gfrw")
                    if tem_coor and btn_coor:
                        new_coor = ((tem_coor[0] + btn_coor[0],
                                     tem_coor[1] + btn_coor[1], btn_coor[2],
                                     btn_coor[3]))
                        if btn_coor:
                            self.btn.l(new_coor)
                            processing = True

                            while True:
                                r = self.smc("gf_lqrw")
                                sleep(0.5)
                                if r:
                                    self.logger.info(f'工坊已领取')
                                    break

                            break

                else:
                    self.btn.v(-1)

        step_list = [
            "rw_kg",
            "rw_gf",
            "gf_xz",
            "dh",
            "gfnot",
            "gfgm",
            "djjx",
            "sy",
            "sj",
        ]

        count = 0
        if processing:
            self.logger.info(f'工坊进行中')
            while processing:
                for item in step_list:
                    self.capture()
                    is_hd = self.match('hd')
                    if item == 'rw_kg' or item == 'rw_gf' or item == 'dh':
                        coor = self.match(item, simi=0.9)
                    else:
                        coor = self.match(item)
                    if coor:
                        print(item, coor)
                        if item == 'rw_kg' or item == 'rw_gf':
                            self.btn.l(coor, min_x=800, min_y=150)
                            sleep(0.5)

                        elif item == "dh":
                            while True:
                                self.capture()
                                coor = self.match(item, simi=0.9)
                                if coor:
                                    new_coor = ((coor[0], coor[1] + 69, 87,
                                                 22))
                                    self.btn.l(new_coor)
                                    sleep(0.3)
                                else:
                                    break

                        elif item == "djjx":
                            while True:
                                res = self.smc("djjx", sleep_time=0.3)
                                if res == 0:
                                    break

                        elif item == "gfgm":
                            sleep(0.5)
                            self.btn.l(coor)
                            res = self.smc("gm_sb", is_click=False)
                            if res:
                                new_coor = ((308, 245, 294, 75))
                                self.btn.l(new_coor)
                                self.btn.r()
                                self.btn.r()

                        elif item == "sy":
                            if (coor[0] + coor[2]) < 920:
                                self.btn.l(coor)

                        elif item == "gfnot":
                            self.btn.r()
                            processing = False
                            break

                        else:
                            self.btn.l(coor, min_x=300)

                    else:
                        if item == "rw_kg" and is_hd:
                            self.btn.m(900, 300)
                            self.btn.v(-1, 10)
                            sleep(0.5)

                            if self.smc('rw_kg', simi=0.9, min_x=800) or self.smc('rw_gf', simi=0.9):
                                count = 0
                                break
                            else:
                                count += 1

                            if count == 5:
                                self.logger.info(f'工坊完成')
                                processing = False
                                break

                            sleep(2)

                    sleep(1 / len(step_list))

        has_gd = self.kaogu()
        if has_gd:
            self.sell()


if __name__ == "__main__":
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

    Gongfang(adb).start()
