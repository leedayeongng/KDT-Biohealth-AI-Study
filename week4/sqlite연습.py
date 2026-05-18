import sqlite3 #sqlite3 → DB(저장소) 사용

import requests #requests → 인터넷(API) 요청 보내기

market = "KRW-BTC" #KRW-BTC = 비트코인 원화 가격
url = f"https://api.upbit.com/v1/ticker?markets={market}"
response = requests.get(url) #비트코인 가격 주세요” 요청
print(response.json())  #응답을 JSON(파이썬 딕셔너리 형태)으로 받음
json_data = response.json()

create_sql = """
create table if not exists coin_price(
    seq integer primary key autoincrement,
    market text,
    price real,
    collect_dt datetime default current_timestamp
)
"""

#테이블 생성  SQLite DB 연결 + 테이블 생성
conn = sqlite3.connect('mydb.db') #mydb.db 파일 생성 (없으면 자동 생성)
cur = conn.cursor()
cur.execute(create_sql) #coin_price 테이블 생성

#실시간 거래금액 저장   #json_data[0]['market'] → "KRW-BTC" json_data[0]['trade_price'] → 현재 비트코인 가격
#이 두 값을 DB에 저장
insert_sql = """insert into coin_price(market, price) values (?, ?)"""
cur.execute(insert_sql, [json_data[0]['market'], json_data[0]['trade_price']])
conn.commit()
conn.close()
#mydb.db 파일 생성됨,coin_price 테이블 안에

#KRW-BTC(비트코인) 현재 가격을 업비트 API에서 가져와서 SQLite DB에 기록하는 프로그램 ❞
#coin_price 테이블에 저장하는 프로그램 /코인 자동 수집-스케줄러랑 결합-로그 시스템과 연결