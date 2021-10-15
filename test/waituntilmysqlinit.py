######################################################################
# @author      : bidaya0 (bidaya0@$HOSTNAME)
# @file        : waituntilmysqlfinish
# @created     : 星期五 10月 15, 2021 15:43:54 CST
#
# @description :
######################################################################


import requests
import pymysql
while True:
    try:
        pymysql.connect(host='127.0.0.1',
                        user='root',
                        password='dongtai-iast',
                        database='dongtai-webapi')
        break
    except:
        pass
