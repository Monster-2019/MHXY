import sys
sys.path.append(".")
import traceback

from paddleocr import PaddleOCR
from cutScreen import CScreen
import cv2

def ocr(img):
    try:
        ocr = PaddleOCR(use_angle_cls=False, use_tensorrt=True, enable_mkldnn=True, use_gpu=False, lang="ch")
        result = ocr.ocr(img, det=False)
        return result[0][0][0]

    except BaseException as e:
        traceback.print_exc()

if __name__ == '__main__':
    CScreen().customCutScreen('hy')
    txt = ocr(cv2.imread('./images/screen0.jpg'))
    print(txt)