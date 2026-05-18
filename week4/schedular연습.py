#schedular , sqlite4를 이용해 코인수집함수만들기
# #1분마다 함수실행 #저장확인
# pip install apscheduler requests
import datetime
import requests
import sqlite3
from apscheduler.schedulers.blocking import BlockingScheduler

# ===============================
# 1️⃣ SQLite DB 생성 및 테이블 설정
# ===============================
conn = sqlite3.connect('coin_price2.db')
cur = conn.cursor()

create_sql = """
CREATE TABLE IF NOT EXISTS coin_price2 (
    seq INTEGER PRIMARY KEY AUTOINCREMENT,
    market TEXT,
    price REAL,
    collect_dt DATETIME DEFAULT CURRENT_TIMESTAMP
)
"""
cur.execute(create_sql)
conn.commit()
conn.close()

# ===============================
# 2️⃣ 코인 가격 수집 함수
# ===============================
def collect_coin_price2():
    try:
        market = "KRW-BTC"
        url = f"https://api.upbit.com/v1/ticker?markets={market}"
        response = requests.get(url, timeout=5)
        data = response.json()[0]

        market_name = data['market']
        price = data['trade_price']
        now = datetime.datetime.now()

        conn = sqlite3.connect('coin_price2.db')
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO coin_price2 (market, price) VALUES (?, ?)",
            (market_name, price)
        )
        conn.commit()
        conn.close()

        print(f"[{now}] {market_name} 가격 저장: {price}원")

    except Exception as e:
        print("오류 발생:", e)

# ===============================
# 3️⃣ 스케줄러 설정
# ===============================
scheduler = BlockingScheduler()
scheduler.add_job(collect_coin_price2, 'interval', minutes=1)

print("코인 가격 수집 스케줄러 시작!")
scheduler.start()
