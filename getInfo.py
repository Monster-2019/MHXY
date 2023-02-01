import sys

from glo import Glo
from btn import Btn
from cutScreen import CScreen
from match import Match
from log import log
from retrying import retry
from paddleocr import PaddleOCR

from time import sleep
from ocr import ocr

import re
import cv2

# def ocr(img):
#     try:
#         ocr = PaddleOCR(lang="ch")
#         result = ocr.ocr(img, det=False)
#         return result[0][0][0]

#     except BaseException as e:
#         pass
#         # traceback.print_exc()

class Info():
    def __init__(self):
        self.g = Glo()
        self.B = Btn()
        self.cutScreen = CScreen().cutScreen
        self.customCutScreen = CScreen().customCutScreen
        self.matchTem = Match().matchTem

    # @retry
    def handleOcr(self, ocrCoor, isNum=False):
        self.customCutScreen(ocrCoor)
        sleep(0.5)
        txt = ocr(cv2.imread('./images/screen' + self.g.get('screen') + '.jpg'))
        print('识别', txt)
        if not txt:
            # raise IOError("ocr err")
            return '未识别'
        else:
            return txt


    def getInfo(self):
        try:
            # txt = ocr(cv2.imread('./images/screen1.jpg'))
            # print(txt)
            # return
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
    # txt = ocr(cv2.imread('./images/screen1.jpg'))
    # print(txt)