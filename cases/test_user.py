# encoding:utf-8

import requests, json, nose, logging, sys
sys.path.append('..')
from data.read_cases import *
from configs.common1 import *
from nose.tools import nottest, istest, assert_equal


class User:

    @classmethod
    def setup_class(cls):

        global token_headers
        token = get_token(LOGIN_PHONE)
        token_headers = get_token_json(token)

        global param2
        x1 = read_xls1('user')
        param1 = tuple(x1)
        x2 = read_xls2(param1)
        param2 = tuple(x2)

    @classmethod
    def teardown_class(cls):
        try:
            del_app_user(REG_PHONE)
            del_sms(REG_PHONE)
        except:
            raise

    # APP用户注册（无token）
    def test01_app_register(self):
        sms = get_sms(REG_PHONE)
        for i in range(len(param2)):
            if param2[i][1] == u'APP用户注册' and param2[i][9] == 'available':
                json_param = json.JSONDecoder().decode(param2[i][5])
                json_param['verification_code'] = sms
                r = requests.request(method=param2[i][4], url=param2[i][3], json=json_param, headers=base_headers)
                if r.status_code != param2[i][6]:
                    j = r.json()
                    code_msg = (param2[i][2] + j['message']).encode('utf-8')
                    assert_equal(param2[i][6], r.status_code, code_msg)
                else:
                    logging.info(u'\n%s测试通过！' % param2[i][2])
            else:
                continue

    # APP用户登录（无token）
    def test02_app_login(self):
        for i in range(len(param2)):
            if param2[i][1] == u'APP用户登录' and param2[i][9] == 'available':
                json_param = json.JSONDecoder().decode(param2[i][5])
                r = requests.request(method=param2[i][4], url=param2[i][3], json=json_param, headers=base_headers)
                if r.status_code != param2[i][6]:
                    j = r.json()
                    code_msg = (param2[i][2] + j['message']).encode('utf-8')
                    assert_equal(param2[i][6], r.status_code, code_msg)
                else:
                    logging.info(u'\n%s测试通过！' % param2[i][2])
            else:
                continue

    # APP用户修改用户信息
    def test03_app_mod_info(self):
        for i in range(len(param2)):
            if param2[i][1] == u'APP用户修改用户信息' and param2[i][9] == 'available':
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

    # APP用户修改密码


if __name__ == '__main__':
    nose.main()
