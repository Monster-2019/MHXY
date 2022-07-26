import requests

# def SendMsg(message):
#     url = 'https://qmsg.zendee.cn/send/ab1b6ba494c7891e83b3940859ab41ad'
#     param = {'msg': message}
#     requests.post(url, param)


def SendMsg(msg):
    url = 'http://www.pushplus.plus/send'
    params = {
        "token": "342994c7162c41dc98a894a0ae133bda",
        "title": "梦幻西游脚本完成提醒",
        "content": msg
    }
    requests.post(url, params)


if __name__ == '__main__':
    SendMsg('用时1小时')
