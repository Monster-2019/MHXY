import requests

# def SendMsg(message):
#     url = 'https://qmsg.zendee.cn/send/ab1b6ba494c7891e83b3940859ab41ad'
#     param = {'msg': message}
#     requests.post(url, param)


def SendMsg(msg):
    url = 'https://push.dongxin.co/v1/message/send'
    params = {
        "token": "54ae34e322deb80bb8d26e70",
        "title": "梦幻西游脚本完成提醒",
        "content": msg,
        "template": "text"
    }
    res = requests.post(url, json=params)
    print(res.json())


if __name__ == '__main__':
    SendMsg('用时1小时')
