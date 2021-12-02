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

def retry_if_error(exception):
    if isinstance(exception, Exception):
        log('获取账号信息错误', True)
    return isinstance(exception, Exception)

class Info():
    def __init__(self):
        self.g = Glo()
        self.B = Btn()
        self.ocr = OCR().ocr
        CScreenObj = CScreen()
        self.cutScreen = CScreenObj.cutScreen
        self.customCutScreen = CScreenObj.customCutScreen
        self.matchTem = Match().matchTem

    @retry(retry_on_exception=retry_if_error, stop_max_attempt_number=2)
    def useOcr(self):
        self.B.Hotkey(self.hotk)
        sleep(1)
        self.customCutScreen(self.ocrText)
        sleep(0.5)
        self.B.RBtn()
        txt = self.ocr()
        return txt

    def setOcr(self, hotk, ocrText):
        self.hotk = hotk
        self.ocrText = ocrText
        return self.useOcr()

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
            nameLevel = self.setOcr('js', 'name')

            if nameLevel:
                res = re.match(r"(.+)(\d{2})级?", nameLevel)
                name = res.group(1)
                level = int(res.group(2))
                self.g.set("name", name)
                self.g.set("level", level)
                sleep(0.5)

            # 获取金币数量和银币数量
            # gold = self.setOcr('bb', 'gold')
            # print(gold)
            # if gold:
            #     self.g.set("gold", gold)
            #     sleep(0.5)
            
            # silver = self.setOcr('js', 'silver')
            # print(silver)
            # if silver:
            #     self.g.set("silver", silver)

            log(f"账号:{name}, 等级:{level}级")
            # log(f"账号:{name}, 等级:{level}级, 金币:{gold}, 银币:{silver}")
        except Exception as e:
            log(e, True)

if __name__ == '__main__':
    Info().getInfo()