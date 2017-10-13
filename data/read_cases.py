# encoding:utf-8

import xlrd


def xls(module_name, url, method, req_param, res_code, res_param):
    data = xlrd.open_workbook('cases.xls')
    table = data.sheet_by_name(module_name)
    base_url = table.cell(1, 2).value
    req_url = table.cell(1, 3).value
    url = base_url + req_url
    method = table.cell(1, 4).value
    req_param = table.cell(1, 6).value
    res_code = table.cell(1, 7).value
    res_param = table.cell(1, 8).value
    return url, method, req_param, res_code, res_param
