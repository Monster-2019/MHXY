import cv2 as cv

MIN_MATCH_COUNT = 10
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)
flann = cv.FlannBasedMatcher(index_params, search_params)


class Match(object):
    default_simi = 0.99
    default_feature_count = MIN_MATCH_COUNT

    def __init__(self, screen):
        self.screen = screen

    def match_tem(self, tem, screen=None, simi=default_simi, debug=False, **kwds):
        s = screen or self.screen
        img1 = cv.imread("./images/" + s + ".jpg", 0)
        img2 = cv.imread("./images/imgTem/" + tem + ".jpg", 0)
        result = cv.matchTemplate(img1, img2, cv.TM_CCORR_NORMED)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

        # if tem == 'btn_sh':
        #     cv.imshow('img1', img1)
        #     cv.imshow('img2', img2)
        #     cv.waitKey(0)
        #     cv.destroyAllWindows()

        if debug:
            print(tem, max_val, max_loc, simi)
        if max_val > simi:
            w, h = img2.shape[::-1]
            x, y = max_loc
            return (x, y, w, h)

        return ()

    def match_tem_list(self, tem_list, screen=None, simi=default_simi, **kwds):
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

    def __call__(self, tem, **kwds):
        return self.match_tem(tem, **kwds)


if __name__ == "__main__":
    import win32gui

    from capture import CaptureScreen
    hwnd = win32gui.FindWindow(None, "梦幻西游：时空")
    screen = '0'
    capture = CaptureScreen(hwnd, screen)
    capture()
    Match('0').match_tem('rw_jyl', debug=True)
    # Match('0').match_tem('dhda')