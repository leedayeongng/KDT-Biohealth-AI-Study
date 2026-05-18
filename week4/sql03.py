import json
import sqlite3
import requests

url = "https://api.upbit.com/v1/market/all" #모든 마켓 리스트를 가져오는 Upbit API
res = requests.get(url)
print(res.json())
json_data = json.loads(res.text) #텍스트(JSON 문자열)를 다시 파이썬 객체로 변환
#리스트 안에 딕셔너리가 여러 개 들어있음
for v in json_data:
    print(v)
conn = sqlite3.connect('mydb.db') #sqlite db연결
cur = conn.cursor() #커서 생성 → SQL 실행용
sql = """
    insert into tb_coin values(?, ?, ?)  
""" #tb_coin 테이블에 한 줄씩 넣기 위한 SQL
for row in json_data: #API에서 받아온 모든 마켓 정보를 한 줄씩 콘솔에 출력 /모든 마켓 정보를 반복해서 DB 한 줄씩 INSERT
    cur.execute(sql, [row['market'],row['korean_name'],row['english_name']])

conn.commit()
conn.close()

#“Upbit API에서 모든 마켓 정보를 받아와서, tb_coin 테이블에 순서대로 한 줄씩 저장하는 코드”