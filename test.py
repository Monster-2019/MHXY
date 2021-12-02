import sys
sys.path.append(".")
sys.path.append("..")
import cv2 as cv
import pytesseract


def not_empty(s):
    return s and s.strip()


class OCR:
    def __init__(self):
        super(OCR, self).__init__()

    def ocr(self):
        try:
            image = cv.imread("./unnamed.jpg", 0)
            # cv.imwrite('unnamed1.jpg', image)
            content = pytesseract.image_to_string(image, lang="num", config="--psm 6").splitlines()
            content = list(filter(not_empty, content))
            print(content[0].replace(',', ''))
            if content:
                return content[0]
            return 0
        except BaseException as e:
            print('识别错误:', e)


if __name__ == "__main__":
    OCR().ocr()
