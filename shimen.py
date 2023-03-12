from time import sleep


class Shimen(object):

    def __init__(self, adb, task_finished):
        for key, val in adb.items():
            self.__dict__[key] = val
        self.task_finished = task_finished

    def start(self):
        print(f'{self.name}开始师门任务')
        while not self.smc('hd', is_click=False):
            self.btn.r()

        while True:
            if not self.smc("sygb", sleep_time=0.5):
                break

        if self.task_finished('sm_wc'):
            print(f'{self.name}师门任务已完成')
            self.btn.r()
            return

        # self.btn.hotkey('zz', sleep_time=1)
        # self.btn.l('zr1', sleep_time=0.5)
        # self.btn.r()

        sleep(1)
        self.btn.hotkey("hd")
        self.smc("rchd", sleep_time=0.5)
        self.btn.m(590, 330)
        self.btn.v(1, 31)

        processing = self.smc('sm_sm')

        if not processing:
            print(f'{self.name}领取师门任务')
            for n in range(31):
                if n % 10 == 0:
                    self.capture()
                    tem_coor = self.match("hd_smrw")
                    btn_coor = self.match("cj", screen="imgTem/hd_smrw")
                    if tem_coor and btn_coor:
                        new_coor = ((tem_coor[0] + btn_coor[0],
                                     tem_coor[1] + btn_coor[1], btn_coor[2],
                                     btn_coor[3]))
                        self.btn.l(new_coor, sleep_time=1)

                        # 去完成或继续任务
                        while True:
                            self.capture()
                            btn_coor = self.match("sm_qwc") or self.match(
                                "sm_jxrw")
                            if btn_coor:
                                self.btn.l(btn_coor, sleep_time=1)
                                processing = True
                                break

                        break
                else:
                    self.btn.v(-1)

        if processing:
            print(f'{self.name}师门任务进行中')
            step_list = [
                "sm_mpgx",
                "sm_sm",
                "djjx",
                "dh",
                "dhda",
                "gm",
                "btgm",
                "gfgm",
                "sj",
                "sy",
                "sm_hdwp",
                "sm_rwdh",
                # "jm_gb",
            ]

            while processing:
                for item in step_list:
                    self.capture()
                    is_hd = self.match('hd')
                    if item == "dh" or item == 'dhda' or item == "sm_sm":  #
                        coor = self.match(item, simi=0.94)
                    else:
                        coor = self.match(item)
                    if coor:
                        if item == "dh" or item == "dhda":
                            while True:
                                coor = self.smc(item, is_click=False)
                                if coor:
                                    new_coor = ((coor[0], coor[1] + 69, 87,
                                                 22))
                                    self.btn.l(new_coor)
                                    sleep(0.3)
                                else:
                                    break

                            sleep(0.5)

                        elif item == "djjx":
                            while True:
                                res = self.smc("djjx", sleep_time=0.2)
                                if res:
                                    break
                            
                            sleep(0.5)

                        elif item == "btgm" or item == "gfgm":
                            sleep(2)
                            item_coor = (308, 245, 294, 75)
                            self.btn.l(item_coor, sleep_time=0.5)
                            self.btn.l(coor, sleep_time=1)

                            if self.smc(item):
                                self.btn.r()

                        elif item == "sy":
                            self.btn.l(coor, max_x=920)

                        elif item == "sm_mpgx":
                            self.smc("sm_jl")
                            self.btn.r()
                            processing = False
                            break

                        elif item == 'sm_sm' and is_hd:
                            self.btn.l(coor, min_x=800)

                        else:
                            self.btn.l(coor, min_x=300)

                        sleep(0.1)

                    elif is_hd:
                        if item == "sm_sm":
                            if self.smc("hd", is_click=False):
                                self.btn.r()
                                self.btn.m(900, 300)
                                self.btn.v(1, 10)
                    
                    sleep(1 / len(step_list))

            sleep(0.5)
            while True:
                coor = self.smc('sy')
                if not coor:
                    break

        print(f'{self.name}完成师门任务')
        return 1


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

    Shimen(adb, complex_task.task_finished).start()
