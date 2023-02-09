from time import sleep


class SJ(object):

    def __init__(self, adb, task_finished):
        for key, val in adb.items():
            self[key] = val
        self.task_finished = task_finished

    def start(self):
        while not self.smc('hd', is_click=False):
            self.btn.r()

        if self.task_finished('sj_wc'):
            return

        self.btn.hotkey("hd")
        self.smc("rchd", sleep_time=0.5)
        self.btn.m(590, 330)
        self.btn.v(1, 31)
        sleep(0.5)

        processing = False

        for n in range(31):
            if n % 10 == 0:
                self.capture()
                tem_coor = self.match('hd_sjqy') or self.match('hd_sjqy1')
                if tem_coor:
                    btn_coor = self.match('cj',
                                          'imgTem/hd_sjqy') or self.match(
                                              'cj', 'imgTem/hd_sjqy1')
                    new_coor = ((tem_coor[0] + btn_coor[0],
                                 tem_coor[1] + btn_coor[1], btn_coor[2],
                                 btn_coor[3]))
                    if btn_coor:
                        self.btn.l(new_coor, sleep_time=1)
                        while True:
                            if self.smc('sj_start', is_click=False):
                                processing = True
                                break

            else:
                self.btn.v(-1)

        if processing:
            while processing:
                res = self.smc('sj_dw', is_click=False)
                if res:
                    self.btn.RBtn()
                    processing = False
                    break
                else:
                    self.btn.l((380, 230, 170, 240), sleep_time=0.5)


if __name__ == '__main__':
    SJ().start()
