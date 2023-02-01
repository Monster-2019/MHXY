import cv2 as cv
import numpy as np

from config import base

MIN_MATCH_COUNT = 10
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)
flann = cv.FlannBasedMatcher(index_params, search_params)


class Match(object):
    default_simi = base.GLOBAL_SIMI
    default_feature_count = MIN_MATCH_COUNT

    def __init__(self, screen):
        self.screen = screen

    def match_tem(self, tem, screen, simi=default_simi):
        s = screen or self.screen
        img1 = cv.imread("./images/" + s + ".jpg", 0)
        img2 = cv.imread("./images/imgTem/" + tem + ".jpg", 0)
        result = cv.matchTemplate(img1, img2, cv.TM_CCORR_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

        if max_val > simi:
            w, h = img2.shape[::-1]
            x, y = max_loc
            return (x, y, w, h)

        return ()

    def match_tem_list(self, tem_list, screen, simi=default_simi):
        # s = screen or self.screen
        # img1 = cv.imread("./images/" + s + ".jpg", 0)

        for tem in tem_list:
            result = self.match_tem(tem, screen, simi)
            if result:
                return result
            # img2 = cv.imread("./images/imgTem/" + tem + ".jpg", 0)
            # result = cv.matchTemplate(img1, img2, cv.TM_CCORR_NORMED)
            # min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
            # if max_val > simi:
            # w, h = img2.shape[::-1]
            # x, y = max_loc
            # return (x, y, w, h)

        return ()

    def match_feature(self, tem, screen, count=default_feature_count):
        s = screen or self.screen
        img1 = cv.imread("./images/imgTem/" + tem + ".jpg", 0)
        img2 = cv.imread("./images/" + s + ".jpg", 0)

        sift = cv.xfeatures2d.SIFT_create()
        kp1, des1 = sift.detectAndCompute(img1, None)
        kp2, des2 = sift.detectAndCompute(img2, None)
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
            return (x1, y1, w, h)

        return ()