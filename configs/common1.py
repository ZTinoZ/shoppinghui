# encoding:utf-8

import json, MySQLdb, requests, hashlib
from configs.config import *
from data.read_cases import *

base_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Connection": "keep-alive",
    "Host": "192.168.2.200",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
}


# 获取验证码
def get_sms(account, table='sms'):
    db = conn_db(table)
    sql1 = "select comment from sms_log where account = "
    sql2 = " order by created_at desc limit 1"
    sql = sql1 + account + sql2
    db[1].execute(sql)
    results = db[1].fetchone()
    results = results[0]
    db[0].close()
    return results


# 获取修改密码签名
def get_sign_code(account, product):
    sha11 = get_sha1(account)
    url1 = 'http://192.168.2.200/sms/forget'
    req_param = {"sign": sha11, "password": "123abc", "product": product}
    r1 = requests.post(url=url1, json=req_param)
    sms = get_sms(account)
    sha12 = get_sha1(sms)
    url2 = 'http://192.168.2.200/sms/forget'
    req_param = {"sign": sha12, "verification_code": sms, "phone": account}
    r2 = requests.put(url=url1, json=req_param)
    c = r2.json()
    return c["sign_code"]


# 删除验证码
def del_sms(account, table='sms'):
    db = conn_db(table)
    sql1 = "delete from sms_log where account = "
    sql = sql1 + account
    db[1].execute(sql)
    db[0].close()


# 删除APP用户
def del_app_user(account, table='users'):
    db = conn_db(table)
    sql1 = "delete from shop_user where phone = "
    sql = sql1 + account
    db[1].execute(sql)
    db[0].commit()
    db[0].close()
    if db[1].rowcount == 1:  # 判断是否删除成功，如果失败则回滚
        print("用户 %s 删除成功！" % account)
    else:
        db[0].rollback()


# 获取散列值
def get_sha1(value):
    data = 'phone=' + value + '&' + 'salt=123456'
    sha1 = hashlib.sha1(data)
    return sha1.hexdigest()


# 获取Bearer型令牌
def get_token(phone):
    url = 'http://192.168.2.200/shop/user/login'
    req_param = {"phone": phone, "password": "123abc"}
    r = requests.post(url=url, json=req_param)
    c = r.json()
    token = 'Bearer ' + c['token']
    return token

if __name__ == '__main__':
    a = get_token('15100000000')
    print(a)