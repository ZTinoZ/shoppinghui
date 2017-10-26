# encoding:utf-8

import xlrd, json,requests, math
from configs import config



url = 'http://192.168.2.200/shop/user/login'
req_param = {"phone": "15100000000", "password": "123abc"}
r = requests.post(url=url, json=req_param)
c = r.json()



data = xlrd.open_workbook(r'case_templet.xls')
table = data.sheet_by_name('Sheet1')
a = table.cell(1, 10).value
a = json.JSONDecoder().decode(a)
b = table.cell(1, 7).value
b = json.JSONDecoder().decode(b)

print(a['verification_code'])