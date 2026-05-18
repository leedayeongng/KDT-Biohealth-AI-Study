import FinanceDataReader as fdr
import pymysql # pymysql → Python에서 MySQL DB 연결하기 위한 라이브러리

# MySQL 데이터베이스에 연결
conn = pymysql.connect(
    host='localhost', # DB가 설치된 주소 (내 컴퓨터)
    user='root',  # MySQL 사용자 계정
    password='root',
    db='money',
    charset='utf8mb4', # 한글 깨짐 방지
    cursorclass=pymysql.cursors.DictCursor
)

# 한국거래소(KRX)에 상장된 모든 종목 목록을 가져옴
# 결과는 pandas DataFrame 형태
df = fdr.StockListing('KRX')

# MySQL에 데이터를 넣기 위한 SQL문
# %s 는 나중에 실제 값으로 치환됨
sql = """
    INSERT INTO stocks (ticker, stock_nm, market_code)
    VALUES (%s, %s, %s)
"""

try:
    with conn.cursor() as cursor:
        for idx, row in df.iterrows():
            cursor.execute(
                sql,
                (row['Code'], row['Name'], row['Market'])
            )
        conn.commit()    # 모든 INSERT 작업을 DB에 최종 반영
except Exception as e:
    print("에러 발생:", str(e))
finally:
    conn.close()


# KRX 전체 종목 목록을 가져와서 MySQL stocks 테이블에 저장하는 코드