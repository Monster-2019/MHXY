sys.path.append(".")
sys.path.append("..")
import sys
import cv2 as cv
import pytesseract
from public.glo import Glo


def not_empty(s):
    return s and s.strip()


class OCR:
    def __init__(self):
        super(OCR, self).__init__()
        self.g = Glo()

    def ocr(self):
        image = cv.imread("./images/screen" + self.g.get("screen") + ".jpg", 0)
        content = pytesseract.image_to_string(image, lang="chi_sim").splitlines()
        content = list(filter(not_empty, content))
        if content:
            return content[0]
        return 0


if __name__ == "__main__":
    OCR().ocr()
