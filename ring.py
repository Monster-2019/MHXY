from time import sleep


class Ring(object):

    def __init__(self, adb):
        for key, val in adb.items():
            self.__dict__[key] = val
        if adb["print"]: 
            global print 
            print = adb["print"]

    def start(self):
        print(f"开始经验链")

        while not self.smc('hd', is_click=False):
            self.btn.r()

        processing = self.smc('rw_jyl', simi=0.9, is_click=False)
        print(processing)

        if not processing:
            if self.task_finished('jyl_wc'):
                print('经验链完成')
                return

        print(f"经验链进行中")

        if not processing:
            self.btn.hotkey("hd")
            self.smc("rchd", sleep_time=0.5)
            self.btn.m(590, 330)
            self.btn.v(1, 31)

            for n in range(31):
                if n % 10 == 0:
                    self.capture()
                    tem_coor = self.match("hd_jyl")
                    btn_coor = self.match("cj", screen="imgTem/hd_jyl")
                    if tem_coor and btn_coor:
                        new_coor = ((tem_coor[0] + btn_coor[0],
                                     tem_coor[1] + btn_coor[1], btn_coor[2],
                                     btn_coor[3]))
                        self.btn.l(new_coor, sleep_time=5)

                        # 去完成或继续任务
                        while True:
                            step_list = ["dh_jyl", "dh_lqjyl", "qd_1"]

                            for item in step_list:
                                while True:
                                    r = self.smc(item, sleep_time=0.5)
                                    if r:
                                        break

                            processing = True

                else:
                    self.btn.v(-1)

        if not processing:
            print('未找到任务')
            return

        step_list = ["rw_jyl_wc", "rw_jyl", "gm", "gm_1", 'btgm', "dh", "sj"]

        count = 0
        while processing:
            for item in step_list:
                self.capture()
                is_hd = self.match('hd')
                if item == 'dh' or item == 'rw_jyl':
                    coor = self.match(item, simi=0.95)
                else:
                    coor = self.match(item)
                if coor:
                    count = 0
                    if item == 'rw_jyl_wc':
                        processing = False
                        break

                    elif item == "dh":
                        while True:
                            coor = self.smc(item, is_click=False)
                            if coor:
                                new_coor = ((coor[0], coor[1] + 69, 87, 22))
                                self.btn.l(new_coor)
                                sleep(0.3)
                            else:
                                break

                        sleep(0.5)

                    elif item == "btgm":
                        sleep(2)
                        res = self.smc('bt_sj') or self.smc(
                            'bt_jlh') or self.smc('bt_mgh')
                        if res:
                            print("高价物品，手动处理")
                            return

                            # self.btn.hotkey('gj')

                            # while True:
                            #     self.B.DBtn((900, 350, 130, 350))
                            #     sleep(1)
                            #     res = self.smc('gj_xysm')
                            #     if res:
                            #         break

                            # start = int(time.time())
                            # end = int(time.time())
                            # while end - start < 1200:
                            #     end = int(time.time())
                            #     res = self.smc('sj')
                            #     if res:
                            #         CS = False
                            #         break
                            #     sleep(1)

                            # self.btn.l(((500, 450), (2, 2)))

                        else:
                            sleep(0.5)
                            self.btn.l(coor)
                            sleep(0.1)
                            self.btn.r()

                    elif item == "gm_1":
                        sleep(0.5)
                        self.btn.l(coor)
                        sleep(0.1)
                        self.btn.r()

                    else:
                        self.btn.l(coor)

                    sleep(0.1)

                elif is_hd:
                    if item == 'rw_jyl':
                        count += 1
                        sleep(5)

                        if count == 6:
                            processing = False
                            print('未找到任务，任务完成')
                            break

        print(f"经验链结束")


if __name__ == "__main__":
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

    Ring(adb, complex_task.task_finished).start()
