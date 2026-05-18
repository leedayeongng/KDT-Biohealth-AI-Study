import FinanceDataReader as fdr
import pandas as pd
# pip install matplotlib
import matplotlib.pyplot as plt
#한글폰트설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False
df = fdr.DataReader('005930','2024-01-01')
print(df.head())
plt.figure(figsize=(10,8)) # 가로 10 세로 8
plt.subplot(2,1,1)  #2행1열 그리드에서 1번째 칸
plt.plot(df.index, df['Close'], label='samsung close', color='navy')
plt.title('삼성전자 주가 추이(2024~)')
plt.ylabel('가격(원)')
plt.grid(True) #격자표시
plt.legend() #범례표시
#두번째 그래프 거래량
plt.subplot(2,1,2)
plt.bar(df.index, df['Volume'], label='거래량', color='lightgreen')
plt.title('일별 거래량')
plt.ylabel('거래량(주)')
plt.xlabel('날짜')
plt.grid(True, axis='y') #y축만 격자 표시
plt.legend()
plt.tight_layout() # 그래프 간격 자동 조정
plt.show()