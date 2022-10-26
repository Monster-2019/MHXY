import sys
sys.path.append(".")
sys.path.append("..")
import traceback
# import cv2

from paddleocr import PaddleOCR
from cutScreen import CScreen

def ocr(img):
    try:
        ocr = PaddleOCR(use_angle_cls=False, use_tensorrt=True, enable_mkldnn=True, use_gpu=False, lang="ch")
        result = ocr.ocr(img, det=False)
        return result[0][0][0]

    except BaseException as e:
        traceback.print_exc()

if __name__ == "__main__":
    r = ocr(cv2.imread('./images/imgTem/bb_60.jpg'))
    print(r)
