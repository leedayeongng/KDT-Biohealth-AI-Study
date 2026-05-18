import pymysql
from auth import *

print ("=== 회원가입 ===")
login_id = input('회원 아이디 입력!: ')
user_pw = input('비번입력: ')
user_nm = input('이름입력: ')
hash_pw_input = hash_pw(user_pw)
try :
    conn = pymysql.connect(
        host='192.168.0.7'
        , user='ldy'
        , password='ldy'
        , db='money'  # 직접적인 data set 이름
        , charset='utf8mb4'
    )
    print('db 접속 성공')
    with conn.cursor() as cursor:
        check_sql = "SELECT user_id FROM users WHERE login_id = %s"
        cursor.execute(check_sql, (login_id,))
        if cursor.fetchone():
            print(f"오류!:{login_id}는 이미 존재하는 아이디 입니다.")
        insert_sql = "INSERT INTO users(login_id, user_pw, user_nm) VALUES(%s, %s, %s)"
        cursor.execute(insert_sql, [login_id, hash_pw_input, user_nm])
        conn.commit()
        print("회원가입이 성공적으로 완료됨.")
except Exception as e:
    print(str(e))
finally:
    if conn:
        conn.close()