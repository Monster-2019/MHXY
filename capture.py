import win32con
import win32gui
import win32ui

COOR = {
    "btgm": ((412, 258), (135, 25)),
    "name": ((197, 136), (190, 35)),
    "gold": ((106, 634), (130, 24)),
    "silver": ((300, 634), (160, 24)),
    "bb": ((513, 202), (407, 407)),
    "gfbt": ((647, 207), (306, 461)),
    "hy": ((862, 615), (110, 20)),
    "level": ((913, 49), (23, 18))
}

DEFAULT_SAVE_URL = "./images/"
MARGIN_HEIGHT = 39
MARGIN_WIDTH = 17


class CaptureScreen(object):

    def __init__(self, hwnd, screen):
        self.hwnd = hwnd
        self.screen = screen

    def capture(self):
        l, t, r, b = win32gui.GetWindowRect(self.hwnd)

        coor = (0, 0)

        wh = (r - l - MARGIN_WIDTH, b - t - MARGIN_HEIGHT)

        self.save_img(coor, wh)

    def custom_capture(self, key):
        if not key: return

        coor, wh = COOR[key]

        self.save_img(coor, wh)

    def save_img(self, coor, wh):
        x, y = coor
        w, h = wh

        try:
            hwndDC = win32gui.GetDC(self.hwnd)
            mfcDC = win32ui.CreateDCFromHandle(hwndDC)
            saveDC = mfcDC.CreateCompatibleDC()
            saveBitMap = win32ui.CreateBitmap()
            saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
            saveDC.SelectObject(saveBitMap)
            saveDC.BitBlt((0, 0), (w, h), mfcDC, (x, y), win32con.SRCCOPY)
            saveBitMap.SaveBitmapFile(saveDC,
                                    DEFAULT_SAVE_URL + self.screen + '.jpg')
            win32gui.DeleteObject(saveBitMap.GetHandle())
            saveDC.DeleteDC()
            mfcDC.DeleteDC()
            win32gui.ReleaseDC(self.hwnd, hwndDC)
        except Exception as e:
            print('capture ', e)
            pass

    def __call__(self):
        self.capture()

if __name__ == "__main__":
    import win32gui
    hwnd = win32gui.FindWindow(None, "梦幻西游：时空")
    screen = '0'
    capture = CaptureScreen(hwnd, screen)
    capture.custom_capture('name')
    # Match('0').match_tem('dhda')