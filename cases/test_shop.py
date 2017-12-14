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
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s')
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
    @nottest
    def test01_app_place_order(self):
        for i in range(len(param2)):

            # 下单成功用例
            if param2[i][2] == u'APP用户下单_下单成功: ' and param2[i][9] == 'available':
                for j in range(2):  # 下两笔单，用于之后的两种支付方式
                    json_param = read_param(param2[i][5])
                    json_param["shopcart"][0]["id"] = get_shopcart_id()
                    json_param["leave_message"] = "XXX"
                    r = requests.request(method=param2[i][4], url=param2[i][3], json=json_param, headers=token_headers)
                    if r.status_code != param2[i][6]:
                        j = r.json()
                        code_msg = (param2[i][2] + j['message']).encode('utf-8')
                        assert_equal(param2[i][6], r.status_code, code_msg)
                    else:
                        logging.info(u'\n%s测试通过！' % param2[i][2])

            # 商品数量错误用例
            elif param2[i][2] == u'APP用户下单_商品数量错误: ' and param2[i][9] == 'available':
                json_param = read_param(param2[i][5])
                json_param["count"] = 2
                r = requests.request(method=param2[i][4], url=param2[i][3], json=json_param, headers=token_headers)
                if r.status_code != param2[i][6]:
                    j = r.json()
                    code_msg = (param2[i][2] + j['message']).encode('utf-8')
                    assert_equal(param2[i][6], r.status_code, code_msg)
                else:
                    logging.info(u'\n%s测试通过！' % param2[i][2])

            # 运费错误用例
            elif param2[i][2] == u'APP用户下单_运费错误: ' and param2[i][9] == 'available':
                json_param = read_param(param2[i][5])
                json_param["company_express"] = 2
                r = requests.request(method=param2[i][4], url=param2[i][3], json=json_param, headers=token_headers)
                if r.status_code != param2[i][6]:
                    j = r.json()
                    code_msg = (param2[i][2] + j['message']).encode('utf-8')
                    assert_equal(param2[i][6], r.status_code, code_msg)
                else:
                    logging.info(u'\n%s测试通过！' % param2[i][2])

            # 总金额错误用例
            elif param2[i][2] == u'APP用户下单_商品数量错误: ' and param2[i][9] == 'available':
                json_param = read_param(param2[i][5])
                json_param["order_amount"] = 0.02
                r = requests.request(method=param2[i][4], url=param2[i][3], json=json_param, headers=token_headers)
                if r.status_code != param2[i][6]:
                    j = r.json()
                    code_msg = (param2[i][2] + j['message']).encode('utf-8')
                    assert_equal(param2[i][6], r.status_code, code_msg)
                else:
                    logging.info(u'\n%s测试通过！' % param2[i][2])

            # 必填参数非空校验用例
            elif param2[i][2] == u'APP用户下单_必填参数非空校验: ' and param2[i][9] == 'available':
                for p in range(10):  # 十个参数，循环十次，每次赋给相应的参数空值，来模拟必填参数为空的情况
                    json_param = list(read_param(param2[i][5]))
                    json_param[p] = ""
                    print(json_param)
                    r = requests.request(method=param2[i][4], url=param2[i][3], json=json_param, headers=token_headers)
                    print(r.status_code)
                    if r.status_code != param2[i][6]:
                        j = r.json()
                        code_msg = (param2[i][2] + j['message']).encode('utf-8')
                        assert_equal(param2[i][6], r.status_code, code_msg)
                    else:
                        logging.info(u'\n%s测试通过！' % param2[i][2])

            # 购物车id不存在用例
            elif param2[i][2] == u'APP用户下单_购物车id不存在: ' and param2[i][9] == 'available':
                json_param = read_param(param2[i][5])
                r = requests.request(method=param2[i][4], url=param2[i][3], json=json_param, headers=token_headers)
                if r.status_code != param2[i][6]:
                    j = r.json()
                    code_msg = (param2[i][2] + j['message']).encode('utf-8')
                    assert_equal(param2[i][6], r.status_code, code_msg)
                else:
                    logging.info(u'\n%s测试通过！' % param2[i][2])

            # 无token用例
            elif param2[i][2] == u'APP用户下单_无token校验: ' and param2[i][9] == 'available':
                json_param = read_param(param2[i][5])
                json_param["shopcart"][0]["id"] = get_shopcart_id()
                r = requests.request(method=param2[i][4], url=param2[i][3], json=json_param)
                if r.status_code != param2[i][6]:
                    j = r.json()
                    code_msg = (param2[i][2] + j['message']).encode('utf-8')
                    assert_equal(param2[i][6], r.status_code, code_msg)
                else:
                    logging.info(u'\n%s测试通过！' % param2[i][2])

            else:
                continue

    # APP用户订单列表
    @nottest
    def test02_app_order_list(self):
        for i in range(len(param2)):
            if param2[i][1] == u'APP用户订单列表' and param2[i][9] == 'available':
                if param2[i][8] == 'need_token':
                    r = requests.request(method=param2[i][4], url=param2[i][3], params=param2[i][5], headers=token_headers)
                else:
                    r = requests.request(method=param2[i][4], url=param2[i][3])
                if r.status_code != param2[i][6]:
                    j = r.json()
                    code_msg = (param2[i][2] + j['message']).encode('utf-8')
                    assert_equal(param2[i][6], r.status_code, code_msg)
                else:
                    logging.info(u'\n%s测试通过！' % param2[i][2])
            else:
                continue

    # APP用户订单详情
    @nottest
    def test03_app_order_detail(self):
        for i in range(len(param2)):
            if param2[i][1] == u'APP用户订单详情' and param2[i][9] == 'available':
                if param2[i][8] == 'need_token':
                    r = requests.request(method=param2[i][4], url=param2[i][3], headers=token_headers)
                else:
                    r = requests.request(method=param2[i][4], url=param2[i][3])
                if r.status_code != param2[i][6]:
                    j = r.json()
                    code_msg = (param2[i][2] + j['message']).encode('utf-8')
                    assert_equal(param2[i][6], r.status_code, code_msg)
                else:
                    logging.info(u'\n%s测试通过！' % param2[i][2])
            else:
                continue

    # APP用户第三方支付
    @nottest
    def test04_app_paycash(self):
        for i in range(len(param2)):

            # 订单id错误用例
            if param2[i][2] == u'APP用户第三方支付_订单id错误: ' and param2[i][9] == 'available':
                json_param = json.JSONDecoder().decode(param2[i][5])
                incorrect_order_id = get_order0() + "!@#"
                url = param2[i][3] + incorrect_order_id
                r = requests.request(method=param2[i][4], url=url, json=json_param, headers=token_headers)
                if r.status_code != param2[i][6]:
                    j = r.json()
                    code_msg = (param2[i][2] + j['message']).encode('utf-8')
                    assert_equal(param2[i][6], r.status_code, code_msg)
                else:
                    logging.info(u'\n%s测试通过！' % param2[i][2])

            # 订单金额错误用例
            elif param2[i][2] == u'APP用户第三方支付_订单金额错误: ' and param2[i][9] == 'available':
                json_param = json.JSONDecoder().decode(param2[i][5])
                url = param2[i][3] + get_order0()
                r = requests.request(method=param2[i][4], url=url, json=json_param, headers=token_headers)
                if r.status_code != param2[i][6]:
                    j = r.json()
                    code_msg = (param2[i][2] + j['message']).encode('utf-8')
                    assert_equal(param2[i][6], r.status_code, code_msg)
                else:
                    logging.info(u'\n%s测试通过！' % param2[i][2])

            # 运费错误用例
            elif param2[i][2] == u'APP用户第三方支付_运费错误: ' and param2[i][9] == 'available':
                json_param = json.JSONDecoder().decode(param2[i][5])
                url = param2[i][3] + get_order0()
                r = requests.request(method=param2[i][4], url=url, json=json_param, headers=token_headers)
                if r.status_code != param2[i][6]:
                    j = r.json()
                    code_msg = (param2[i][2] + j['message']).encode('utf-8')
                    assert_equal(param2[i][6], r.status_code, code_msg)
                else:
                    logging.info(u'\n%s测试通过！' % param2[i][2])

            # 总金额错误用例
            elif param2[i][2] == u'APP用户第三方支付_总金额错误: ' and param2[i][9] == 'available':
                json_param = json.JSONDecoder().decode(param2[i][5])
                url = param2[i][3] + get_order0()
                r = requests.request(method=param2[i][4], url=url, json=json_param, headers=token_headers)
                if r.status_code != param2[i][6]:
                    j = r.json()
                    code_msg = (param2[i][2] + j['message']).encode('utf-8')
                    assert_equal(param2[i][6], r.status_code, code_msg)
                else:
                    logging.info(u'\n%s测试通过！' % param2[i][2])

            # 奖励金余额不足用例
            elif param2[i][2] == u'APP用户第三方支付_奖励金余额不足: ' and param2[i][9] == 'available':
                json_param = json.JSONDecoder().decode(param2[i][5])
                url = param2[i][3] + get_order0()
                r = requests.request(method=param2[i][4], url=url, json=json_param, headers=token_headers)
                if r.status_code != param2[i][6]:
                    j = r.json()
                    code_msg = (param2[i][2] + j['message']).encode('utf-8')
                    assert_equal(param2[i][6], r.status_code, code_msg)
                else:
                    logging.info(u'\n%s测试通过！' % param2[i][2])

            # 账户余额不足用例
            elif param2[i][2] == u'APP用户第三方支付_账户余额不足: ' and param2[i][9] == 'available':
                json_param = json.JSONDecoder().decode(param2[i][5])
                url = param2[i][3] + get_order0()
                r = requests.request(method=param2[i][4], url=url, json=json_param, headers=token_headers)
                if r.status_code != param2[i][6]:
                    j = r.json()
                    code_msg = (param2[i][2] + j['message']).encode('utf-8')
                    assert_equal(param2[i][6], r.status_code, code_msg)
                else:
                    logging.info(u'\n%s测试通过！' % param2[i][2])

            # 必填参数非空校验用例
            elif param2[i][2] == u'APP用户第三方支付_必填参数非空校验: ' and param2[i][9] == 'available':
                for p in range(4):  # 四个参数，循环四次，每次赋给相应的参数空值，来模拟必填参数为空的情况
                    json_param = json.JSONDecoder().decode(param2[i][5])
                    json_param[p] = ""
                    url = param2[i][3] + get_order0()
                    r = requests.request(method=param2[i][4], url=url, json=json_param, headers=token_headers)
                    if r.status_code != param2[i][6]:
                        j = r.json()
                        code_msg = (param2[i][2] + j['message']).encode('utf-8')
                        assert_equal(param2[i][6], r.status_code, code_msg)
                    else:
                        logging.info(u'\n%s测试通过！' % param2[i][2])

            # 支付成功用例
            elif param2[i][2] == u'APP用户第三方支付_支付成功: ' and param2[i][9] == 'available':
                json_param = json.JSONDecoder().decode(param2[i][5])
                url = param2[i][3] + get_order0()
                r = requests.request(method=param2[i][4], url=url, json=json_param, headers=token_headers)
                if r.status_code != param2[i][6]:
                    j = r.json()
                    code_msg = (param2[i][2] + j['message']).encode('utf-8')
                    assert_equal(param2[i][6], r.status_code, code_msg)
                else:
                    logging.info(u'\n%s测试通过！' % param2[i][2])

            # 支付状态不匹配用例
            elif param2[i][2] == u'APP用户第三方支付_订单状态不匹配: ' and param2[i][9] == 'available':
                json_param = json.JSONDecoder().decode(param2[i][5])
                url = param2[i][3] + get_order1()
                r = requests.request(method=param2[i][4], url=url, json=json_param, headers=token_headers)
                if r.status_code != param2[i][6]:
                    j = r.json()
                    code_msg = (param2[i][2] + j['message']).encode('utf-8')
                    assert_equal(param2[i][6], r.status_code, code_msg)
                else:
                    logging.info(u'\n%s测试通过！' % param2[i][2])

            # 无token用例
            elif param2[i][2] == u'APP用户第三方支付_无token校验: ' and param2[i][9] == 'available':
                json_param = json.JSONDecoder().decode(param2[i][5])
                url = param2[i][3] + get_order1()
                r = requests.request(method=param2[i][4], url=url, json=json_param)
                if r.status_code != param2[i][6]:
                    j = r.json()
                    code_msg = (param2[i][2] + j['message']).encode('utf-8')
                    assert_equal(param2[i][6], r.status_code, code_msg)
                else:
                    logging.info(u'\n%s测试通过！' % param2[i][2])

            else:
                continue

    # APP用户非第三方支付
    @nottest
    def test05_app_pay(self):
        for i in range(len(param2)):

            # 订单id错误用例
            if param2[i][2] == u'APP用户非第三方支付_订单id错误: ' and param2[i][9] == 'available':
                json_param = json.JSONDecoder().decode(param2[i][5])
                incorrect_order_id = get_order0() + "!@#"
                url = param2[i][3] + incorrect_order_id
                r = requests.request(method=param2[i][4], url=url, json=json_param, headers=token_headers)
                if r.status_code != param2[i][6]:
                    j = r.json()
                    code_msg = (param2[i][2] + j['message']).encode('utf-8')
                    assert_equal(param2[i][6], r.status_code, code_msg)
                else:
                    logging.info(u'\n%s测试通过！' % param2[i][2])

            # 订单金额错误用例
            elif param2[i][2] == u'APP用户非第三方支付_订单金额错误: ' and param2[i][9] == 'available':
                json_param = json.JSONDecoder().decode(param2[i][5])
                url = param2[i][3] + get_order0()
                r = requests.request(method=param2[i][4], url=url, json=json_param, headers=token_headers)
                if r.status_code != param2[i][6]:
                    j = r.json()
                    code_msg = (param2[i][2] + j['message']).encode('utf-8')
                    assert_equal(param2[i][6], r.status_code, code_msg)
                else:
                    logging.info(u'\n%s测试通过！' % param2[i][2])

            # 运费错误用例
            elif param2[i][2] == u'APP用户非第三方支付_运费错误: ' and param2[i][9] == 'available':
                json_param = json.JSONDecoder().decode(param2[i][5])
                url = param2[i][3] + get_order0()
                r = requests.request(method=param2[i][4], url=url, json=json_param, headers=token_headers)
                if r.status_code != param2[i][6]:
                    j = r.json()
                    code_msg = (param2[i][2] + j['message']).encode('utf-8')
                    assert_equal(param2[i][6], r.status_code, code_msg)
                else:
                    logging.info(u'\n%s测试通过！' % param2[i][2])

            # 总金额错误用例
            elif param2[i][2] == u'APP用户非第三方支付_总金额错误: ' and param2[i][9] == 'available':
                json_param = json.JSONDecoder().decode(param2[i][5])
                url = param2[i][3] + get_order0()
                r = requests.request(method=param2[i][4], url=url, json=json_param, headers=token_headers)
                if r.status_code != param2[i][6]:
                    j = r.json()
                    code_msg = (param2[i][2] + j['message']).encode('utf-8')
                    assert_equal(param2[i][6], r.status_code, code_msg)
                else:
                    logging.info(u'\n%s测试通过！' % param2[i][2])

            # 奖励金余额不足用例
            elif param2[i][2] == u'APP用户非第三方支付_奖励金余额不足: ' and param2[i][9] == 'available':
                json_param = json.JSONDecoder().decode(param2[i][5])
                url = param2[i][3] + get_order0()
                r = requests.request(method=param2[i][4], url=url, json=json_param, headers=token_headers)
                if r.status_code != param2[i][6]:
                    j = r.json()
                    code_msg = (param2[i][2] + j['message']).encode('utf-8')
                    assert_equal(param2[i][6], r.status_code, code_msg)
                else:
                    logging.info(u'\n%s测试通过！' % param2[i][2])

            # 账户余额不足用例
            elif param2[i][2] == u'APP用户非第三方支付_账户余额不足: ' and param2[i][9] == 'available':
                json_param = json.JSONDecoder().decode(param2[i][5])
                url = param2[i][3] + get_order0()
                r = requests.request(method=param2[i][4], url=url, json=json_param, headers=token_headers)
                if r.status_code != param2[i][6]:
                    j = r.json()
                    code_msg = (param2[i][2] + j['message']).encode('utf-8')
                    assert_equal(param2[i][6], r.status_code, code_msg)
                else:
                    logging.info(u'\n%s测试通过！' % param2[i][2])

            # 必填参数非空校验用例
            elif param2[i][2] == u'APP用户非第三方支付_必填参数非空校验: ' and param2[i][9] == 'available':
                for p in range(4):  # 四个参数，循环四次，每次赋给相应的参数空值，来模拟必填参数为空的情况
                    json_param = json.JSONDecoder().decode(param2[i][5])
                    json_param[p] = ""
                    url = param2[i][3] + get_order0()
                    r = requests.request(method=param2[i][4], url=url, json=json_param, headers=token_headers)
                    if r.status_code != param2[i][6]:
                        j = r.json()
                        code_msg = (param2[i][2] + j['message']).encode('utf-8')
                        assert_equal(param2[i][6], r.status_code, code_msg)
                    else:
                        logging.info(u'\n%s测试通过！' % param2[i][2])

            # 支付成功用例
            elif param2[i][2] == u'APP用户非第三方支付_支付成功: ' and param2[i][9] == 'available':
                json_param = json.JSONDecoder().decode(param2[i][5])
                url = param2[i][3] + get_order0()
                r = requests.request(method=param2[i][4], url=url, json=json_param, headers=token_headers)
                if r.status_code != param2[i][6]:
                    j = r.json()
                    code_msg = (param2[i][2] + j['message']).encode('utf-8')
                    assert_equal(param2[i][6], r.status_code, code_msg)
                else:
                    logging.info(u'\n%s测试通过！' % param2[i][2])

            # 支付状态不匹配用例
            elif param2[i][2] == u'APP用户非第三方支付_订单状态不匹配: ' and param2[i][9] == 'available':
                json_param = json.JSONDecoder().decode(param2[i][5])
                url = param2[i][3] + get_order1()
                r = requests.request(method=param2[i][4], url=url, json=json_param, headers=token_headers)
                if r.status_code != param2[i][6]:
                    j = r.json()
                    code_msg = (param2[i][2] + j['message']).encode('utf-8')
                    assert_equal(param2[i][6], r.status_code, code_msg)
                else:
                    logging.info(u'\n%s测试通过！' % param2[i][2])

            # 无token用例
            elif param2[i][2] == u'APP用户非第三方支付_无token校验: ' and param2[i][9] == 'available':
                json_param = json.JSONDecoder().decode(param2[i][5])
                url = param2[i][3] + get_order1()
                r = requests.request(method=param2[i][4], url=url, json=json_param)
                if r.status_code != param2[i][6]:
                    j = r.json()
                    code_msg = (param2[i][2] + j['message']).encode('utf-8')
                    assert_equal(param2[i][6], r.status_code, code_msg)
                else:
                    logging.info(u'\n%s测试通过！' % param2[i][2])

            else:
                continue

    # APP用户购物车列表
    @nottest
    def test06_app_shopcart_list(self):
        for i in range(len(param2)):
            if param2[i][1] == u'APP用户购物车列表' and param2[i][9] == 'available':
                get_shopcart_id()  # 添加购物车
                if param2[i][8] == 'need_token':
                    r = requests.request(method=param2[i][4], url=param2[i][3], params=param2[i][5], headers=token_headers)
                else:
                    r = requests.request(method=param2[i][4], url=param2[i][3], params=param2[i][5])
                j = r.json()
                if r.status_code != param2[i][6]:
                    code_msg = (param2[i][2] + j['message']).encode('utf-8')
                    assert_equal(param2[i][6], r.status_code, code_msg)
                elif param2[i][7] != 'none' and j["count"] != param2[i][7]:
                    code_msg = (param2[i][2] + j['message']).encode('utf-8')
                    assert_equal(param2[i][7], j["count"], code_msg)
                else:
                    logging.info(u'\n%s测试通过！' % param2[i][2])
                    requests.delete(url='http://192.168.2.200/shop/shopcart', headers=token_headers)  # 删除购物车（调用接口）
            else:
                continue

    # APP用户购物车添加
    @nottest
    def test07_app_shopcart_add(self):
        for i in range(len(param2)):
            if param2[i][1] == u'APP用户购物车添加' and param2[i][9] == 'available':
                json_param = json.JSONDecoder().decode(param2[i][5])
                if param2[i][8] == 'need_token':
                    r = requests.request(method=param2[i][4], url=param2[i][3], json=json_param, headers=token_headers)
                else:
                    r = requests.request(method=param2[i][4], url=param2[i][3], json=json_param)
                if r.status_code != param2[i][6]:
                    j = r.json()
                    code_msg = (param2[i][2] + j['message']).encode('utf-8')
                    assert_equal(param2[i][6], r.status_code, code_msg)
                else:
                    logging.info(u'\n%s测试通过！' % param2[i][2])
            else:
                continue

    # APP用户购物车修改
    @nottest
    def test08_app_shopcart_add(self):
        for i in range(len(param2)):
            if param2[i][1] == u'APP用户购物车修改' and param2[i][9] == 'available':
                json_param = json.JSONDecoder().decode(param2[i][5])
                url = param2[i][3] + get_shopcart_id()
                if param2[i][8] == 'need_token':
                    r = requests.request(method=param2[i][4], url=url, json=json_param, headers=token_headers)
                else:
                    r = requests.request(method=param2[i][4], url=url, json=json_param)
                if r.status_code != param2[i][6]:
                    j = r.json()
                    print(url)
                    code_msg = (param2[i][2] + j['message']).encode('utf-8')
                    assert_equal(param2[i][6], r.status_code, code_msg)
                else:
                    logging.info(u'\n%s测试通过！' % param2[i][2])
            else:
                continue

    # APP用户购物车删除
    @nottest
    def test09_app_shopcart_delete(self):
        for i in range(len(param2)):
            if param2[i][1] == u'APP用户购物车删除' and param2[i][9] == 'available':
                if param2[i][8] == 'need_token':
                    r = requests.request(method=param2[i][4], url=param2[i][3], headers=token_headers)
                else:
                    r = requests.request(method=param2[i][4], url=param2[i][3])
                if r.status_code != param2[i][6]:
                    j = r.json()
                    code_msg = (param2[i][2] + j['message']).encode('utf-8')
                    assert_equal(param2[i][6], r.status_code, code_msg)
                else:
                    logging.info(u'\n%s测试通过！' % param2[i][2])
            else:
                continue

    # APP用户购物车清空
    @nottest
    def test10_app_shopcart_empty(self):
        for i in range(len(param2)):
            if param2[i][1] == u'APP用户购物车清空' and param2[i][9] == 'available':
                if param2[i][8] == 'need_token':
                    r = requests.request(method=param2[i][4], url=param2[i][3], headers=token_headers)
                else:
                    r = requests.request(method=param2[i][4], url=param2[i][3])
                if r.status_code != param2[i][6]:
                    j = r.json()
                    code_msg = (param2[i][2] + j['message']).encode('utf-8')
                    assert_equal(param2[i][6], r.status_code, code_msg)
                else:
                    logging.info(u'\n%s测试通过！' % param2[i][2])
            else:
                continue

    # APP商品列表
    @nottest
    def test11_app_goods_list(self):
        for i in range(len(param2)):
            if param2[i][1] == u'APP商品列表' and param2[i][9] == 'available':
                try:
                    json_param = json.JSONDecoder().decode(param2[i][5])
                except ValueError:
                    continue
                r = requests.request(method=param2[i][4], url=param2[i][3], params=json_param)
                j = r.json()
                if r.status_code != param2[i][6]:
                    code_msg = (param2[i][2] + j['message']).encode('utf-8')
                    assert_equal(param2[i][6], r.status_code, code_msg)
                elif param2[i][7] != 'none' and j["count"] != param2[i][7]:
                    code_msg = (param2[i][2] + j['message']).encode('utf-8')
                    assert_equal(param2[i][7], j["count"], code_msg)
                else:
                    logging.info(u'\n%s测试通过！' % param2[i][2])
            else:
                continue

    # APP商品信息
    @nottest
    def test12_app_goods_info(self):
        for i in range(len(param2)):
            if param2[i][1] == u'APP商品信息' and param2[i][9] == 'available':
                if param2[i][8] == 'need_token':
                    r = requests.request(method=param2[i][4], url=param2[i][3], headers=token_headers)
                else:
                    r = requests.request(method=param2[i][4], url=param2[i][3])
                if r.status_code != param2[i][6]:
                    j = r.json()
                    code_msg = (param2[i][2] + j['message']).encode('utf-8')
                    assert_equal(param2[i][6], r.status_code, code_msg)
                else:
                    logging.info(u'\n%s测试通过！' % param2[i][2])
            else:
                continue

    # APP查询运费
    @nottest
    def test13_app_querycost(self):
        for i in range(len(param2)):
            if param2[i][1] == u'APP查询运费' and param2[i][9] == 'available':
                r = requests.request(method=param2[i][4], url=param2[i][3])
                j = r.json()
                if r.status_code != param2[i][6]:
                    code_msg = (param2[i][2] + j['message']).encode('utf-8')
                    assert_equal(param2[i][6], r.status_code, code_msg)
                elif j["express_cost"] != param2[i][7]:
                    print(j["express_cost"], param2[i][7])
                    code_msg = (param2[i][2] + j['message']).encode('utf-8')
                    assert_equal(param2[i][7], j["count"], code_msg)
                else:
                    logging.info(u'\n%s测试通过！' % param2[i][2])
            else:
                continue

    # APP获取版本号
    @nottest
    def test14_app_version(self):
        for i in range(len(param2)):
            if param2[i][1] == u'APP获取版本号' and param2[i][9] == 'available':
                json_param = json.JSONDecoder().decode(param2[i][5])
                r = requests.request(method=param2[i][4], url=param2[i][3], params=json_param)
                if r.status_code != param2[i][6]:
                    j = r.json()
                    code_msg = (param2[i][2] + j['message']).encode('utf-8')
                    assert_equal(param2[i][6], r.status_code, code_msg)
                else:
                    logging.info(u'\n%s测试通过！' % param2[i][2])
            else:
                continue

    # APP获取服务内容列表
    @nottest
    def test15_app_term_list(self):
        for i in range(len(param2)):
            if param2[i][1] == u'APP获取服务内容列表' and param2[i][9] == 'available':
                json_param = json.JSONDecoder().decode(param2[i][5])
                r = requests.request(method=param2[i][4], url=param2[i][3], params=json_param)
                if r.status_code != param2[i][6]:
                    j = r.json()
                    code_msg = (param2[i][2] + j['message']).encode('utf-8')
                    assert_equal(param2[i][6], r.status_code, code_msg)
                else:
                    logging.info(u'\n%s测试通过！' % param2[i][2])
            else:
                continue

    # APP获取服务内容详细信息
    @nottest
    def test16_app_term(self):
        for i in range(len(param2)):
            if param2[i][1] == u'APP获取服务内容详细信息' and param2[i][9] == 'available':
                r = requests.request(method=param2[i][4], url=param2[i][3])
                if r.status_code != param2[i][6]:
                    j = r.json()
                    code_msg = (param2[i][2] + j['message']).encode('utf-8')
                    assert_equal(param2[i][6], r.status_code, code_msg)
                else:
                    logging.info(u'\n%s测试通过！' % param2[i][2])
            else:
                continue

    # APP广告列表
    @nottest
    def test17_app_ad_list(self):
        for i in range(len(param2)):
            if param2[i][1] == u'APP广告列表' and param2[i][9] == 'available':
                json_param = json.JSONDecoder().decode(param2[i][5])
                r = requests.request(method=param2[i][4], url=param2[i][3], json=json_param)
                j = r.json()
                global requests_id
                requests_id = j["request_id"]
                if r.status_code != param2[i][6]:
                    code_msg = (param2[i][2] + j['message']).encode('utf-8')
                    assert_equal(param2[i][6], r.status_code, code_msg)
                else:
                    logging.info(u'\n%s测试通过！' % param2[i][2])
            else:
                continue

    # APP广告展示
    @nottest
    def test18_app_ad(self):
        for i in range(len(param2)):
            if param2[i][1] == u'APP广告展示' and param2[i][9] == 'available':
                json_param = json.JSONDecoder().decode(param2[i][5])
                json_param["request_id"] = requests_id
                r = requests.request(method=param2[i][4], url=param2[i][3], json=json_param)
                j = r.json()
                if r.status_code != param2[i][6]:
                    code_msg = (param2[i][2] + j['message']).encode('utf-8')
                    assert_equal(param2[i][6], r.status_code, code_msg)
                else:
                    logging.info(u'\n%s测试通过！' % param2[i][2])
            else:
                continue

if __name__ == '__main__':
    raise
    nose.main()
