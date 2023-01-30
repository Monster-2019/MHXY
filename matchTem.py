import sys

sys.path.append(".")
sys.path.append("..")
import cv2 as cv
import numpy as np
from glo import Glo
from config import base
from cutScreen import CScreen

MIN_MATCH_COUNT = 10
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)
flann = cv.FlannBasedMatcher(index_params, search_params)


class Match:
    default_simi = base.GLOBAL_SIMI
    simi = default_simi

    def __init__(self, img=0):
        g = Glo()
        if not img:
            self.screen = "screen" + g.get("screen")
        else:
            self.screen = img

    def siftMatch(self, tem, img):
        sift = cv.xfeatures2d.SIFT_create()
        kp1, des1 = sift.detectAndCompute(tem, None)
        kp2, des2 = sift.detectAndCompute(img, None)
        matches = flann.knnMatch(des1, des2, k=2)
        good = []
        for m, n in matches:
            if m.distance < 0.7 * n.distance:
                good.append(m)

        if len(good) > MIN_MATCH_COUNT:
            src_pts = np.float32([kp1[m.queryIdx].pt
                                  for m in good]).reshape(-1, 1, 2)
            dst_pts = np.float32([kp2[m.trainIdx].pt
                                  for m in good]).reshape(-1, 1, 2)
            M, mask = cv.findHomography(src_pts, dst_pts, cv.RANSAC, 5.0)
            h, w = tem.shape
            pts = np.float32([[0, 0], [0, h - 1], [w - 1, h - 1],
                              [w - 1, 0]]).reshape(-1, 1, 2)
            dst = cv.perspectiveTransform(pts, M)
            coor = np.int32(np.around(dst)).flatten()
            x1, x2, y1, y2 = set(coor)
            return ((x1, y1), (w, h))

        return 0

    def matchTem(self, tem, img=0, simi=simi):
        if img == 0:
            img = self.screen
        if simi and simi != 0:
            self.simi = simi
        s = cv.imread("./images/" + img + ".jpg", 0)
        n = cv.imread("./images/imgTem/" + tem + ".JPG", 0)
        screen = s
        newTem = n
        result = cv.matchTemplate(screen, newTem, cv.TM_CCORR_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

        res = 0
        if max_val > self.simi:
            w, h = newTem.shape[::-1]
            res = (max_loc, (w, h))

        self.simi = self.default_simi

        return res

    def matchArrTem(self, tem, img=0, simi=simi):
        if img == 0:
            img = self.screen
        if simi and simi != 0:
            self.simi = simi

        s = cv.imread("./images/" + img + ".jpg", 0)
        screen = s
        for item in tem:
            n = cv.imread("./images/imgTem/" + item + ".jpg", 0)
            newTem = n
            result = cv.matchTemplate(screen, newTem, cv.TM_CCORR_NORMED)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
            if max_val > self.simi:
                break

        res = 0
        if max_val > self.simi:
            w, h = newTem.shape[::-1]
            res = (max_loc, (w, h))

        self.simi = self.default_simi

        return res


if __name__ == "__main__":
    CScreen().cutScreen()
    Match().matchTem("zg_zgwc")
