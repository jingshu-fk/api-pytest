import requests
import json
import datetime


class DateEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj,datetime.datetime):
            return obj.strftime("%Y-%m-%d %H:%M:%S")
        else:
            return json.JSONEncoder.default(self,obj)


def request_me(token, host, path, body, method, header, header_change):
    # 封装请求
    url = host + path

    # middle = json.dumps(header)
    # header = json.loads(middle)
    # if header is not None:
    #     header = eval(header)
    if header_change is not None:
        header[header_change] = token
    # print(url)
    # print(body)
    result = None
    response = None
    try:
        if method == 'post':
            response = requests.post(url, data=json.dumps(body, cls=DateEncoder), headers=header)
            print(response.encoding)
            result = response.json()
        elif method == 'get':
            response = requests.get(url, params=body, headers=header)
            result = response.json()
        elif method == 'put':
            response = requests.put(url, data=json.dumps(body, cls=DateEncoder), headers=header)
            result = response.json()
        else:
            print('Unknown method' + body)
    except requests.exceptions.ConnectTimeout as e:
        result = {response.content: 'timeout'}

    return result