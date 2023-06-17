from time import sleep



empty = {
    "name": "",
    "wc": "",
    "hd": "",
    "xz": "",
    "rw": "",
}

ecy = {
    "name": "二重影",
    "wc": "ecy_wc",
    "hd": "hd_ecy_pt",
    "xz": "fb_ecy_xz",
    "rw": "fb_ecy",
}

lyrm = {
    "name": "绿烟如梦",
    "wc": "lyrm_wc",
    "hd": "hd_lyrm_pt",
    "xz": "fb_lyrm_xz",
    "rw": "fb_lyrm",
}

lls = {
    "name": "琉璃碎",
    "wc": "lls_wc",
    "hd": "hd_lls_pt",
    "xz": "fb_lls_xz",
    "rw": "fb_lls",
}

jcx = {
    "name": "金禅心",
    "wc": "jcx_wc",
    "hd": "hd_jcx_pt",
    "xz": "fb_jcx_xz",
    "rw": "fb_jcx",
}


class FuBen(object):

    def __init__(self, adb):
        for key, val in adb.items():
            self.__dict__[key] = val
        self.fb_img = empty

    def leader(self, fb):
        while not self.smc('hd', is_click=False):
            self.btn.r()

        self.fb_img = eval(fb)
        self.fb_name = self.fb_img['name']
        self.logger.info(f'{self.fb_name}副本开始')

        complete = self.task_finished(self.fb_img['wc'])

        if complete:
            self.logger.info(f'{self.fb_name}副本已完成')
            return

        self.btn.hotkey('hd')
        self.smc('rchd', sleep_time=0.5)
        self.btn.m(590, 330)
        self.btn.v(1, 31)
        sleep(1)

        self.logger.info(f'{self.fb_name}副本领取')
        processing = False
        for n in range(31):
            if n % 10 == 0:
                self.capture()
                coor = self.match(self.fb_img["hd"])
                if coor:
                    tem_x, tem_y, tem_w, tem_h = coor
                    x, y, w, h = self.match("cj",
                                            screen="imgTem/" +
                                            self.fb_img["hd"])
                    new_coor = (tem_x + x, tem_y + y, w, h)
                    if x:
                        self.btn.l(new_coor, sleep_time=1)

                        # 去完成或继续任务
                        while not processing:
                            for item in ['fb_xzfb', self.fb_img["xz"]]:
                                r = self.smc(item, sleep_time=1)
                                if r and item == self.fb_img["xz"]:
                                    btn_coor = self.match('fb_jr',
                                                          screen='imgTem/' +
                                                          self.fb_img["xz"])
                                    if btn_coor != 0:
                                        new_coor = ((
                                            r[0] + btn_coor[0],
                                            r[1] + btn_coor[1],
                                            btn_coor[2],
                                            btn_coor[3],
                                        ))
                                        self.btn.l(new_coor, sleep_time=3)

                                        r = self.smc(self.fb_img["rw"],
                                                     simi=0.95,
                                                     is_click=False)
                                        if r:
                                            self.logger.info(
                                                f'{self.fb_name}副本已领取')
                                            processing = True
                                            break

                        break
            else:
                self.btn.v(-1)

        step_list = [
            'zd_qx', 'sb', 'hd', 'fb_tgjq', self.fb_img["rw"], 'dh', 'djjx'
        ]

        self.logger.info(f'{self.fb_name}副本进行中')
        while processing:
            for item in step_list:
                if item == self.fb_img["rw"] or item == 'dh':
                    coor = self.smc(item, simi=0.9, is_click=False)
                else:
                    coor = self.smc(item, is_click=False)
                if coor:
                    if item == 'zd_qx':
                        sleep(3)
                        break

                    elif item == self.fb_img["rw"]:
                        if coor[0] > 800 and coor[1] < 240:
                            self.btn.l(coor, sleep_time=3)

                    elif item == 'fb_tgjq':
                        self.btn.l(coor)
                        self.btn.l(coor)

                    elif item == 'djjx':
                        while True:
                            res = self.smc('djjx', sleep_time=0.3)
                            if not res:
                                break

                    elif item == 'dh':
                        while True:
                            self.capture()
                            coor = self.match('dh', simi=0.9)
                            if coor:
                                new_coor = (coor[0] + 14, coor[1] + 64, 247,
                                            41)
                                self.btn.l(new_coor)
                                sleep(0.3)
                            else:
                                break

                    elif item == 'sb':
                        while True:
                            self.smc('sb', sleep_time=0.5)
                            self.btn.hotkey('dt', sleep_time=1)
                            self.smc('dt_cac', sleep_time=2)
                            res = self.smc('hd', is_click=False)
                            if res:
                                break
                        break

                    elif item == 'hd':
                        sleep(2)
                        res = self.smc('hd')
                        if res:
                            processing = False
                            break

        self.logger.info(f'{self.fb_name}副本完成')
        return 1

    def palyer(self):
        pass


if __name__ == "__main__":
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
    adb["task_finished"] = complex_task.task_finished

    FuBen(adb).leader('lls')