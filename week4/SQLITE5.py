import sqlite3 #SQLite DB 다루기 위해 모듈 불러오기
conn = sqlite3.connect('mydb.db')
cur = conn.cursor() #커서 생성 → DB에 SQL 문 실행용
cur.execute("SELECT * FROM tb_coin WHERE kr_nm LIKE ?", ('%비트%',))
#비트'를 포함한 모든 행을 가져옴 ('%비트%',) → 튜플로 값 전달, ?-자리표시자
rows = cur.fetchall() #SELECT 결과를 모든 행 리스트로 가져오기
for row in rows: #검색된 모든 행을 한 줄씩 출력
    print(row)


#“DB에서 한국어 이름에 ‘비트’가 포함된 코인만 찾아서 출력하는 코드”