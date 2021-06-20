import requests


def SendMsg(message):
    url = 'https://sctapi.ftqq.com/SCT37678TkfAexmUvgQO2iJLCmQfLCq7o.send'
    msg = message
    param = {'title': msg}
    requests.post(url, param)