import pymysql
from flask import Flask, render_template, request
# import timer
import ipaddr

ip = ipaddr.ip[:]
port = ipaddr.dbport[:]

def test_db():
    for i in range(len(port)):
        db = pymysql.connect(
            user="test",
            passwd="qwe123!@#",
            host=ip[i],
            port=port[i],
            db="db1"
        )
        cursor = db.cursor(pymysql.cursors.DictCursor)
        print("testdb : ", cursor)
        #delete_sql = "TRUNCATE table word_count;"
        #cursor.execute(delete_sql)
        db.commit()
        cursor.close()
        db.close()
    return 0

test_db()
