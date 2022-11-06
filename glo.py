import sys

sys.path.append(".")
sys.path.append("..")
import numpy as np
import win32gui


class Glo:
    obj = {
        "windowClass": win32gui.FindWindow(None, "《梦幻西游》手游"),
        "screen": "0",
        "name": "",
        "level": 0,
        "gold": 0,
        "silver": 0,
        "TeamStatus": False,
        "lock": None,
        "config": None,
        "oldCoor": [],
        "newCoor": [],
        "hyd": 0
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

    def compare(self):
        a = np.array(self.get("oldCoor"))
        b = np.array(self.get("newCoor"))
        return (a == b).sum() >= 3

if __name__ == "__main__":
    g = Glo()
