from time import sleep
from datetime import datetime


class GengZhong(object):

    def __init__(self, adb):
        for key, val in adb.items():
            self.__dict__[key] = val
        if adb["print"]: 
            global print 
            print = adb["print"]
        self.weekday = datetime.today().isoweekday()

    def sell(self):
        print(f'{self.name}开始出售金银花')
        while not self.smc('hd', is_click=False):
            self.btn.r()

        self.btn.hotkey('bb')
        self.smc('bb_zl', sleep_time=0.5)
        self.btn.m(720, 440)
        self.btn.v(1, 30)
        sleep(0.5)

        page = 1
        for n in range(61):
            if n % 10 == 0:
                res = self.smc('bb_jyh', sleep_time=0.5)
                if res:
                    self.smc('bb_gd', sleep_time=0.5)
                    self.smc('bb_gfbt', sleep_time=1)
                    self.btn.r()
                    break

                else:
                    self.btn.m(720, 440)
                    self.btn.v(-1, 6)

        sleep(1)
        complete = False
        while not complete:
            res = self.smc('gfbt_gq', sleep_time=0.5)
            if res:
                self.smc('gfbt_cxsj', sleep_time=0.5)
                self.smc('bzts', sleep_time=0.5)
                self.smc('qd', sleep_time=0.5)
            else:
                complete = True
                break

        complete = False
        while not complete:
            self.capture.custom_capture('gfbt')
            res = self.match('gfbt_jyh')
            if res:
                Coor = ((647 + res[0], 207 + res[1], res[2], res[3]))
                self.btn.l(Coor, sleep_time=0.5)
                # res = self.smc('gfbt_jyh', infoKey='gfbt', sleep_time=0.5)
                # if res != 0:
                self.smc('gfbt_sj', sleep_time=0.5)
                res = self.smc('gfbt_max', sleep_time=0.5)
                if res:
                    complete = True
                    break
                self.smc('bzts', sleep_time=0.5)
                self.smc('qd', sleep_time=0.5)
            else:
                complete = True
                break

        self.btn.r()
        self.btn.r()

        print(f"{self.name}出售完成")

        return complete

    def start(self, isSell=False):
        print(f'{self.name}开始耕种')
        while not self.smc('hd', is_click=False):
            self.btn.r()

        self.btn.hotkey('jy', sleep_time=2)

        self.smc('jy_hj', sleep_time=3)

        while not self.smc('hd', is_click=False):
            sleep(1)

        coor = self.smc('td_status', sleep_time=2)

        self.capture()

        is_sh = self.match('btn_sh', simi=0.999)

        is_zz = self.match('gz_zz', simi=0.999)

        if is_sh:
            self.btn.l(is_sh)
            print(f'{self.name}已成熟，可收获')
        
        if is_zz:
            print(f'{self.name}无作物，可耕种')

        if not is_sh and not is_zz:
            print('成熟中')
            self.btn.r()
            return
        
        sleep(3)

        if is_sh:
            self.btn.l((250, 250, 2, 2))
            sleep(3)
            self.smc('td_status', sleep_time=0.5)

        print(f'{self.name}耕种中')
        self.capture()
        tem_coor = self.match('gz_jyh')
        btn_coor = self.match('gz_add', screen='imgTem/gz_jyh')
        if tem_coor and btn_coor:
            new_coor = ((tem_coor[0] + btn_coor[0], tem_coor[1] + btn_coor[1],
                         btn_coor[2], btn_coor[3]))
            for i in range(10):
                self.btn.l(new_coor)
                sleep(0.1)

            self.smc('gz_zz', sleep_time=0.5)

            self.btn.r()

        print(f'{self.name}完成耕种')
        if ((self.weekday - 1) % 2 == 0) or isSell:
            self.sell()


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

    GengZhong(adb, complex_task.task_finished).start()
    # GengZhong(adb, complex_task.task_finished).sell()