import cv2 as cv
from public.cutScreen import CScreen


def matchTem():
    # s = cv.imread("./images/screen0.jpg", 0)
    s = cv.imread("./images/screen0.jpg", 0)
    # n = cv.imread("./images/imgTem/hd.JPG", 0)
    n = cv.imread("./images/imgTem/dt_lyc.JPG", 0)
    # ret3, screen = cv.threshold(s,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
    # ret4, newTem = cv.threshold(n,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)

    # ret3, screen = cv.threshold(screen,127,255,cv.THRESH_TRUNC)
    # ret4, newTem = cv.threshold(newTem,127,255,cv.THRESH_TRUNC)
    # screen = cv.Canny(screen,100,200)
    # newTem = cv.Canny(newTem,100,200)

    w, h = n.shape[::-1]

    result = cv.matchTemplate(s, n, cv.TM_CCORR_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

    cv.rectangle(s, max_loc, (max_loc[0] + w, max_loc[1] + h),
                 (0, 128, 0), 3)

    cv.imshow("custom_blur_demo1", s)
    cv.imshow("custom_blur_demo", n)
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
