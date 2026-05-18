import sqlite3
#경량 db파일 형태   # dbbrowser 다운받아 실행해서 파일땡겨오면 데이터베이스 생성
# conn = sqlite3.connect('mydb.db') #없으면 생성됨
conn = sqlite3.connect(":memory:")
sql="""
    create table tb_coin(
    market VARCHAR(20)
    ,kr_nm VARCHAR(100)
    ,en_nm VARCHAR(100)
    )
        """

cur = conn.cursor()
cur.execute(sql)
conn.close()

#“메모리 안에 임시 SQLite DB를 만들고, tb_coin 테이블을 만들어 놓고 바로 종료한 코드”