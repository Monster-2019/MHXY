import configparser
import os

import cv2 as cv
import pytesseract

conf = configparser.ConfigParser()
path = os.path.join(os.getcwd(), "config.ini")
conf.read(path, encoding='utf-8')

exe_file = conf.get('software_path', 'tesseract_ocr')
pytesseract.pytesseract.tesseract_cmd = exe_file

def ocr(path, lang="eng", **kwds):
    config = f"-l {lang} --psm 7"

    image = cv.imread(path)

    text = pytesseract.image_to_string(image, config=config)

    return text


if __name__ == '__main__':
    # ocr('./images/imgTem/ck_max.jpg')
    # get_token()
    ocr('./images/0.jpg', 'chi_sim')