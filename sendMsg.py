import requests


def SendMsg(message):
    url = 'https://qmsg.zendee.cn/send/ab1b6ba494c7891e83b3940859ab41ad'
    param = {'msg': message}
    requests.post(url, param)

if __name__ == '__main__':
    SendMsg('test')