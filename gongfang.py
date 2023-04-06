from time import sleep


class Gongfang(object):

    def __init__(self, adb):
        for key, val in adb.items():
            self.__dict__[key] = val

    def kaogu(self):
        self.btn.hotkey("bb", sleep_time=1)
        self.btn.m(707, 406)
        self.btn.v(1, 30)

        page = 0
        # cz = 'bb_fjc'
        cz = "bb_lyc"
        while True:
            has_cz = self.smc(cz)
            if has_cz:
                self.btn.l(has_cz)
                self.btn.l(has_cz)
                sleep(1)
                break

            else:
                page += 1
                self.btn.m(707, 406)
                self.btn.v(-1, 13)
                sleep(0.3)
                if page == 6:
                    self.btn.r()
                    return False

        while True:
            r = self.smc("kg_ks", sleep_time=1)
            if r:
                self.btn.r()
                self.btn.r()
                break

        for i in range(10):
            while True:
                coor = self.smc('wj', is_click=False)
                if coor:
                    if coor[0] + coor[1] < 920:
                        self.btn.l(coor, sleep_time=3)
                        break

        return True

    def sell(self):
        self.btn.hotkey('bb')

        page = 0
        while True:
            has_gd = self.smc('bb_gd')
            if has_gd:
                self.btn.l(has_gd)
                self.btn.l(has_gd)
                sleep(1)
                break

            else:
                page += 1
                self.btn.m(707, 406)
                self.btn.v(-1, 13)
                sleep(0.3)
                if page == 6:
                    self.btn.r()
                    return False

        while True:
            r = self.smc('kg_gdsm')
            if r:
                break

        step_list = ["kg_zp", "kg_sm", "kg_smwc"]

        sell_status = False
        while not sell_status:
            for item in step_list:
                r = self.smc(item)
                if r != 0 and (item == "kg_zp" or item == "kg_smwc"):
                    sell_status = True
                    self.btn.r()
                    self.btn.r()
                    break

    def start(self):
        while not self.smc('hd', is_click=False):
            self.btn.r()

        processing = self.smc('rw_kg', is_click=False, simi=0.95)

        if not processing:
            if self.task_finished('gf_wc', 'jjxx'):
                return

            self.btn.hotkey("hd")
            self.smc("jjxx", sleep_time=0.5)
            self.btn.m(590, 330)
            self.btn.v(1, 31)
            sleep(0.5)

            processing = self.smc('rw_kg', simi=0.95)

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
                                sleep(1)
                                if r:
                                    break

                            break

                else:
                    self.btn.v(-1)

        step_list = [
            "rw_kg",
            "gf_xz",
            "dh",
            "dhda",
            "gfnot",
            "gfgm",
            "djjx",
            "sy",
            "sj",
        ]

        while processing:
            for item in step_list:
                self.capture()
                is_hd = self.match('hd')
                if item == 'rw_kg' or item == 'dh':
                    coor = self.match(item, simi=0.95)
                else:
                    coor = self.match(item)
                if coor:
                    if item == 'rw_kg':
                        if coor[0] > 780:
                            self.btn.l(coor)
                        else:
                            self.btn.r()
                            self.btn.m(157, 686)
                            self.btn.v(-1, 10)

                    elif item == "dh" or item == "dhda":
                        while True:
                            self.capture()
                            coor = self.match(item, simi=0.95)
                            if coor:
                                new_coor = ((coor[0], coor[1] + 69, 87, 22))
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

                    sleep(0.1)

                else:
                    if item == "rw_kg" and is_hd:
                        count = 0
                        while True:
                            complete = self.smc('rw_kg',
                                                simi=0.95,
                                                is_click=False)
                            if complete:
                                count = 0
                            else:
                                count += 1

                            if count == 12:
                                processing = False
                                break

                            sleep(5)

        res = self.kaogu()
        if res:
            self.sell()


if __name__ == "__main__":
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

    Gongfang(adb, complex_task.task_finished).start()
