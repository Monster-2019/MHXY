from time import sleep


class SMC(object):

    def __init__(self, capture, match, btn):
        self.capture = capture.capture
        self.match = match.match_tem
        self.btn = btn

    def smc(self, tem, simi=0, sleep_time=0):
        self.capture()
        coor = self.matchTem(tem, simi=simi)
        if coor:
            self.B.LBtn(coor)
            sleep(sleep_time)
            return coor
        return 0


if __name__ == '__main__':
    SMC().smc('bt_wc')