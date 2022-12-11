import pymysql
import os
import paramiko
import time
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import ipaddr
db = None
cursor = None
ip = ipaddr.ip[2]
dbport = ipaddr.dbport[2]
sshport = ipaddr.sshport[2]

def connect_db():
    global db
    global cursor
    db = pymysql.connect(
        user="test",
        passwd="qwe123!@#",
        host=ip,
        port=dbport,
        db="db1"
    )
    cursor = db.cursor(pymysql.cursors.DictCursor)


def insert(data):
    insert_sql = "REPLACE INTO html (id, docs) VALUES (%s, %s);"
    # cursor.executemany(insert_sql,(data))
    cursor.execute(insert_sql, (data))
    db.commit()


def test_get_file(filename):
    f = open("./resource/" + filename, 'r', encoding='UTF-8')
    fid = filename[:-4]
    return (str(fid), str(f.read()))


def remote():
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        ssh.connect(ip, port=sshport, username="root", password="1234")
        print('ssh connected')

        # stdin, stdout, stderr = ssh.exec_command("ls -l")
        ## 경로설정!!!!
        stdin, stdout, stderr = ssh.exec_command("sudo /root/anaconda3/bin/python /home/test/word_count.py")
        lines = stdout.readlines()
        for i in lines:
            re = str(i).replace('\n', '')
            print(re)
        ssh.close()
    except Exception as err:
        print(err)


def main():
    run_time = [time.time()]
    file_list = os.listdir("./resource")
    print(len(file_list))

    print("html문서를 PC의 DB에 저장합니다.")
    connect_db()
    ## 개수 설정
    for i in file_list[:300]:
        a = test_get_file(i)
        insert(a)
    global cursor
    global db
    cursor.close()
    db.close()
    print("\n\nDB 저장 완료!!!!")
    run_time.append(time.time())
    print(f"{run_time[1] - run_time[0]:.4f} sec")

    print("\n%s 의 word_count.py 실행" % ip)
    remote()
    print("word_count.py 종료")
    run_time.append(time.time())
    print(f"{run_time[2] - run_time[1]:.4f} sec")

    print(f"\n총 Run time 시간 : {run_time[2] - run_time[0]:.4f} sec")


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


def start_one_pc_system():
    main()
    main2()
