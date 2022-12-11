import initdb
import one_pc_system
import two_pc_system
import four_pc_system
import pymysql
from flask import Flask, render_template, request

app = Flask(__name__)
app.run(port=11123, debug=True)

db = pymysql.connect(
    user="test",
    passwd="qwe123!@#",
    host="localhost",
    port=3306,
    db="word_count"
)
cursor = db.cursor(pymysql.cursors.DictCursor)


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/result', methods = ['GET'])
def result():
    if request.method == 'GET':
        temp = request.args.get('num')
        temp = int(temp)
        if temp == 1:
            one_pc_system.start_one_pc_system()
        elif temp == 2:
            two_pc_system.start_two_pc_system()
        elif temp == 4:
            four_pc_system.start_four_pc_system()
        else:
            d = initdb.delete_db()
            d = initdb.delete_dbs()
            if d > 0:
                return "<script>alert('"+str(d)+"개의 DB가 초기화 되었습니다.!'); location.href='/'</script>"
            else:
                return "<script>alert('[ERROR] DB not connected.!'); location.href='/'</script>"
    sql = "SELECT * from word_count order by count DESC"
    cursor.execute(sql)
    word = cursor.fetchall()

    return render_template('result.html', word=word)


if __name__ == "__main__":
    print("server start")
    app.run(host="12.12.2.4", port=11123)
    print("Adsadasdasdadasda")