# encoding:utf-8

import xlrd, json,requests
from configs import config

data = xlrd.open_workbook('case_templet.xls')
table = data.sheet_by_name('Sheet1')
base_url = table.cell(1, 2).value
req_url = table.cell(1, 3).value
url = base_url + req_url
method = table.cell(1, 4).value
req_param = table.cell(1, 6).value
res_code = table.cell(1, 7).value
res_param = table.cell(5, 8).value
print(res_param)
print(type(res_param))
print((json.dumps(res_param))["code"])
print(type(json.dumps(res_param)))


