# encoding:utf-8

import MySQLdb


def conn_db(table):
    test_db = MySQLdb.connect("192.168.2.215","root","root",table)
    cursor = test_db.cursor()
    return test_db, cursor