#!/usr/bin/python
# coding: utf-8

import cx_Oracle

os.environ['NLS_LANG'] = 'AMERICAN_AMERICA.ZHS16GBK'

class dbc:
    def __init__(self):
        self.__db = cx_Oracle.connect('ybjf_agent', 'ybjf_agent', '172.16.10.128:1521/offline')
        self.__cursor = self.__db.cursor()

    def __exit__(self):
        self.__cursor.close()
        self.__db.close()

    def get_result(self):
        self.sql = "select RESP_CODE,count(*) from ACCOUNT_JOURNAL where ACQ_ID in ('90000801') group by RESP_CODE"
        self.__cursor.execute(self.sql)
        return list(self.__cursor)

if __name__ == '__main__':
    db = dbc()
    result = db.get_result()
