# encoding:utf-8

#
# # 循环读取用例
# for x in range():
#     x

import requests, json
from data.read_cases import read_xls
from configs.common1 import *


# def app_register(module_name='user'):
#     x = read_xls(module_name)
#     req_param = json.JSONDecoder().decode(x[2])  # unicode格式转换为json格式
#     r = requests.post(url=x[0], json=req_param, headers=base_headers)
#     c = r.json()
#     assert req_param['phone'] == c['info']['phone']

def app_login(module_name='user'):
    x = read_xls(module_name)
    req_param = json.JSONDecoder().decode(x[2])  # unicode格式转换为json格式
    r = requests.post(url=x[0], json=req_param, headers=base_headers)
    c = r.json()
    assert req_param['phone'] == c['info']['phone'], '登录接口错误！'

if __name__ == '__main__':
    app_login()