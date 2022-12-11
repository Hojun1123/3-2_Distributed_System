from bs4 import BeautifulSoup
import urllib
import pymysql
import re
import nltk
from nltk.corpus import stopwords
from collections import Counter

#1회만 다운
#nltk.download('all')

#db connection
db = pymysql.connect(
    user = "test",
    passwd = "qwe123!@#",
    host = "localhost",
    port = 3306,
    db = "db1"
)
cursor = db.cursor(pymysql.cursors.DictCursor)

#db connection
server_db = pymysql.connect(
    user = "test",
    passwd = "qwe123!@#",
    host = "49.174.54.239",
    port = 11124,
    db = "word_count"
)
cursor2 = server_db.cursor(pymysql.cursors.DictCursor)

#data 
def insert(data):
    icnt = 0
    for i in data:
        insert_sql = "INSERT INTO word_count (word, count) VALUES (%s, %s) on DUPLICATE key update count=count+%s;"
        cursor2.execute(insert_sql, i)
        icnt = icnt + 1
        if icnt%1000:
            server_db.commit()
    server_db.commit()

def select():
    select_sql = "SELECT * FROM html;"
    cursor.execute(select_sql)
    result = list(cursor.fetchall())
    cursor.close()
    db.close()
    return result

def remove_tags(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

############ main ###############
    
def main():
    data = select()
    result_data = []
    cnt = 0
    for d in data:
        cnt += 1
        print(cnt)
        #id, doc
        print("%s.txt" %(d['id']), end=' ')

        #태그 제거
        removed_tags = remove_tags(str(d['docs']))
        removed_tags = re.sub(r"[^\.\?\!\w\d\s]",'',str(removed_tags))
        removed_tags = removed_tags.lower()
        #print("result : ", removed_tags)
        #단어 토큰화
        word_tokens = nltk.word_tokenize(removed_tags)
        
        #폼사 분리, (단어, 품사)
        token_pos = nltk.pos_tag(word_tokens)
        
        #명사 추출
        NN_words = []
        for word, pos in token_pos:
            if 'NN' in pos:
                NN_words.append(word)
        
        #명사의 원형 찾기
        wlem = nltk.WordNetLemmatizer()
        lemmatized_words = []
        for word in NN_words:
            new_word = wlem.lemmatize(word)
            lemmatized_words.append(new_word)
        
        #불용어 제거
        stopwords_list = stopwords.words('english') #nltk에서 제공하는 불용어사전 이용
        unique_NN_words = set(lemmatized_words)
        final_NN_words = lemmatized_words
        for word in unique_NN_words:
            if word in stopwords_list:
                while word in final_NN_words:
                    final_NN_words.remove(word)
        
        #하나의 뉴스기사에 대해 word반환
        #print(final_NN_words)

        #기존 단어 리스트에 추가
        result_data += final_NN_words
        
    #단어 빈도수 계산, word_count
    c = Counter(result_data) # input type should be a list of words (or tokens)
    k = 30

    #print("\n\n빈도수 기준 상위 %d개 단어 출력" %k)
    #print(c.most_common(k)) # 빈도수 기준 상위 k개 단어 출력
    temp = c.most_common()
    data = [[str(i[0]), str(i[1]), str(i[1])] for i in list(temp)]

    print("insert counting word into db...")
    insert(data)
    cursor2.close()
    server_db.close()
    print("end")


if __name__ == '__main__':
    main()
