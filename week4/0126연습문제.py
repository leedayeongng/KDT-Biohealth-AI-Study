import sqlite3

#DB 연결 (logs.db 파일 생성)
conn = sqlite3.connect('logs.db')
cur = conn.cursor() #커서(Cursor) 생성

#테이블 생성 SQL
create_table_sql = """
CREATE TABLE IF NOT EXISTS error_logs (  
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    level VARCHAR(10) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    file_name VARCHAR(255) NOT NULL,
    function_name VARCHAR(255),
    message TEXT NOT NULL,
    details TEXT
);
"""
# ?를 5개 사용
insert_sql = "INSERT INTO error_logs (level, file_name, function_name, message, details) VALUES (?, ?, ?, ?, ?)"

# 데이터도 5개를 튜플로 전달
data = ('ERROR', 'main.py', 'login_user', 'DB 연결 실패', 'ConnectionTimeout: 5000ms')

#실행하기 (통역사 cur에게 SQL 전달)
cur.execute(create_table_sql) #테이블만들고
cur.execute(insert_sql)  #데이터넣고
#저장하고 닫기
conn.commit()
conn.close()
print("성공! logs.db 파일이 생성되었고 데이터가 저장되었습니다.")