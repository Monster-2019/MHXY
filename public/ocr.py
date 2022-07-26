import sys
sys.path.append('.')
sys.path.append('..')
import requests
import base64
from public.glo import Glo
from time import sleep
from retrying import retry
from public.log import log

# 获取授权token
# 一个月一次
#  上次时间：2031/11/29

def getToken():
    url = "https://aip.baidubce.com/oauth/2.0/token"

    param = {
        "grant_type": "client_credentials",
        "client_id": "C4dGEfVil96KbN2AZsEszSNF",
        "client_secret": "Bx7Ch1iuGPBeYDyb5VQgaunIP9fCPRXz"
    }

    res = requests.get(url, param)  
    token = ""
    if res: 
        token = res.json()['access_token']
        print(token)

def retry_if_result_none(result):
    if result is None:
        log('请求失败，重试', True)
    return result is None

class OCR():
    count = 0

    def __init__(self):
        self.g = Glo()

    @retry(retry_on_result=retry_if_result_none, stop_max_attempt_number=2, wait_random_min=1000, wait_random_max=2000)
    def ocr(self):
        result = ""
        token = "24.b05f7ca11035cc875d7f157dcacaaeb4.2592000.1640780385.282335-18542329"
        # request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"
        # request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"

        f = open('./images/screen' + self.g.get('screen') +'.jpg',  'rb')
        img = base64.b64encode(f.read())

        request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic?access_token=" + token
        headers = {'content-type': 'application/x-www-form-urlencoded'}
        param = {"image": img}
        res = requests.post(request_url, data=param, headers=headers)
        count = self.g.get('count') + 1
        self.g.set('count', count)
        res = res.json()
        if len(res['words_result']) > 0:
            # print(res['words_result'][0]['words'])
            return res['words_result'][0]['words']
        else:
            return None
            
if __name__ == '__main__':
    getToken()
    # OCR()ocr()