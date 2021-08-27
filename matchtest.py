import cv2 as cv


def matchTem():
    # s = cv.imread("./images/screen0.jpg", 0)
    s = cv.imread("./images/screen0.jpg", 0)
    # n = cv.imread("./images/imgTem/hd.JPG", 0)
    n = cv.imread("./target1.png", 0)
    screen = cv.adaptiveThreshold(
        s, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 11, 2
    )
    newTem = cv.adaptiveThreshold(
        n, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 11, 2
    )
    w, h = newTem.shape[::-1]


    result = cv.matchTemplate(screen, newTem, cv.TM_CCORR_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

    cv.rectangle(screen, max_loc, (max_loc[0] + w, max_loc[1] + h), (0,128,0), 3)

    cv.imshow("custom_blur_demo1", screen)
    cv.imshow("custom_blur_demo", newTem)
    cv.waitKey(0)
    cv.destroyAllWindows()

    print(min_val, max_val, min_loc, max_loc)
    return (max_loc, (w, h))


if __name__ == "__main__":
    matchTem()
