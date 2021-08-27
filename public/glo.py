import sys

sys.path.append("..")
import config
import numpy as np
import time
import win32gui


class Glo:
    obj = {
        "windowClass": win32gui.FindWindow(
            "class neox::toolkit::Win32Window0", "《梦幻西游》手游"
        ),
        "screen": "0",
        "name": "",
        "level": 0,
        "gold": 0,
        "silver": 0,
        "TeamStatus": False,
        "count": 0,
        "lock": None,
        "config": None,
        "oldCoor": [],
        "newCoor": [],
    }

    def __init__(self):
        pass

    def setObj(self, paramKey, key, val):
        self.obj[paramKey][key] = val

    def getObj(self, paramKey, key):
        return self.obj[paramKey][key]

    def set(self, key, val):
        self.obj[key] = val

    def get(self, key):
        return self.obj[key]

    # def compare(self):
    #     a = np.array(self.get('oldCoor'))
    #     b = np.array(self.get('newCoor'))
    #     # c = (a==b).all()
    #     c = (a==b).any()
    #     return c

    def compare(self, s=0.01):
        status = True
        sTime = time.time()
        eTime = time.time()
        while eTime - sTime < s:
            a = np.array(self.get("oldCoor"))
            b = np.array(self.get("newCoor"))
            res = (a == b).any()
            if not res:
                status = False
                break

            else:
                eTime = time.time()

        return status


if __name__ == "__main__":
    g = Glo()
