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


def del_app_user(account, table='users'):
    db = conn_db(table)
    sql1 = "delete from shop_user where phone = "
    sql = sql1 + account
    db[1].execute(sql)
    db[0].commit()
    db[0].close()
    if db[1].rowcount == 1:
        print("用户 %d 删除成功！" % account)
    else:
        db[0].rollback()


def get_sha1(phone):
    data = 'phone=' + phone + '&' + 'salt=123456'
    hash_sha1 = hashlib.sha1(data)
    return hash_sha1.hexdigest()


def get_token():
    url = 'http://192.168.2.200/shop/user/login'
    req_param = {"phone": "15100000000", "password": "123abc"}
    r = requests.post(url=url, json=req_param, headers=base_headers)
    c = r.json()
    return c['token']
