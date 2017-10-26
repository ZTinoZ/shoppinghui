# encoding:utf-8

import xlrd, os, math
# route = os.path.abspath('../data')


def read_xls1(module_name):
    data = xlrd.open_workbook(r'../data/cases_main.xls')
    table = data.sheet_by_name(module_name)
    for i in range(1, 201):
        num = table.cell(i, 0).value
        if num != '':  # 通过用例序号判断该行是否有用例，如果用例已读取完则跳出循环
            cases = table.row_values(i)
            yield cases
        else:
            break


def read_xls2(tuple_name):
    for i in range(len(tuple_name)):
        num = int(math.floor(tuple_name[i][0]))
        api_name = tuple_name[i][1]
        name = str(num) + '. ' + tuple_name[i][1] + '_' + tuple_name[i][2] + ': '
        url = tuple_name[i][3] + tuple_name[i][4]
        req_param = tuple_name[i][7]
        res_code = int(math.floor(tuple_name[i][8]))
        res_param = tuple_name[i][9]
        yield num, api_name, name, url, req_param, res_code, res_param
