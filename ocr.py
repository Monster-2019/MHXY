import sys
sys.path.append(".")
sys.path.append("..")
import cv2 as cv
import pytesseract
from public.glo import Glo
import traceback


def not_empty(s):
    return s and s.strip()

pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

class OCR:
    def __init__(self):
        super(OCR, self).__init__()
        self.g = Glo()

    def ocr(self, isNum=False):
        try:
            image = cv.imread("./images/screen" + self.g.get("screen") + ".jpg", 0)
            content = pytesseract.image_to_string(image, lang="chi_sim", config="--psm 6").splitlines()
            content = list(filter(not_empty, content))
            result = ''
            for item in content:
                result += item
            return result or 0
        except BaseException as e:
            traceback.print_exc()
            # print('识别错误:', e)

if __name__ == "__main__":
    r = OCR().ocr()
    print(r)
