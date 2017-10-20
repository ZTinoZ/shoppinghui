# encoding:utf-8

#
# # 循环读取用例
# for x in range():
#     x

import requests, json
from data.read_cases import *
from configs.common1 import *


# def app_register(module_name='user'):
#     x = read_xls(module_name)
#     req_param = json.JSONDecoder().decode(x[2])
#     r = requests.post(url=x[0], json=req_param, headers=base_headers)
#     c = r.json()
#     assert req_param['phone'] == c['info']['phone']

def app_login(module_name='user'):
    x1 = read_xls1(module_name)
    param1 = tuple(x1)
    x2 = read_xls2(param1)
    param2 = tuple(x2)
    for i in range(5, 6):
        json_param = json.JSONDecoder().decode(param2[i][2])
        r = requests.post(url=param2[i][1], json=json_param, headers=base_headers)
        c = r.json()
        assert param2[i][3] == r.status_code

if __name__ == '__main__':
    app_login()
