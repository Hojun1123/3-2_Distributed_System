import pymysql
import os
import paramiko
import time
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
from os import path
import ipaddr
from threading import Thread

# 각 클라이언트와의 db_connection을 위한 변수 선언
db1 = None
cursor1 = None
db2 = None
cursor2 = None
db3 = None
cursor3 = None
db4 = None
cursor4 = None

# localhost(서버)의 db_connection을 위한 변수 선언
db = None
cursor = None

# ip_pool, 차례대로 각 클라이언트의 ip
ip = ipaddr.ip[:]

# db_connection
def connect_db():
    # 첫번째 pc
    global db1
    global cursor1
    db1 = pymysql.connect(
        user="test",
        passwd="qwe123!@#",
        host=ip[0],
        port=3306,
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
        port=3306,
        db="db1"
    )
    cursor2 = db2.cursor(pymysql.cursors.DictCursor)

    # 세번째 pc
    global db3
    global cursor3
    db3 = pymysql.connect(
        user="test",
        passwd="qwe123!@#",
        host=ip[2],
        port=3306,
        db="db1"
    )
    cursor3 = db3.cursor(pymysql.cursors.DictCursor)

    # 두번째 pc
    global db4
    global cursor4
    db4 = pymysql.connect(
        user="test",
        passwd="qwe123!@#",
        host=ip[3],
        port=3306,
        db="db1"
    )
    cursor4 = db4.cursor(pymysql.cursors.DictCursor)


# 각 DB에 이미 값이 있다면 update하고, 없으면 insert
# data, 다중 행 삽입, data : 튜플을 요소로 가지는 리스트 타입
def insert1(data):
    insert_sql = "REPLACE INTO html (id, docs) VALUES (%s, %s);"
    cursor1.execute(insert_sql, (data))
    db1.commit()


def insert2(data):
    insert_sql = "REPLACE INTO html (id, docs) VALUES (%s, %s);"
    cursor2.execute(insert_sql, (data))
    db2.commit()


def insert3(data):
    insert_sql = "REPLACE INTO html (id, docs) VALUES (%s, %s);"
    cursor3.execute(insert_sql, (data))
    db3.commit()


def insert4(data):
    insert_sql = "REPLACE INTO html (id, docs) VALUES (%s, %s);"
    cursor4.execute(insert_sql, (data))
    db4.commit()


# 해당 filename을 open해서 db의 입력형식으로 돌려줌
def test_get_file(filename):
    f = open("./resource/" + filename, 'r', encoding='UTF-8')
    fid = filename[:-4]
    return (str(fid), str(f.read()))


# 클라이언트를 원격으로 실행하기 위한 로직
def remote(pid):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        ssh.connect(ip[pid - 1], username="root", password="1234")
        print('%dpc ssh connected' % pid)

        # stdin, stdout, stderr = ssh.exec_command("ls -l") ##테스트 코드
        stdin, stdout, stderr = ssh.exec_command("sudo /root/anaconda3/bin/python /home/client1/word_count.py")
        lines = stdout.readlines()
        for i in lines:
            re = str(i).replace('\n', '')
            print(re)
        ssh.close()
    except Exception as err:
        print(err)


# 각 쓰레드(프로세스) 단위로 작동하는 로직
def work(pid, file_list, run_time):
    print("html문서를 PC%d의 DB에 저장합니다." % pid)

    if pid == 1:
        for i in file_list:
            a = test_get_file(i)
            insert1(a)
        cursor1.close()
    elif pid == 2:
        for i in file_list:
            a = test_get_file(i)
            insert2(a)
        cursor2.close()
    elif pid == 3:
        for i in file_list:
            a = test_get_file(i)
            insert3(a)
        cursor3.close()
    elif pid == 4:
        for i in file_list:
            a = test_get_file(i)
            insert4(a)
        cursor4.close()

    print("\n\nDB 저장 완료!!!!")
    run_time.append(time.time())
    print(f"{run_time[1] - run_time[0]:.4f} sec")

    print("\n%s 의 word_count.py 실행" % ip[pid - 1])
    remote(pid)
    print("word_count.py 종료")
    run_time.append(time.time())

    # 각 쓰레드(프로세스) 에서 걸린 시간 출력
    print(f"{run_time[2] - run_time[1]:.4f} sec")


# pass1 로직
def main():
    # 각 쓰레드(프로세스)의 runtime을 추적하기 위한 변수
    run_time1 = [time.time()]
    run_time2 = [time.time()]
    run_time3 = [time.time()]
    run_time4 = [time.time()]

    # resource폴더의 파일 리스트를 받아와 저장
    file_list = os.listdir("./resource")

    connect_db()
    filenum = 9600
    th1 = Thread(target=work, args=(1, file_list[0:100], run_time1))
    th2 = Thread(target=work, args=(2, file_list[100:200], run_time2))
    th3 = Thread(target=work, args=(3, file_list[200:300], run_time3))
    th4 = Thread(target=work, args=(4, file_list[300:400], run_time4))

    th1.start()
    th2.start()
    th3.start()
    th4.start()

    th1.join()
    th2.join()
    th3.join()
    th4.join()
    print()
    print(f"pc1 총 Run time 시간 : {run_time1[2] - run_time1[0]:.4f} sec")
    print(f"pc2 총 Run time 시간 : {run_time2[2] - run_time2[0]:.4f} sec")
    print(f"pc3 총 Run time 시간 : {run_time3[2] - run_time3[0]:.4f} sec")
    print(f"pc4 총 Run time 시간 : {run_time4[2] - run_time4[0]:.4f} sec")


##################################################################################

def connect_local_db():
    global db
    global cursor
    db = pymysql.connect(
        user="test",
        passwd="qwe123!@#",
        host="localhost",
        port=3306,
        db="word_count"
    )
    cursor = db.cursor(pymysql.cursors.DictCursor)


def select():
    select_sql = "SELECT * FROM word_count;"
    cursor.execute(select_sql)
    result = list(cursor.fetchall())
    cursor.close()
    return result


def main2():
    connect_local_db()
    result = select()

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
        max_font_size=800, relative_scaling=.5,
        font_path=FONT_PATH
    ).generate(noun_text)
    plt.figure()
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()


def start_four_pc_system():
    main()
    main2()