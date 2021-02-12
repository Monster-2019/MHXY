import sys
sys.path.append('..')
from public.glo import Glo
from public.cutScreen import CScreen
from public.btn import Btn
from public.matchTem import Match
from public.ocr import OCR
from public.log import log
from retrying import retry

from time import sleep
import re

def retry_if_error(exception):
    if isinstance(exception, Exception):
        log('获取账号信息错误', True)
    return isinstance(exception, Exception)

class Info():
    def __init__(self, windowClass):
        self.g = Glo()
        self.g.set('windowClass', windowClass)
        self.B = Btn()
        ocr = OCR()
        self.ocr = ocr.ocr
        C = CScreen()
        self.cutScreen = C.cutScreen
        M = Match()
        self.matchTem = M.matchTem

    @retry(retry_on_exception=retry_if_error, stop_max_attempt_number=2)
    def useOcr(self):
        self.B.Hotkey(self.hotk)
        sleep(0.5)
        self.cutScreen(self.ocrText)
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
            tem = self.setOcr('js', 'name')

            if tem != None:
                name = re.findall(r"[1-5a-zA-Z_\u4e00-\u9fa5]+", tem)
                name = name[0]
                self.g.set("name", name)
                level = re.findall(r"\d+", tem)
                if int(level[0]) > 1000:
                    level = int(level[0]) % 100
                else:
                    level = int(level[0])
                self.g.set("level", level)
                sleep(0.5)

            # 获取金币数量和银币数量
            # gold = self.setOcr('bb', 'gold')
            # if gold != None:
            #     self.g.set("gold", gold)
            #     sleep(0.5)
            
            # silver = self.setOcr('bb', 'silver')
            # if silver != None:
            #     self.g.set("silver", silver)

            log(f"账号:{name}, 等级:{level}级")
        except Exception as e:
            log(e, True)

if __name__ == '__main__':
    g = Info('0')
    g.getInfo()