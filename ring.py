from time import sleep, time


class Ring(object):

    def __init__(self, adb):
        for key, val in adb.items():
            self.__dict__[key] = val

    def legend(self):
        self.btn.hotkey('gj')

        sleep(1)

        self.btn.l((400, 340, 2, 2))

        start = int(time())
        end = int(time())
        while end - start < 1200:
            end = int(time())
            res = self.smc('sj')
            if res:
                return True
            sleep(1)

        while True:
            is_hd = self.smc('hd', is_click=False)
            if is_hd:
                self.btn.l((500, 450, 2, 2))
                break

        return False

    def start(self):
        self.logger.info(f"开始经验链")

        while not self.smc('hd', is_click=False):
            self.btn.r()

        processing = self.smc('rw_jyl', simi=0.9, is_click=False)

        if not processing:
            if self.task_finished('jyl_wc'):
                self.logger.info('经验链完成')
                return

        self.logger.info(f"经验链领取")

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
                            
                            break

                else:
                    self.btn.v(-1)

        if not processing:
            self.logger.info('未找到任务')
            return

        self.logger.info(f"经验链进行中")

        sleep(1)
        self.btn.r()
        sleep(1)

        self.smc('rw_jyl', simi=0.9)

        step_list = ["gm", "gm_1", 'btgm', "dh", "sj"]

        count = 0
        while processing:
            for item in step_list:
                # print(123, item)
                if item == 'dh':
                    coor = self.smc(item, simi=0.9, is_click=False)
                else:
                    coor = self.smc(item, is_click=False)
                if coor:
                    count = 0
                    if item == "dh":
                        sleep(0.5)
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
                        sleep(1)
                        res = self.smc('bt_sj') or self.smc(
                            'bt_jlh') or self.smc('bt_mgh')
                        print('高价', res)
                        if res:
                            self.logger.info("高价物品，开始传说")
                            self.btn.r()

                            has_legend = self.legend()
                            if not has_legend:
                                self.logger.info("传说失败，手动处理")
                                return

                        else:
                            self.btn.l(coor)
                            sleep(1)
                            self.btn.r()

                    else:
                        self.btn.l(coor)

                sleep(1 / len(step_list))
            else:
                count += 1
                print('count', count)
                if count < 15:
                    continue
                # for i in range(5):
                #     if self.smc('rw_jyl', simi=0.9):
                #         break
                #     sleep(2)
                # else:
                #     continue
            
            count = 0
            is_still = self.is_still()
            if is_still:
                sleep(1)
                has_jyl = self.smc('rw_jyl', simi=0.9)
                if not has_jyl:
                    processing = True

        self.logger.info(f"经验链完成")


def main():
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

    Ring(adb).start()


if __name__ == "__main__":
    main()