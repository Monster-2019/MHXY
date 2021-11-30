import cv2 as cv
import pytesseract

def not_empty(s):
    return s and s.strip()

def start():
    image = cv.imread("./images/imgTem/zh1_z6.JPG", 0)
    content = pytesseract.image_to_string(image, lang="chi_sim").splitlines()
    content = list(filter(not_empty, content))
    if content:
        return content[0]
    return ''

print(start())