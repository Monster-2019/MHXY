from time import sleep
from btn import Btn
from smc import SMC

class HD:
    def __init__(self):
        self.B = Btn()
        self.smc = SMC().smc
        self.smca = SMC().smca

    def jihuo(self):
        while True:
            self.smc('jh')
            sleep(0.1)

    def qie(self):
        xhList = ['zd', 'lshd_qie', 'lshd_qc']
        end = False
        while not end:
            for item in xhList:
                res = self.smc(item)
                if res and item == 'lshd_qc':
                    end = True
                    break

                sleep(0.5)

if __name__ == '__main__':
    HD().jihuo()
