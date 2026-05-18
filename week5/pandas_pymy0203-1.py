# pip install sqlalchemy
from sqlalchemy import create_engine
import pandas as pd
import FinanceDataReader as fdr

# MySQL 연결 엔진 생성
engine = create_engine('mysql+pymysql://root:root@localhost/money')

# KRX 종목 목록 가져오기
df = fdr.StockListing('KRX')

# 필요한 컬럼만 선택 + 컬럼명 DB에 맞게 변경
stocks_df = df[['Code', 'Name', 'Market']].rename(
    columns={
        'Code': 'ticker',
        'Name': 'stock_nm',
        'Market': 'market_code'
    }
)

# DataFrame → MySQL 테이블에 저장
stocks_df.to_sql(
    name='stocks',        # 테이블명
    con=engine,           # DB 연결 엔진
    index=False,          # 인덱스 컬럼 저장 안 함
    if_exists='append'    # 기존 테이블에 데이터 추가
)
