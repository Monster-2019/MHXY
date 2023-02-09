from time import sleep


class Yunbiao(object):

    def __init__(self, adb, task_finished):
        for key, val in adb.items():
            self[key] = val
        self.task_finished = task_finished

    def start(self):
        while not self.smc('hd', is_click=False):
            self.btn.r()

        if self.task_finished('yb_wc'):
            return

        self.btn.Hotkey("hd")
        self.smc("rchd", sleepT=0.5)
        self.btn.MBtn(590, 330)
        self.btn.VBtn(1, 31)
        sleep(0.5)

        processing = False

        for n in range(31):
            if n % 10 == 0:
                self.capture()
                tem_coor = self.match('hd_yb1') or self.match('hd_yb')
                if tem_coor:
                    btn_coor = self.match('cj', 'imgTem/hd_yb1') or self.match(
                        'cj', 'imgTem/hd_yb')
                    new_coor = ((tem_coor[0][0] + btn_coor[0][0],
                                 tem_coor[0][1] + btn_coor[0][1], btn_coor[2],
                                 btn_coor[3]))
                    if btn_coor:
                        self.btn.l(new_coor)
                        processing = True
                        break

            else:
                self.btn.v(-1)

        if processing:
            count = 0
            step_list = ['yb_ys', 'qd']
            while processing:
                is_hd = self.smc('hd', is_click=False)
                if count >= 3 and is_hd:
                    processing = False
                    break

                for item in step_list:
                    res = self.smc(item)
                    if res and item == 'qd':
                        count += 1
                        sleep(20)

                sleep(1)


if __name__ == '__main__':
    Yunbiao().start()