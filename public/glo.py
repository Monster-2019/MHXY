import sys
sys.path.append('..')
import config
import numpy as np

class Glo:
    obj = {
        'windowClass': config.DEFAULT_CLASS,
        'name': "",
        "level": 0,
        "gold": 0,
        "silver": 0,
        'TeamStatus': False,
        'count': 0,
        'lock': None,
        'config': None,
        'oldCoor': [],
        'newCoor': []
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
        a = np.array(self.get('oldCoor'))
        b = np.array(self.get('newCoor'))
        # c = (a==b).all()
        c = (a==b).any()
        return c

if __name__ == '__main__':
    g = Glo()