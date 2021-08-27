import sys

sys.path.append(".")
sys.path.append("..")
import cv2 as cv
from public.glo import Glo


class Match:
    simi = 0.85

    def __init__(self):
        g = Glo()
        self.screen = "screen" + g.get("screen")

    def imgProcess(self, img, type=0):
        # elif type == 1:
        #     # 自适应阈值
        return cv.adaptiveThreshold(
            img, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 11, 2
        )
        # elif type == 2:
        #     # 去噪处理
        # return cv.fastNlMeansDenoising(img, None, 10, 7, 21)

    def matchTem(self, tem, img=0, simi=0.85):
        if img == 0:
            img = self.screen
        self.simi = simi
        screen = cv.imread("./images/" + img + ".jpg", 0)
        newTem = cv.imread("./images/imgTem/" + tem + ".jpg", 0)
        screen = self.imgProcess(screen)
        newTem = self.imgProcess(newTem)
        result = cv.matchTemplate(screen, newTem, cv.TM_CCORR_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

        if max_val > self.simi:
            w, h = newTem.shape[::-1]
            return (max_loc, (w, h))
        else:
            return 0

    def matchArrTem(self, tem, img=0, simi=0.85, bina=False):
        if img == 0:
            img = self.screen
        self.simi = simi

        screen = cv.imread("./images/" + img + ".jpg", 0)
        screen = self.imgProcess(screen)
        for item in tem:
            newTem = cv.imread("./images/imgTem/" + item + ".jpg", 0)
            newTem = self.imgProcess(newTem)
            result = cv.matchTemplate(screen, newTem, cv.TM_CCORR_NORMED)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
            if max_val > self.simi:
                break

        if max_val > self.simi:
            w, h = newTem.shape[::-1]
            return (max_loc, (w, h))
        else:
            return 0


if __name__ == "__main__":
    Match().matchTem("zh1")
