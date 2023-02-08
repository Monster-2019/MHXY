class SMC(object):

    def __init__(self, capture, match, btn):
        self.capture = capture
        self.match = match
        self.btn = btn

    def smc(self, tem, **kwargs):
        self.capture()
        coor = self.matchTem(tem, **kwargs)
        if coor:
            self.B.LBtn(coor, **kwargs)
            return coor
        return 0


if __name__ == '__main__':
    SMC().smc('bt_wc')