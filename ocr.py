import base64
import configparser
import urllib

import requests

conf = configparser.ConfigParser()

conf.read('config.ini', encoding='utf-8')

headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'application/json'
}

token_api = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={api_key}&client_secret={secret_key}'.format(
    api_key=conf.get('ocr', 'api_key'),
    secret_key=conf.get('ocr', 'secret_key'))

ocr_api = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic?access_token={access_token}".format(
    access_token=conf.get('ocr', 'access_token'))


def get_token():
    response = requests.get(token_api)
    if response:
        return response.json().get('access_token')


def ocr(img):
    # access_token = get_token()
    payload = 'image=' + get_file_content_as_base64(img, True)
    response = requests.request("POST", ocr_api, headers=headers, data=payload)

    result = []
    for item in response.json().get('words_result'):
        result.append(item.get('words'))

    print(result)
    return result


def get_file_content_as_base64(path, urlencoded=False):
    with open(path, "rb") as f:
        content = base64.b64encode(f.read()).decode("utf8")
        if urlencoded:
            content = urllib.parse.quote_plus(content)
    return content


if __name__ == '__main__':
    ocr('./images/imgTem/ck_max.jpg')