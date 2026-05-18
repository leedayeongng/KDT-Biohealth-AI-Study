#pip install pymysql
import pymysql   #회원가입
from auth import*

from week4.sqlite연습 import insert_sql

print("=== 회원가입 ===")
login_id = input("회원 아이디입력!: ")
user_pw = input("비밀번호 입력: ")
user_nm = input("이름 입력: ")
hash_pw_input = hash_pw(user_pw)
try:
    conn = pymysql.connect(  #db접속)
        host='192.168.0.7'
        , user='ldy'  # 이니셜|이니셜
        , password='ldy'
        , db='money'
        , charset='utf8MB4',
    )
    print('db 접속 성공')
    with conn.cursor() as cursor:
        check_sql = "SELECT user_id FROM users WHERE login_id=%s" #아이디 중복 확인
        cursor.execute(check_sql, (login_id,))
        if cursor.fetchone():
            print(f"오류! :{login_id}는 이미 존해하는 아이디입니다.")
#사용자 정보 INSERT
        insert_sql = "INSERT INTO users (login_id, user_pw, user_nm) VALUES (%s, %s, %s)"
        cursor.execute(insert_sql, (login_id, user_pw, user_nm))
        conn.commit()
        print("회원가입이 성공적으로 완료됨.")
except Exception as e:
    print(str(e))
finally:
    if conn:
        conn.close()