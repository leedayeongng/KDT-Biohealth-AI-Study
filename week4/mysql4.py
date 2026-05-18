import pymysql
from auth import *   # 샘한테 내 sql을 권한을 줘서 샘이 나한테 들어오는 로그인 인증

print("=== 로그인 ===")
login_id = input("아이디를 입력하세요: ")
input_pw = input("비밀번호를 입력하세요: ")

conn = None

try :
    # db연결
    conn =pymysql.connect(
        host='192.168.0.7'
        , user='ldy'
        , password = 'ldy'
        , db = 'money'              # 직접적인 data set 이름
        , charset = 'utf8mb4'       #
    )
    print('db 접속 성공')
    with conn.cursor(pymysql.cursors.DictCursor) as cursor:
        sql = "SELECT * FROM users WHERE login_id = %s"
        cursor.execute(sql, (login_id,))
        result = cursor.fetchone()
        if result:
            stored_hash = result['user_pw']
            if check_pw(input_pw, stored_hash):
                print(f"로그인 성공 {result['user_nm']}님 환영합니다.")
            else :
                print(f"로그인 실패")
        else :
            print(f"로그인 실패 {login_id}는 존재하지 않는 아이디입니다.")

except Exception as e :
    print(str(e))

finally:
    if conn:
        conn.close()