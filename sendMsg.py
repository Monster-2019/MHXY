import requests

def SendMsg(message):
    url = 'https://sc.ftqq.com/SCU69656T782d340ca550c446fba0708c1436e3af5e2aadb811f2f.send'
    msg = message
    param = {
        'text': msg
    }
    requests.post(url, param)