import sys
sys.path.append(".")
sys.path.append("..")
from public.glo import Glo
import traceback

from paddleocr import PaddleOCR, draw_ocr
from public.cutScreen import CScreen

def not_empty(s):
    return s and s.strip()

class OCR:
    def __init__(self):
        super(OCR, self).__init__()
        self.g = Glo()
        self.padOcr = PaddleOCR(enable_mkldnn=True, use_gpu=False, lang="ch")

    def ocr(self):
        try:
            # image = cv.imread("./images/screen" + self.g.get("screen") + ".jpg", 0)
            # content = pytesseract.image_to_string(image, lang="chi_sim", config="--psm 6").splitlines()
            # content = list(filter(not_empty, content))
            # result = ''
            # for item in content:
            #     result += item
            # return result or 0
            result = self.padOcr.ocr("./images/screen" + self.g.get("screen") + ".jpg", det=False)
            return result[0][0][0]

        except BaseException as e:
            traceback.print_exc()

if __name__ == "__main__":
    CScreen().customCutScreen('name')
    r = OCR().ocr()
    print(r)
