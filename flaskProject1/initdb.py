import pymysql
from flask import Flask, render_template, request
# import timer
import ipaddr
def delete_db():
    db = pymysql.connect(
        user="test",
        passwd="qwe123!@#",
        host="localhost",
        port=3306,
        db="word_count"
    )
    cursor = db.cursor(pymysql.cursors.DictCursor)
    print("localDB : ", cursor)
    delete_sql = "TRUNCATE table word_count;"
    cursor.execute(delete_sql)
    db.commit()
    cursor.close()
    db.close()
    return 0

def delete_dbs():
    pc = ipaddr.ip[:]
    port = ipaddr.dbport[:]
    cnt = 0
    for i in range(len(pc)):
        try:
            db = pymysql.connect(
                user="test",
                passwd="qwe123!@#",
                host=pc[i],
                port=port[i],
                db="db1"
            )

            cursor = db.cursor(pymysql.cursors.DictCursor)
            print("pc%d  : %s" %(i, cursor))
            delete_sql = "TRUNCATE table html;"
            cursor.execute(delete_sql)
            db.commit()
            cursor.close()
            db.close()
            cnt += 1
        except:
            print("db connection error")
    return cnt
