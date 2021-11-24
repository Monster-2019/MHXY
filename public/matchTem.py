import sys

sys.path.append(".")
sys.path.append("..")
import cv2 as cv
from public.glo import Glo
import config


class Match:
    default_simi = config.GLOBAL_SIMI
    simi = default_simi

    def __init__(self, img = 0):
        g = Glo()
        if img == 0:
            self.screen = "screen" + g.get("screen")
        else:
            self.screen = img

    def imgProcess(self, img, type=0):
        #     自适应阈值
        # return cv.adaptiveThreshold(
        #     img, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 11, 2
        # )
        #   Otsu 二值化
        # ret3, newImg = cv.threshold(img,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
        # ret3, newImg = cv.threshold(img,127,255,cv.THRESH_TRUNC)
        # return newImg
        return img


    def matchTem(self, tem, img=0, simi=simi):
        if img == 0:
            img = self.screen
        if simi and simi != 0:
            self.simi = simi
        s = cv.imread("./images/" + img + ".jpg", 0)
        n = cv.imread("./images/imgTem/" + tem + ".JPG", 0)
        screen = self.imgProcess(s)
        newTem = self.imgProcess(n)
        result = cv.matchTemplate(screen, newTem, cv.TM_CCORR_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

        res = 0
        if tem == 'hd_jyl':
            print(max_val)
        if max_val > self.simi:
            # print('匹配成功', tem, max_val, self.simi, max_loc)
            w, h = newTem.shape[::-1]
            res = (max_loc, (w, h))

        self.simi = self.default_simi

        return res

    def matchArrTem(self, tem, img=0, simi=simi, bina=False):
        if img == 0:
            img = self.screen
        if simi and simi != 0:
            self.simi = simi

        s = cv.imread("./images/" + img + ".jpg", 0)
        screen = self.imgProcess(s)
        for item in tem:
            n = cv.imread("./images/imgTem/" + item + ".jpg", 0)
            newTem = self.imgProcess(n)
            result = cv.matchTemplate(screen, newTem, cv.TM_CCORR_NORMED)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
            if max_val > self.simi:
                # print('匹配成功', item, max_val, self.simi, max_loc)
                break

        res = 0
        if max_val > self.simi:
            w, h = newTem.shape[::-1]
            res = (max_loc, (w, h))

        self.simi = self.default_simi

        return res


if __name__ == "__main__":
    Match().matchTem("zh1")
