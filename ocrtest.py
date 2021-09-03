import re
from PIL import Image
import pytesseract

def test ():
    tessdata_dir_config ='--tessdata-dir "D:/dev/Tesseract-OCR/tessdata" --psm 7'
    img = Image.open('./images/coor/coor281.jpg')
    result = pytesseract.image_to_string(img, config=tessdata_dir_config, lang='num')
    print(result)
    res = re.findall(r"\d+", result)
    print(res)

if __name__ == '__main__':
    test()