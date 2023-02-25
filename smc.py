class SMC(object):

    def __init__(self, capture, match, btn):
        self.capture = capture
        self.match = match
        self.btn = btn

    def smc(self, tem, **kwds):
        self.capture()
        coor = self.match(tem, **kwds)
        if coor:
            self.btn.l(coor, **kwds)
            return coor
        return 0

    def __call__(self, tem, **kwds):
        return self.smc(tem, **kwds)


if __name__ == '__main__':
    SMC().smc('bt_wc')