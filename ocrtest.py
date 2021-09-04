import re
from PIL import Image
import pytesseract
import cv2 as cv

def test ():
    tessdata_dir_config ='--tessdata-dir "D:/dev/Tesseract-OCR/tessdata" --psm 7'
    img = cv.imread('./images/coor1.jpg', 0)
    result = pytesseract.image_to_string(img, config=tessdata_dir_config, lang="num")
    print(result)
    res = re.findall(r"\d+", result)
    print(res)

if __name__ == '__main__':
    test()