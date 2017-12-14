# encoding:utf-8

import xlrd, os, math, json


cases_main = '%s%s' % (os.path.abspath(os.path.dirname(os.path.dirname(__file__))), '/data/cases_main.xls')
cases_gpbs = '%s%s' % (os.path.abspath(os.path.dirname(os.path.dirname(__file__))), '/data/cases_gpbs.xls')
cases_qiniu = '%s%s' % (os.path.abspath(os.path.dirname(os.path.dirname(__file__))), '/data/cases_qiniu.xls')
param_path = '%s%s' % (os.path.abspath(os.path.dirname(os.path.dirname(__file__))), '/data/')


def read_xls1(module_name):
    data = xlrd.open_workbook(cases_main)
    table = data.sheet_by_name(module_name)
    for i in range(1, 201):
        num = table.cell(i, 0).value
        if num != 'END':  # 如果用例已读取完毕则跳出循环
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
        req_method = tuple_name[i][5]
        req_param = tuple_name[i][7]
        res_code = int(math.floor(tuple_name[i][8]))
        res_param = tuple_name[i][9]
        correlation = tuple_name[i][10]
        exec_condition = tuple_name[i][11]
        yield num,          api_name,     name,         url,          req_method,   req_param,    res_code,     res_param,    correlation,  exec_condition
        #     param2[i][0], param2[i][1], param2[i][2], param2[i][3], param2[i][4], param2[i][5], param2[i][6], param2[i][7], param2[i][8], param2[i][9]


def read_param(excel_path):
    path = '/'.join((param_path, excel_path))
    with open(path, 'r') as p:
        param = p.readlines()
    param = json.loads(''.join(param).strip('\n'))
    return param
