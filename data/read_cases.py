# encoding:utf-8

import xlrd, os, math
route = os.path.abspath('../data')


def read_xls1(module_name):
    data = xlrd.open_workbook(route + '/cases.xls')
    table = data.sheet_by_name(module_name)
    for i in range(1, 201):
        num = table.cell(i, 0).value  # 判断该行是否有用例，如果用例已读取完则跳出循环
        if num != '':
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
            yield int(math.floor(num)), api_name, url, req_param, int(math.floor(res_code)), res_param
        else:
            break


def read_xls2(tuple_name):
    for i in range(len(tuple_name)):
        yield tuple_name[i][1], tuple_name[i][2], tuple_name[i][3], tuple_name[i][4], tuple_name[i][5]
