import sys
sys.path.append('..')

import config

class Glo:
    obj = {
        'windowClass': config.DEFAULT_CLASS,
        'name': "",
        "level": 0,
        "gold": 0,
        "silver": 0,
        "Till": 0,
        'TeamStatus': False,
        'count': 0,
        'lock': None,
        'z': None,
        'config': None,
        "request_url": "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
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

if __name__ == '__main__':
    g = Glo()