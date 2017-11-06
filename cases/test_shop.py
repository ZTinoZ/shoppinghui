# encoding:utf-8

import requests, json, nose, logging, sys
sys.path.append('..')
from data.read_cases import *
from configs.common1 import *
from nose.tools import nottest, istest, assert_equal


class TestShop:

    @classmethod
    def setup_class(cls):
        global headers
        token = get_token(login_phone)
        headers = get_token_json(token)
        requests.delete(url='http://192.168.2.200/shop/shopcart', headers=headers)  # 清空购物车

    @classmethod
    def teardown_class(cls):
        requests.delete(url='http://192.168.2.200/shop/shopcart', headers=headers)  # 清空购物车

    # APP用户下单
    def test_1_app_order(self):
        x1 = read_xls1('shop')
        param1 = tuple(x1)
        x2 = read_xls2(param1)
        param2 = tuple(x2)
        for i in range(len(param2)):

            # 下单成功用例
            if param2[i][2] == u'APP用户下单_下单成功: ' and param2[i][8] == 'available':
                json_param = read_param(param2[i][4])
                json_param["shopcart"][0]["id"] = get_shopcart_id()
                headers = correlation(param2[i][7], get_token(login_phone))
                r = requests.post(url=param2[i][3], json=json_param, headers=headers)
                code_msg = param2[i][2].encode('utf-8') + '用例失败（状态码不匹配）！'
                assert_equal(param2[i][5], r.status_code, code_msg)

            # 必填参数非空校验用例
            elif param2[i][1] == u'APP用户下单: ' and param2[i][4] == u'app_order_non_null.txt' and param2[i][8] == 'available':
                for p in range(9):
                    json_param = list(read_param(param2[i][4]))
                    json_param[p] = ''
                    headers = correlation(param2[i][7], get_token(login_phone))
                    r = requests.post(url=param2[i][3], json=json_param, headers=headers)
                    code_msg = param2[i][2].encode('utf-8') + '用例失败（状态码不匹配）！'
                    assert_equal(param2[i][5], r.status_code, code_msg)

            # 购物车id不存在用例
            elif param2[i][2] == u'APP用户下单_购物车id不存在: ' and param2[i][8] == 'available':
                json_param = read_param(param2[i][4])
                headers = correlation(param2[i][7], get_token(login_phone))
                r = requests.post(url=param2[i][3], json=json_param, headers=headers)
                code_msg = param2[i][2].encode('utf-8') + '用例失败（状态码不匹配）！'
                assert_equal(param2[i][5], r.status_code, code_msg)

            # 无token用例
            elif param2[i][2] == u'APP用户下单_无token校验: ' and param2[i][8] == 'available':
                json_param = read_param(param2[i][4])
                json_param["shopcart"][0]["id"] = get_shopcart_id()
                r = requests.post(url=param2[i][3], json=json_param)
                code_msg = param2[i][2].encode('utf-8') + '用例失败（状态码不匹配）！'
                assert_equal(param2[i][5], r.status_code, code_msg)

            else:
                continue

if __name__ == '__main__':
    nose.main()
