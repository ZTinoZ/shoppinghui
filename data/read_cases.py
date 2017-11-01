# encoding:utf-8

import xlrd, os, math


def read_xls1(module_name):
    f = '%s%s' % (os.path.abspath(os.path.dirname(os.path.dirname(__file__))), '/data/cases_main.xls')
    data = xlrd.open_workbook(f)
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
        name = tuple_name[i][1] + '_' + tuple_name[i][2] + ': '
        url = tuple_name[i][3] + tuple_name[i][4]
        req_param = tuple_name[i][7]
        res_code = int(math.floor(tuple_name[i][8]))
        res_param = tuple_name[i][9]
        correlation = tuple_name[i][10]
        condition = tuple_name[i][11]
        yield num,          api_name,     name,         url,          req_param,    res_code,     res_param,    correlation,  condition
        #     param2[i][0], param2[i][1], param2[i][2], param2[i][3], param2[i][4], param2[i][5], param2[i][6], param2[i][7], param2[i][8]

