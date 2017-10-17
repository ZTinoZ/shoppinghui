# encoding:utf-8

import xlrd, os
route = os.path.abspath('../data')


def read_xls(module_name):
    data = xlrd.open_workbook(route + '/cases.xls')
    table = data.sheet_by_name(module_name)
    base_url = table.cell(6, 2).value
    req_url = table.cell(6, 3).value
    url = base_url + req_url
    req_method = table.cell(6, 4).value
    req_param = table.cell(6, 6).value
    res_code = table.cell(6, 7).value
    res_param = table.cell(6, 8).value
    return url, req_method, req_param, res_code, res_param
