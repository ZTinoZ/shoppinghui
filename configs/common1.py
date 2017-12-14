# encoding:utf-8

import json, MySQLdb, requests, hashlib, logging
from configs.config import *
from nose.tools import nottest, istest, assert_equal


REG_PHONE = '15000000000'  # 注册专用手机号
LOGIN_PHONE = '15100000000'  # 登录专用手机号（已认证）
LOGIN_PHONE_UNAUTH = '15200000000'  # 登录专用手机号（未认证）
SKU = 'aabb7c86-bf9b-11e7-9271-000c2925c14e'  # 下单专用sku
SKU2 = '7f5e2f93-ca7a-11e7-9271-000c2925c14e'  # 已下架sku
WAREHOUSE = '8e09b82f-bf96-11e7-9271-000c2925c14e'  # 下单专用sku所属仓库
WAREHOUSE2 = 'be784eab-c9f8-11e7-9271-000c2925c14e'  # 不在配送范围内的仓库


base_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Connection": "keep-alive",
    "Host": "192.168.2.200",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
}


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
    sql1 = "select comment from sms.sms_log where account = "
    sql2 = " order by created_at desc limit 1"
    sql = sql1 + account + sql2
    db[1].execute(sql)
    results = db[1].fetchone()
    results = results[0]
    db[0].close()
    return results


# 添加商品至购物车并获取购物车id
def get_shopcart_id():
    url = 'http://192.168.2.200/shop/shopcart'
    req_param = {
        "sku_id": SKU,
        "company_id": "3d75251a-6df2-11e7-a420-000c2925c14e",
        "count": 1,
        "sale_price": 0.01,
        "bonus": 0.01,
        "points": 0,
        "warehouse_ids": ["8e09b82f-bf96-11e7-9271-000c2925c14e"]
    }
    base_headers["Authorization"] = get_token(LOGIN_PHONE)
    headers = base_headers
    r = requests.post(url=url, json=req_param, headers=headers)
    if r.status_code == 200:
        shopcart_id = get_db_shopcart_id(SKU)
        return shopcart_id
    else:
        raise Exception(r.status_code)


# 从数据库获取购物车id
def get_db_shopcart_id(sku_id):
    db = conn_db('sms')
    sql1 = "select id from shop.shop_user_cart where sku_id = "
    sql2 = " order by created_at desc limit 1"
    sql = sql1 + "'" + sku_id + "'" + sql2
    db[1].execute(sql)
    results = db[1].fetchone()
    results = results[0]
    db[0].close()
    return results


# 获取修改密码签名
def get_sign_code(account, product):
    sha11 = get_sha1(account)
    url1 = 'http://192.168.2.200/sms/forget'
    req_param = {"sign": sha11, "phone": account, "product": product}
    requests.post(url=url1, json=req_param)
    sms = get_sms(account)
    sha12 = get_sha1(sms)
    url2 = 'http://192.168.2.200/sms/forget'
    req_param = {"sign": sha12, "verification_code": sms, "phone": account}
    r2 = requests.put(url=url2, json=req_param)
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
    sql1 = "delete from users.shop_user where phone = "
    sql = sql1 + "'" + account + "'"
    db[1].execute(sql)
    db[0].commit()
    db[0].close()
    if db[1].rowcount != 1:  # 判断是否删除成功，如果失败则回滚
        db[0].rollback()
    else:
        raise


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


# 获取带有token的headers
def get_token_json(token):
    base_headers["Authorization"] = token
    token_headers = base_headers
    return token_headers


# 获取最新一笔待支付订单
def get_order0():
    db = conn_db('shop')
    sql = "select * from shop.member_order where user_id = '070b4130-b896-11e7-9271-000c2925c14e' and pay_status = 0 order by created_at desc limit 1;"
    db[1].execute(sql)
    results = db[1].fetchone()
    results = results[0]
    db[0].close()
    return results


# 获取最新一笔待支付（进行过支付）订单
def get_order1():
    db = conn_db('shop')
    sql = "select * from shop.member_order where user_id = '070b4130-b896-11e7-9271-000c2925c14e' and pay_status = 1 order by created_at desc limit 1;"
    db[1].execute(sql)
    results = db[1].fetchone()
    results = results[0]
    db[0].close()
    return results


# 获取最新一笔待支付（进行过支付，部分已支付）订单
def get_order2():
    db = conn_db('shop')
    sql = "select * from shop.member_order where user_id = '070b4130-b896-11e7-9271-000c2925c14e' and pay_status = 2 order by created_at desc limit 1;"
    db[1].execute(sql)
    results = db[1].fetchone()
    results = results[0]
    db[0].close()
    return results

# if __name__ == '__main__':
#     print(type(get_order()))
