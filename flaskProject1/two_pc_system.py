import pymysql
import os
import paramiko
import time
# https://mkjjo.github.io/python/2019/07/09/english_preprocessing.html
import wordcloud
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from os import path
import ipaddr
from threading import Thread

db1 = None
cursor1 = None
db2 = None
cursor2 = None

db = None
cursor = None

ip = ipaddr.ip[1:3]
dbport = ipaddr.dbport[1:3]
sshport = ipaddr.sshport[1:3]

def connect_db():
    # 첫번째 pc
    global db1
    global cursor1
    db1 = pymysql.connect(
        user="test",
        passwd="qwe123!@#",
        host=ip[0],
        port=dbport[0],
        db="db1"
    )
    cursor1 = db1.cursor(pymysql.cursors.DictCursor)

    # 두번째 pc
    global db2
    global cursor2
    db2 = pymysql.connect(
        user="test",
        passwd="qwe123!@#",
        host=ip[1],
        port=dbport[1],
        db="db1"
    )
    cursor2 = db2.cursor(pymysql.cursors.DictCursor)


# data, 다중 행 삽입, data : 튜플을 요소로 가지는 리스트 타입
def insert1(data):
    insert_sql = "REPLACE INTO html (id, docs) VALUES (%s, %s);"
    cursor1.execute(insert_sql, (data))
    db1.commit()


def insert2(data):
    insert_sql = "REPLACE INTO html (id, docs) VALUES (%s, %s);"
    cursor2.execute(insert_sql, (data))
    db2.commit()


def test_get_file(filename):
    f = open("./resource/" + filename, 'r', encoding='UTF-8')
    fid = filename[:-4]
    return (str(fid), str(f.read()))


def remote(pid):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        ssh.connect(ip[pid - 1], port=sshport[pid-1], username="root", password="1234")
        print('%dpc ssh connected' % pid)

        # stdin, stdout, stderr = ssh.exec_command("ls -l")
        stdin, stdout, stderr = ssh.exec_command("sudo /root/anaconda3/bin/python /home/test/word_count.py")
        lines = stdout.readlines()
        for i in lines:
            re = str(i).replace('\n', '')
            print(re)

        ssh.close()
    except Exception as err:
        print(err)


def work(pid, file_list, run_time):
    print("html문서를 PC%d의 DB에 저장합니다." % pid)

    if (pid == 1):
        for i in file_list:
            a = test_get_file(i)
            insert1(a)
            print("pc1:%s" % i, end=' ')
        cursor1.close()
        db1.close()
    elif (pid == 2):
        for i in file_list:
            a = test_get_file(i)
            insert2(a)
            print("pc2:%s" % i, end=' ')
        cursor2.close()
        db2.close()

    print("\n\nDB 저장 완료!!!!")
    run_time.append(time.time())
    print(f"{run_time[1] - run_time[0]:.4f} sec")

    print("\n%s 의 word_count.py 실행" % ip[pid - 1])
    remote(pid)
    print("word_count.py 종료")
    run_time.append(time.time())
    print(f"{run_time[2] - run_time[1]:.4f} sec")

    print(f"\n총 Run time 시간 : {run_time[2] - run_time[0]:.4f} sec")


def main():
    ### code 작성 ###
    run_time1 = [time.time()]
    run_time2 = [time.time()]

    arr = []
    file_list = os.listdir("./resource")
    connect_db()

    th1 = Thread(target=work, args=(1, file_list[0:150], run_time1))
    th2 = Thread(target=work, args=(2, file_list[150:300], run_time2))

    th1.start()
    th2.start()

    th1.join()
    th2.join()


##################################################################################

def connect_local_db():
    ldb = pymysql.connect(
        user="test",
        passwd="qwe123!@#",
        host="localhost",
        port=3306,
        db="word_count"
    )
    lcursor = ldb.cursor(pymysql.cursors.DictCursor)
    select_sql = "SELECT * FROM word_count;"
    lcursor.execute(select_sql)
    result = list(lcursor.fetchall())
    lcursor.close()
    ldb.close()
    return result


def main2():
    result = connect_local_db()
    noun_text = ''
    for d in result:
        ## 속도 튜닝
        for i in range(d['count'] // 10):
            noun_text = noun_text + ' ' + d['word']

    spwords = set(STOPWORDS)
    not_used = ['BBC', 'people', 'year', 'mr', 'day', 'linking', 'price', 'month', 'company', 'service', 'week', 'part',
                'home', ]
    for i in not_used:
        spwords.add(i)
    FONT_PATH = 'C:/Windows/Fonts/malgun.ttf'  # For Korean characters
    # generate() 는 하나의 string value를 입력 받음
    wordcloud = WordCloud(
        background_color='white', width=2000, height=1200,
        ranks_only=None, max_words=100, collocations=False, stopwords=spwords,
        max_font_size=800, relative_scaling=.5
        # font_path=FONT_PATH
    ).generate(noun_text)
    plt.figure()
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.savefig('./static/images/word_cloud.png')


def start_two_pc_system():
    main()
    main2()
