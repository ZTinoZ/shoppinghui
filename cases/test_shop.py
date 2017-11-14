# encoding:utf-8

import requests, json, nose, logging, sys
sys.path.append('..')
from data.read_cases import *
from configs.common1 import *
from nose.tools import nottest, istest, assert_equal


class TestShop:

    @classmethod
    def setup_class(cls):

        global token_headers
        token = get_token(LOGIN_PHONE)
        token_headers = get_token_json(token)
        requests.delete(url='http://192.168.2.200/shop/shopcart', headers=token_headers)  # 清空购物车

        global param2
        x1 = read_xls1('shop')
        param1 = tuple(x1)
        x2 = read_xls2(param1)
        param2 = tuple(x2)

    @classmethod
    def teardown_class(cls):
        requests.delete(url='http://192.168.2.200/shop/shopcart', headers=token_headers)  # 清空购物车

    # APP用户下单
    def test_1_app_place_order(self):
        for i in range(len(param2)):
            # 下单成功用例
            if param2[i][2] == u'APP用户下单_下单成功: ' and param2[i][8] == 'available':
                json_param = read_param(param2[i][4])
                json_param["shopcart"][0]["id"] = get_shopcart_id()
                json_param["leave_message"] = "XXX"
                r = requests.post(url=param2[i][3], json=json_param, headers=token_headers)
                if r.status_code != param2[i][5]:
                    j = r.json()
                    code_msg = (param2[i][2] + j['message']).encode('utf-8')
                    assert_equal(param2[i][5], r.status_code, code_msg)
                else:
                    assert_equal(param2[i][5], r.status_code, r.status_code)

            # 必填参数非空校验用例
            elif param2[i][2] == u'APP用户下单_必填参数非空校验: ' and param2[i][8] == 'available':
                for p in range(9):
                    json_param = list(read_param(param2[i][4]))
                    json_param[p] = ''
                    r = requests.post(url=param2[i][3], json=json_param, headers=token_headers)
                    if r.status_code != param2[i][5]:
                        j = r.json()
                        code_msg = (param2[i][2] + j['message']).encode('utf-8')
                        assert_equal(param2[i][5], r.status_code, code_msg)
                    else:
                        assert_equal(param2[i][5], r.status_code, r.status_code)

            # 购物车id不存在用例
            elif param2[i][2] == u'APP用户下单_购物车id不存在: ' and param2[i][8] == 'available':
                json_param = read_param(param2[i][4])
                r = requests.post(url=param2[i][3], json=json_param, headers=token_headers)
                if r.status_code != param2[i][5]:
                    j = r.json()
                    code_msg = (param2[i][2] + j['message']).encode('utf-8')
                    assert_equal(param2[i][5], r.status_code, code_msg)
                else:
                    assert_equal(param2[i][5], r.status_code, r.status_code)

            # 无token用例
            elif param2[i][2] == u'APP用户下单_无token校验: ' and param2[i][8] == 'available':
                json_param = read_param(param2[i][4])
                json_param["shopcart"][0]["id"] = get_shopcart_id()
                r = requests.post(url=param2[i][3], json=json_param)
                if r.status_code != param2[i][5]:
                    j = r.json()
                    code_msg = (param2[i][2] + j['message']).encode('utf-8')
                    assert_equal(param2[i][5], r.status_code, code_msg)
                else:
                    assert_equal(param2[i][5], r.status_code, r.status_code)

            else:
                continue

    # APP用户订单列表
    @nottest
    def test_2_app_order_list(self):
        for i in range(len(param2)):
            if param2[i][1] == u'APP用户订单列表' and param2[i][8] == 'available':
                r = requests.get(url=param2[i][3], params=param2[i][4], headers=token_headers)
                if r.status_code != param2[i][5]:
                    j = r.json()
                    code_msg = (param2[i][2] + j['message']).encode('utf-8')
                    assert_equal(param2[i][5], r.status_code, code_msg)
                else:
                    assert_equal(param2[i][5], r.status_code, r.status_code)
            else:
                continue

    # APP用户订单详情
    @nottest
    def test_3_app_order_detail(self):
        for i in range(len(param2)):
            # 订单详情获取成功用例
            if param2[i][2] == u'APP用户订单详情_订单详情获取成功：' and param2[i][8] == 'available':
                r = requests.get(url=param2[i][3], headers=token_headers)
                if r.status_code != param2[i][5]:
                    j = r.json()
                    code_msg = (param2[i][2] + j['message']).encode('utf-8')
                    assert_equal(param2[i][5], r.status_code, code_msg)
                else:
                    assert_equal(param2[i][5], r.status_code, r.status_code)

            # 无token用例
            elif param2[i][2] == u'APP用户订单详情_无token校验: ' and param2[i][8] == 'available':
                r = requests.get(url=param2[i][3])
                if r.status_code != param2[i][5]:
                    j = r.json()
                    code_msg = (param2[i][2] + j['message']).encode('utf-8')
                    assert_equal(param2[i][5], r.status_code, code_msg)
                else:
                    assert_equal(param2[i][5], r.status_code, r.status_code)

            else:
                continue

    # APP用户第三方支付
    def test_4_app_paycash(self):
        for i in range(len(param2)):

            # 订单id错误用例
            if param2[i][2] == u'APP用户第三方支付_订单id错误: ' and param2[i][8] == 'available':
                json_param = read_param(param2[i][4])
                incorrect_order_id = get_order() + "!@#"
                url = param2[i][3] + incorrect_order_id
                r = requests.put(url=url, json=json_param, headers=token_headers)
                if r.status_code != param2[i][5]:
                    j = r.json()
                    code_msg = (param2[i][2] + j['message']).encode('utf-8')
                    assert_equal(param2[i][5], r.status_code, code_msg)
                else:
                    assert_equal(param2[i][5], r.status_code, r.status_code)

            # 订单金额错误用例
            elif param2[i][2] == u'APP用户第三方支付_订单金额错误: ' and param2[i][8] == 'available':
                json_param = read_param(param2[i][4])
                json_param["order_amount"] = 0.02
                url = param2[i][3] + get_order()
                r = requests.put(url=url, json=json_param, headers=token_headers)
                if r.status_code != param2[i][5]:
                    j = r.json()
                    code_msg = (param2[i][2] + j['message']).encode('utf-8')
                    assert_equal(param2[i][5], r.status_code, code_msg)
                else:
                    assert_equal(param2[i][5], r.status_code, r.status_code)

            # 运费错误用例
            elif param2[i][2] == u'APP用户第三方支付_运费错误: ' and param2[i][8] == 'available':
                json_param = read_param(param2[i][4])
                json_param["express_cost"] = 2
                url = param2[i][3] + get_order()
                r = requests.put(url=url, json=json_param, headers=token_headers)
                if r.status_code != param2[i][5]:
                    j = r.json()
                    code_msg = (param2[i][2] + j['message']).encode('utf-8')
                    assert_equal(param2[i][5], r.status_code, code_msg)
                else:
                    assert_equal(param2[i][5], r.status_code, r.status_code)

            # 总金额错误用例
            elif param2[i][2] == u'APP用户第三方支付_总金额错误: ' and param2[i][8] == 'available':
                json_param = read_param(param2[i][4])
                json_param["total_amount"] = 100
                url = param2[i][3] + get_order()
                r = requests.put(url=url, json=json_param, headers=token_headers)
                if r.status_code != param2[i][5]:
                    j = r.json()
                    code_msg = (param2[i][2] + j['message']).encode('utf-8')
                    assert_equal(param2[i][5], r.status_code, code_msg)
                else:
                    assert_equal(param2[i][5], r.status_code, r.status_code)

            # 奖励金余额不足用例
            elif param2[i][2] == u'APP用户第三方支付_奖励金余额不足: ' and param2[i][8] == 'available':
                json_param = read_param(param2[i][4])
                json_param["bonus_pay_amount"] = 1
                url = param2[i][3] + get_order()
                r = requests.put(url=url, json=json_param, headers=token_headers)
                if r.status_code != param2[i][5]:
                    j = r.json()
                    code_msg = (param2[i][2] + j['message']).encode('utf-8')
                    assert_equal(param2[i][5], r.status_code, code_msg)
                else:
                    assert_equal(param2[i][5], r.status_code, r.status_code)

            # 账户余额不足用例
            elif param2[i][2] == u'APP用户第三方支付_账户余额不足: ' and param2[i][8] == 'available':
                json_param = read_param(param2[i][4])
                json_param["balance_pay_amount"] = 1
                url = param2[i][3] + get_order()
                r = requests.put(url=url, json=json_param, headers=token_headers)
                if r.status_code != param2[i][5]:
                    j = r.json()
                    code_msg = (param2[i][2] + j['message']).encode('utf-8')
                    assert_equal(param2[i][5], r.status_code, code_msg)
                else:
                    assert_equal(param2[i][5], r.status_code, r.status_code)

            # 支付成功用例
            elif param2[i][2] == u'APP用户第三方支付_支付成功: ' and param2[i][8] == 'available':
                json_param = read_param(param2[i][4])
                url = param2[i][3] + get_order()
                r = requests.put(url=url, json=json_param, headers=token_headers)
                if r.status_code != param2[i][5]:
                    j = r.json()
                    code_msg = (param2[i][2] + j['message']).encode('utf-8')
                    assert_equal(param2[i][5], r.status_code, code_msg)
                else:
                    assert_equal(param2[i][5], r.status_code, r.status_code)

            # 支付状态不匹配用例
            elif param2[i][2] == u'APP用户第三方支付_订单状态不匹配: ' and param2[i][8] == 'available':
                json_param = read_param(param2[i][4])
                url = param2[i][3] + get_order()
                r = requests.put(url=url, json=json_param, headers=token_headers)
                if r.status_code != param2[i][5]:
                    j = r.json()
                    code_msg = (param2[i][2] + j['message']).encode('utf-8')
                    assert_equal(param2[i][5], r.status_code, code_msg)
                else:
                    assert_equal(param2[i][5], r.status_code, r.status_code)

            # 无token用例
            elif param2[i][2] == u'APP用户第三方支付_无token校验: ' and param2[i][8] == 'available':
                json_param = read_param(param2[i][4])
                url = param2[i][3] + get_order()
                r = requests.put(url=url, json=json_param)
                if r.status_code != param2[i][5]:
                    j = r.json()
                    code_msg = (param2[i][2] + j['message']).encode('utf-8')
                    assert_equal(param2[i][5], r.status_code, code_msg)
                else:
                    assert_equal(param2[i][5], r.status_code, r.status_code)

            else:
                continue

if __name__ == '__main__':
    nose.main()
