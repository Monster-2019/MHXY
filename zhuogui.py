from time import sleep



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
        sleep(1)

        self.logger.info(f"捉鬼领取")
        for n in range(31):
            if n % 10 == 0:
                self.capture()
                tem_coor = self.match('hd_zgrw', simi=0.995)
                btn_coor = self.match('cj',
                                      screen='imgTem/hd_zgrw',
                                      simi=0.995)
                if tem_coor and btn_coor:
                    new_coor = ((tem_coor[0] + btn_coor[0],
                                 tem_coor[1] + btn_coor[1], btn_coor[2],
                                 btn_coor[3]))
                    if new_coor:
                        self.btn.l(new_coor)
                        break

            else:
                self.btn.v(-1)

        self.loop(COUNT)

        self.logger.info(f"捉鬼完成")

    def player(self):
        pass

    def loop(self, count=25):
        self.logger.info(f"捉鬼进行中")
        step_list = ['zg_zgrw', 'zg_zg', 'zg_zgwc']
        cur_count = 0
        while cur_count <= count:
            for item in step_list:
                self.capture()
                is_hd = self.match('hd')
                if item == 'zg_zg':
                    coor = self.match(item, simi=0.95)
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
    
    def auto_match(self):
        self.logger.info(f"开始自动匹配")
        self.btn.hotkey('hd')
        self.smc('rchd', sleep_time=0.5)
        self.btn.m(590, 330)
        self.btn.v(1, 31)
        sleep(1)

        for n in range(31):
            if n % 10 == 0:
                self.capture()
                tem_coor = self.match('hd_zgrw', simi=0.995)
                btn_coor = self.match('cj',
                                      screen='imgTem/hd_zgrw',
                                      simi=0.995)
                if tem_coor and btn_coor:
                    new_coor = ((tem_coor[0] + btn_coor[0],
                                 tem_coor[1] + btn_coor[1], btn_coor[2],
                                 btn_coor[3]))
                    self.btn.l(new_coor)
                    sleep(1)

                    self.smc('zg_auto_match')
                    sleep(1)
                    self.btn.r()
                    self.btn.r()
                    sleep(5)
                    break

            else:
                self.btn.v(-1)

        self.btn.hotkey('dw')

        while True:
            in_team = self.smc('tcdw', is_click=False)
            if in_team:
                self.logger.info(f"已匹配队伍")
                self.smc('rw_gb')
                break

            sleep(1)
        
        return True
    
    def has_zg(self):
        status = False
            # sleep(60)
        self.btn.hotkey('rw', sleep_time=1)
        self.smc('rw_dqrw', sleep_time=0.5)

        has_cgrw = self.smc('rw_cgrw', sleep_time=0.5)
        status = self.smc('rw_cgrw_zgrw', sleep_time=0.5)
        if status or not has_cgrw:
            self.smc('rw_gb')
            return status

        self.smc('rw_cgrw', sleep_time=0.5)
        status = self.smc('rw_cgrw_zgrw', sleep_time=0.5)
                
        self.smc('rw_gb')
        return status
    
    def single(self):
        self.logger.info(f"捉鬼开始")
        while not self.smc('hd', is_click=False):
            self.btn.r()

        if self.task_finished('zg_wc'):
            self.logger.info(f"捉鬼完成")
            self.btn.r()
            return
        
        self.logger.info(f"捉鬼进行中")

        self.auto_match()

        count = 0
        while True:
            if count >= 20:
                self.leave_team()
                break
            for i in range(30):
                sleep(1)
                is_hd = self.smc('hd', is_click=False)
                is_fight = self.smc('qx', is_click=False)
                if is_hd:
                    continue
                if is_fight:
                    while True:
                        is_fight = self.smc('qx', is_click=False)
                        if not is_fight:
                            break
                    count += 1
                    self.logger.info(f"已进行{count}回合抓鬼")
                    break
            else:
                has_zg = self.has_zg()
                if not has_zg:
                    self.leave_team()
                                    
                    zg_wc = self.task_finished('zg_wc')
                    if zg_wc:
                        break
                    else:
                        self.auto_match()
            
            sleep(1)

        self.logger.info(f"捉鬼任务完成")
    
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

    Zhuogui(adb).single()
    # Zhuogui(adb).loop()
    # Zhuogui().leader()

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
    adb['leave_team'] = complex_task.leave_team

    Zhuogui(adb).single()
    # main()