#pip install pymysql
#pip install flask   플라스크로 웹서버만드는 기초, 백엔드 입문
from flask import Flask, render_template
import pymysql

app = Flask(__name__)  #웹 서버 하나 생성


@app.route("/")  #  경로설정 주소(URL) 설정
def index():
        return "Hello" #헬로를 제공
@app.route("/main")
def main():
    nm = "nick"
    return render_template("main.html", nm=nm)
@app.route("/pick")
def pick():
    return render_template("ex-pick.html") #예전에 html만든거 가저온거 가져와서 ex-pick 파일도 복사해놓기

@app.route("/list")
def list():
    users = []
    conn = None
    try:
        #db연결
        conn = pymysql.connect(
             host='192.168.0.7'
            ,user='ldy'   #이니셜|이니셜
            ,password='ldy'
            ,db='money'
            ,charset='utf8MB4',
        )
        print('db 접속 성공')
        with conn.cursor(pymysql.cursors.DictCursor) as cursor:
            sql ="SELECT * FROM users"
            cursor.execute(sql)
            users = cursor.fetchall()

    except Exception as e:
        print(str(e))
    finally:
        if conn:
            conn.close()
    return render_template("list.html",users=users)








if __name__ == '__main__':
    app.run(debug=True, port=5500, host='0.0.0.0')
# 웹 서버 하나 띄워 주소 / 로 접속하면 화면에 Hello를 보여준다”