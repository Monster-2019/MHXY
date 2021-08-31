import easyocr
import re
import cv2 as cv

def test():
    reader = easyocr.Reader(['en'], gpu=False)
    img = cv.imread('./images/screen0.jpg')
    result = reader.readtext(img, detail=0)

    res = re.findall(r"\d+", result[0])

    print(result[0])
    print(res[0], res[1])

test()