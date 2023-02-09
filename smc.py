class SMC(object):

    def __init__(self, capture, match, btn):
        self.capture = capture
        self.match = match
        self.btn = btn

    def smc(self, tem, **kwargs):
        self.capture()
        coor = self.match(tem, **kwargs)
        if coor:
            self.btn.l(coor, **kwargs)
            return coor
        return 0

    def smcs(self, tem, **kwargs):
        self.capture()
        coor = self.match.match_feature(tem, **kwargs)
        if coor:
            self.btn.l(coor, **kwargs)
            return coor
        return 0

    def __call__(self, tem, **kwargs):
        return self.smc(tem, **kwargs)


if __name__ == '__main__':
    SMC().smc('bt_wc')