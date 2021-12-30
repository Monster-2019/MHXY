import sys
sys.path.append('..')
from public.glo import Glo
from public.cutScreen import CScreen
from public.btn import Btn
from public.matchTem import Match
from ocr import OCR
from public.log import log
from retrying import retry

from time import sleep
import re

class Info():
    def __init__(self):
        self.g = Glo()
        self.B = Btn()
        self.ocr = OCR().ocr
        CScreenObj = CScreen()
        self.cutScreen = CScreenObj.cutScreen
        self.customCutScreen = CScreenObj.customCutScreen
        self.matchTem = Match().matchTem

    @retry(stop_max_attempt_number=3)
    def useOcr(self, isNum):
        self.customCutScreen(self.ocrText)
        sleep(0.5)
        self.B.RBtn()
        txt = self.ocr(isNum)
        return txt

    def setOcr(self, hotk, ocrText, isNum=False):
        self.B.Hotkey(hotk)
        sleep(1)
        self.ocrText = ocrText
        return self.useOcr(isNum)

    def getInfo(self):
        try:
            while True:
                self.cutScreen()
                btnCoor = self.matchTem('hd')
                if btnCoor == 0:
                    self.B.RBtn()
                else:
                    break
            # 获取角色名字和等级
            nameLevel = self.setOcr('js', 'name', False)

            name = '空'
            level = '空'
            if nameLevel:
                res = re.match(r"(.+)(\d{2})", nameLevel)
                name = res.group(1)
                level = int(res.group(2))
                self.g.set("name", name)
                self.g.set("level", level)
                sleep(0.5)

            # 获取金币数量和银币数量
            gold = self.setOcr('bb', 'gold', True)
            if gold:
                self.g.set("gold", gold)
                sleep(0.5)
            
            silver = self.setOcr('bb', 'silver', True)
            if silver:
                self.g.set("silver", silver)

            # log(f"账号:{name}, 等级:{level}级")
            log(f"账号:{name}, 等级:{level}级, 金币:{gold}, 银币:{silver}")
        except Exception as e:
            log(e, True)

if __name__ == '__main__':
    Info().getInfo()