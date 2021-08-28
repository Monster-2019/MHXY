import cv2 as cv
from public.cutScreen import CScreen


def matchTem():
    # s = cv.imread("./images/screen0.jpg", 0)
    s = cv.imread("./images/screen0.jpg", 0)
    # n = cv.imread("./images/imgTem/hd.JPG", 0)
    n = cv.imread("./images/imgTem/sm_sm.JPG", 0)
    screen = cv.adaptiveThreshold(s, 255, cv.ADAPTIVE_THRESH_MEAN_C,
                                  cv.THRESH_BINARY, 11, 2)
    newTem = cv.adaptiveThreshold(n, 255, cv.ADAPTIVE_THRESH_MEAN_C,
                                  cv.THRESH_BINARY, 11, 2)
    ret1, screen = cv.threshold(s,127,255,cv.THRESH_BINARY)
    ret2, newTem = cv.threshold(n,127,255,cv.THRESH_BINARY)

    ret3, screen = cv.threshold(s,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
    ret4, newTem = cv.threshold(n,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)

    w, h = newTem.shape[::-1]

    result = cv.matchTemplate(screen, newTem, cv.TM_CCORR_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

    cv.rectangle(screen, max_loc, (max_loc[0] + w, max_loc[1] + h),
                 (0, 128, 0), 3)

    cv.imshow("custom_blur_demo1", screen)
    cv.imshow("custom_blur_demo", newTem)
    # cv.imshow("custom_blur_demo2", s1)
    # cv.imshow("custom_blur_demo1", n1)
    # cv.imshow("custom_blur_demo3", s2)
    # cv.imshow("custom_blur_demo2", n2)
    cv.waitKey(0)
    cv.destroyAllWindows()

    print(max_val, max_loc, (w, h))
    return (max_loc, (w, h))


def test():
    arr = []
    smList = [
        "sm_mpgx",
        "hd",
        "sm_sm",
        "djjx",
        "dh",
        "dhda",
        "gm",
        "btgm",
        "gfgm",
        "sj",
        "sy",
        "sm_hdwp",
        "sm_rwdh",
        "jm_gb",
    ]
    for item in smList:
        dict = {
            "tem": item,
            "simi": None
        }
        arr.append(dict)
    
    print(arr)

if __name__ == "__main__":
    # import win32gui
    # hwnd = win32gui.FindWindow(None, "《梦幻西游》手游")
    CScreen().cutScreen()
    matchTem()
    # test()
