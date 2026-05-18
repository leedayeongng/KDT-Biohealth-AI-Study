import requests #Upbit API 호출

market = "KRW-BTC"
url = f"https://api.upbit.com/v1/ticker?markets={market}" #KRW-BTC 마켓(비트코인/원화)의 실시간 가격 가져오기
response = requests.get(url)
print(response.json()) #JSON 형태로 변환해서 출력   (리스트안 딕셔너리 형태)

create_sql = """ 
create table if not exists coin_price(
    seq integer primary key autoincrement,
    market text,
    price real,
    collect_dt datetime default current_timestamp
)
"""
# coin_price 테이블 생성 SQL 위에부분
# SEQ - 자동증가기본키(몇번째데이터인지) MARKET - 마켓이름
#PRICE - 실시간가격, COLLECT DT - 저장시간
#테이블 생성
#실시간 거래금액 저장

#Upbit API에서 실시간 BTC 가격 가져오기

#SQLite DB용 테이블 coin_price를 만들기 위한 SQL 준비