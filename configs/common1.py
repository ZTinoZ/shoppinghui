# encoding:utf-8

import json, MySQLdb, requests, hashlib, logging
from configs.config import *


reg_phone = '15000000000'  # 注册专用手机号
login_phone = '15100000000'  # 登录专用手机号

base_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Connection": "keep-alive",
    "Host": "192.168.2.200",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
}


# 获取需要带token的headers
def correlation(corr, token):
    if corr is not None:  # 判断是否有关联，如果没有则返回无关联的headers
        if corr == 'need_token':
            base_headers["Authorization"] = token
            token_headers = base_headers
            return token_headers
        else:
            base_headers["Authorization"] = corr
            token_headers = base_headers
            return token_headers
    else:
        return base_headers


# 生成并获取验证码
def get_sms(reg_phone):
        sign = get_sha1(reg_phone)
        json_param = {"sign": sign, "phone": reg_phone}
        url = 'http://192.168.2.200/sms/register'
        r = requests.post(url=url, json=json_param)
        j = r.json()
        if r.status_code == 200:
            sms = get_db_sms(reg_phone)
            return sms
        elif r.status_code == 400:
            raise Exception(j["message"])
        else:
            raise Exception('获取验证码失败！')


# 从数据库获取验证码
def get_db_sms(account):
    db = conn_db('sms')
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


# 从数据库删除验证码
def del_sms(account, table='sms'):
    db = conn_db(table)
    sql1 = "delete from sms_log where account = "
    sql = sql1 + account
    db[1].execute(sql)
    db[0].commit()
    db[0].close()


# 从数据库删除APP用户
def del_app_user(account, table='users'):
    db = conn_db(table)
    sql1 = "delete from shop_user where phone = "
    sql = sql1 + account
    db[1].execute(sql)
    db[0].commit()
    db[0].close()
    if db[1].rowcount == 1:  # 判断是否删除成功，如果失败则回滚
        logging.info("用户 %s 删除成功！" % account)
    else:
        db[0].rollback()
        logging.info("用户 %s 删除失败，回滚删除操作。" % account)


# 获取手机号加salt的散列值
def get_sha1(value):
    data = 'phone=' + value + '&' + 'salt=123456'
    sha1 = hashlib.sha1(data)
    return sha1.hexdigest()


# 获取Bearer型token
def get_token(phone):
    url = 'http://192.168.2.200/shop/user/login'
    req_param = {"phone": phone, "password": "123abc"}
    r = requests.post(url=url, json=req_param)
    c = r.json()
    token = 'Bearer ' + c['token']
    return token
