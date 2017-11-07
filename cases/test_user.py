# encoding:utf-8

import requests, json, nose, logging, sys
sys.path.append('..')
from data.read_cases import *
from configs.common1 import *
from nose.tools import nottest, istest, assert_equal


class TestUser:

    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        try:
            del_app_user(reg_phone)
            del_sms(reg_phone)
        except:
            raise

    # APP用户注册（无token）
    def test_1_app_register(self):
        sms = get_sms(reg_phone)
        x1 = read_xls1('user')
        param1 = tuple(x1)
        x2 = read_xls2(param1)
        param2 = tuple(x2)
        for i in range(len(param2)):
            if param2[i][1] == u'APP用户注册' and param2[i][8] == 'available':
                json_param = json.JSONDecoder().decode(param2[i][4])
                json_param['verification_code'] = sms
                r = requests.post(url=param2[i][3], json=json_param, headers=base_headers)
                j = r.json()
                code_msg = (param2[i][2] + j['message']).encode('utf-8')
                assert_equal(param2[i][5], r.status_code, code_msg)
            else:
                continue

    # APP用户登录（无token）
    def test_2_app_login(self):
        x1 = read_xls1('user')
        param1 = tuple(x1)
        x2 = read_xls2(param1)
        param2 = tuple(x2)
        for i in range(len(param2)):
            if param2[i][1] == u'APP用户登录' and param2[i][8] == 'available':
                json_param = json.JSONDecoder().decode(param2[i][4])
                r = requests.post(url=param2[i][3], json=json_param, headers=base_headers)
                code_msg = param2[i][2].encode('utf-8') + '用例失败（状态码不匹配）！'
                assert_equal(param2[i][5], r.status_code, code_msg)
            else:
                continue

    # APP用户修改用户信息
    def test_3_app_mod_info(self):
        x1 = read_xls1('user')
        param1 = tuple(x1)
        x2 = read_xls2(param1)
        param2 = tuple(x2)
        for i in range(len(param2)):
            if param2[i][1] == u'APP用户修改用户信息' and param2[i][8] == 'available':
                headers = correlation(param2[i][7], get_token(login_phone))
                r = requests.put(url=param2[i][3], headers=headers)
                code_msg = param2[i][2].encode('utf-8') + '用例失败（状态码不匹配）！'
                assert_equal(param2[i][5], r.status_code, code_msg)
            else:
                continue

    # APP用户修改密码


if __name__ == '__main__':
    nose.main()
