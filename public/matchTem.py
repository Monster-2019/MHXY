import sys
sys.path.append('..')
import cv2 as cv
import numpy as np
from time import sleep
from public.glo import Glo
from public.cutScreen import CScreen

class Match():
    simi = 0.85
    kernel = np.ones((1, 1), np.uint8)

    def __init__(self):
        g = Glo()
        self.screen = 'screen' + g.get('windowClass')

    def imgProcess(self, img, type=0):
        if type == 0:
            # 开运算处理
            return cv.morphologyEx(img, cv.MORPH_OPEN, self.kernel)
        elif type == 1:
            # 自适应阈值
            return cv.adaptiveThreshold(img, 255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,cv.THRESH_BINARY,11,2)
        elif type == 2:
            # 去噪处理
            return cv.fastNlMeansDenoising(img, None, 10, 7, 21)

    def matchTem(self, tem, img=0, simi=0.85, bina=False):
        if img == 0:
            img = self.screen
        self.simi = simi
            
        screen = cv.imread('./images/' + img  + '.jpg', 0)
        screen = self.imgProcess(screen)
        if isinstance(tem, str):
            newTem = cv.imread('./images/imgTem/' + tem  + '.jpg', 0)
            newTem = self.imgProcess(newTem)
            result = cv.matchTemplate(screen, newTem, cv.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
            
        elif isinstance(tem, list):
            for item in tem:
                newTem = cv.imread('./images/imgTem/' + item  + '.jpg', 0)
                newTem = self.imgProcess(newTem)
                result = cv.matchTemplate(screen, newTem, cv.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
                if max_val > self.simi:
                    break
        # cv.imshow("custom_blur_demo1", screen)
        # cv.imshow("custom_blur_demo", newTem)
        # cv.waitKey(0)
        # cv.destroyAllWindows()

        # print(max_val, max_loc)
        if max_val > self.simi:
            w, h = newTem.shape[::-1]
            return (max_loc, (w, h))
        else:
            return 0

if __name__ == '__main__':
    CScreen().cutScreen()
    Match().matchTem('bb_gms')
