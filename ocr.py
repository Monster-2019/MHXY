import cv2 as cv
import pytesseract
import configparser
import os
from loguru import logger

conf = configparser.ConfigParser()
path = os.path.join(os.getcwd(), "config.ini")
conf.read(path, encoding='utf-8')

SHARED_FOLDER = conf.get('software_path', 'tesseract_ocr')

pytesseract.pytesseract.tesseract_cmd = SHARED_FOLDER  # your path may be different

def ocr(path, lang="eng", **kwds):
    config = f"-l {lang} --psm 7"
    # config = r"-l eng --psm 7"

    image = cv.imread(path)
    # image = cv.imread('./images/0.jpg', 0)

    text = pytesseract.image_to_string(image, config=config)

    # print(pytesseract.image_to_string(image, lang='chi_sim', config=config))
    # print(pytesseract.image_to_string(image, lang='eng', config=config))
    # print(pytesseract.image_to_string(image, lang='chi_sim+eng',
    #                                   config=config))

    return text


if __name__ == '__main__':
    # ocr('./images/imgTem/ck_max.jpg')
    # get_token()
    ocr('./images/0.jpg', 'chi_sim')