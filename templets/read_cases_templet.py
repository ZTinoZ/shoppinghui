# encoding:utf-8

import xlrd, json,requests, math
from configs import config


def read_xls(module_name):
    data = xlrd.open_workbook('case_templet.xls')
    table = data.sheet_by_name(module_name)
    for i in range(1, 6):
        num = table.cell(i, 0).value
        api_name = table.cell(i, 1).value
        base_url = table.cell(i, 2).value
        req_url = table.cell(i, 3).value
        url = base_url + req_url
        req_method = table.cell(i, 4).value
        req_data_type = table.cell(i, 5).value
        req_param = table.cell(i, 6).value
        res_code = table.cell(i, 7).value
        res_param = table.cell(i, 8).value
        correlation_param = table.cell(i, 9).value
        comments = table.cell(i, 10).value
        yield int(math.floor(num)), url, req_param, int(math.floor(res_code)), res_param

if __name__ == '__main__':
    a = read_xls('Sheet1')
    print(tuple(a))

# data = xlrd.open_workbook('case_templet.xls')
# table = data.sheet_by_name('Sheet1')
# for i in range(1, 6):
#     num = table.cell(i, 0).value
#     api_name = table.cell(i, 1).value
#     base_url = table.cell(i, 2).value
#     req_url = table.cell(i, 3).value
#     url = base_url + req_url
#     req_method = table.cell(i, 4).value
#     req_data_type = table.cell(i, 5).value
#     req_param = table.cell(i, 6).value
#     res_code = table.cell(i, 7).value
#     res_param = table.cell(i, 8).value
#     correlation_param = table.cell(i, 9).value
#     comments = table.cell(i, 10).value
#     print(url, req_param, res_code, res_param)
