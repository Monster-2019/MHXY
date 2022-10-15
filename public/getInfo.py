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
        self.cutScreen = CScreen().cutScreen
        self.customCutScreen = CScreen().customCutScreen
        self.matchTem = Match().matchTem

    @retry
    def handleOcr(self, ocrText, isNum=False):
        self.customCutScreen(ocrText)
        sleep(0.5)
        txt = self.ocr()
        if not txt:
            raise IOError("ocr err")
        else:
            return txt


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
            self.B.Hotkey('js')
            nameLevel = self.handleOcr('name', False)
            self.B.RBtn()

            name = '空'
            level = '空'
            if nameLevel:
                res = re.match(r"(.+)(\d{2})", nameLevel)
                if res:
                    name = res.group(1)
                    level = int(res.group(2))
                    self.g.set("name", name)
                    self.g.set("level", level)
                    sleep(0.5)

            # 获取金币数量和银币数量
            self.B.Hotkey('bb')
            gold = self.handleOcr('gold', True)
            if gold:
                self.g.set("gold", gold)
                sleep(0.5)
            
            silver = self.handleOcr('silver', True)
            if silver:
                self.g.set("silver", silver)

            self.B.RBtn()
            log(f"账号:{name}, 等级:{level}级, 金币:{gold}, 银币:{silver}")
        except Exception as e:
            log(e, True)

if __name__ == '__main__':
    Info().getInfo()