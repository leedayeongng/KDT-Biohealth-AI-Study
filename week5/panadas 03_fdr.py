#pip install finance-datareader
import pandas as pd
import FinanceDataReader as fdr

df = fdr.DataReader('TSLA')
df_2025 = fdr.DataReader('TSLA', '2025-01-01', '2025-12-31')
print(df.tail())
print(df_2025.tail())

#한국 거래소
df_krx = fdr.StockListing('KRX')
print(df_krx.head())
df_krx.to_excel('krx.xlsx', index=False, engine='openpyxl')
