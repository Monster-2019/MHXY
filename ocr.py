import cv2 as cv
import pytesseract

pytesseract.pytesseract.tesseract_cmd = ".\\tesseract\\tesseract.exe"

def ocr(path, lang="eng", **kwds):
    config = f"-l {lang} --psm 7"

    image = cv.imread(path)

    text = pytesseract.image_to_string(image, config=config)

    print(text.strip())

    return text.strip()


if __name__ == '__main__':
    # ocr('./images/imgTem/ck_max.jpg')
    # get_token()
    ocr('./images/imgTem/bb_60.JPG', 'chi_sim')