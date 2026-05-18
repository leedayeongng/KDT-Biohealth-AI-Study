#pip install pymysql
import pymysql   # 아까 sql money 테이블활용 db 접속하기 #선생님 host로 들어감

conn =None
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
        result = cursor.fetchall()
        for row in result:
            print(row['login_id'])

except Exception as e:
    print(str(e))
finally:
    if conn:
        conn.close()