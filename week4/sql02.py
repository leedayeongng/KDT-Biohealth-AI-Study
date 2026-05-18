import sqlite3
conn = sqlite3.connect('mydb.db')

#1.array or tuble
sql = """
    insert into tb_coin  values (?, ?, ?)
"""
# 2. dict 키로 맵핑
sql2 = """INSERT INTO tb_coin VALUES(:market, :kr, :en)"""
cur = conn.cursor()
cur.execute(sql, ['test', 'test', 'test'])
cur.execute(sql2, {"market": "TEST2", "kr": "TEST2", "en": "TEST2"})
conn.commit() #db반영
conn.close()

#“SQLite DB 파일에 tb_coin 테이블에 데이터를 넣는데, 한 줄은 순서로, 한 줄은 이름(key)으로 넣는 예시 코드”