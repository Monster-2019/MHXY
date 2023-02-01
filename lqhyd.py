from time import sleep
from cutScreen import CScreen
from match import Match
from btn import Btn
from smc import SMC
from glo import Glo
from log import log
from ocr import ocr
import cv2

class LQHYD:
    def __init__(self):
        self.g = Glo()
        self.name = self.g.get('name')
        self.B = Btn()
        self.cutScreen = CScreen().cutScreen
        self.customCutScreen = CScreen().customCutScreen
        self.matchTem = Match().matchTem
        self.smc = SMC().smc

    def start(self):
        try:
            while self.smc('hd', count=0) == 0:
                self.B.RBtn()

            self.B.Hotkey('hd')

            xhList = ['hy_20', 'hy_40', 'hy_60', 'hy_80', 'hy_100']
            for item in xhList:
                while True:
                    res = self.smc(item, simi=0.95, sleepT=0.5)
                    if res:
                        res = self.smc('sygb', sleepT=0.2)
                            
                    if item == 'hy_100':
                        complete = True
                    break

            self.customCutScreen('hy')
            
            txt = ocr(cv2.imread('./images/screen' + self.g.get('screen') + '.jpg'))
            print('活跃:', txt)
            self.g.set('hyd', txt)

            sleep(0.5)
            self.B.RBtn()

            if complete:
                log(f"账号: { self.name } 活跃度领取完成")
                return 1
            else:
                self.start()

        except Exception as e:
            log(e, True)
