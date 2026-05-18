import FinanceDataReader as fdr
import pandas as pd
# pip install matplotlib


import matplotlib.pyplot as plt
#한글폰트설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False
samsung = fdr.DataReader('005930','2023-01-01')
sk = fdr.DataReader('000660','2023-01-01')
print('이동평균선 moving average')
#5일[단가], 20일[종가] , 60일[장기]
samsung['MA5'] = samsung['Close'].rolling(window=5).mean()
samsung['MA20'] = samsung['Close'].rolling(window=20).mean()
samsung['MA60'] = samsung['Close'].rolling(window=60).mean()
print(samsung[['Close','MA5','MA20','MA60']].tail())
plt.figure(figsize=(12,6))
plt.plot(samsung.index, samsung['Close'],label='종가',color='black',alpha=0.3)
plt.plot(samsung.index, samsung['MA5'],label='5일 평균이동', linestyle='--')
plt.plot(samsung.index, samsung['MA20'],label='20일 평균이동', linestyle='--')
plt.plot(samsung.index, samsung['MA60'],label='60일 평균이동', linestyle='--')
plt.title('상한 주가 및 이동평균선 분석')
plt.legend()
plt.grid(True)
#plt.show()
#첫날 가격으로 나누고 100 곱 정규화하여 상승률비교
samsung_norm = (samsung['Close'] / samsung['Close'].iloc[0]) * 100
sk_norm = (sk['Close']/sk['Close'].iloc[0]) * 100
plt.figure(figsize=(12,6))
plt.plot(samsung_norm.index, samsung_norm, label='삼성',color='blue')
plt.plot(sk_norm.index, sk_norm, label='sk하이닉스', color='red')
plt.axhline(y=100,color='gray',linestyle='--',alpha=0.5) #기준선
plt.title('삼성 vs 하이닉스 수익률 비교 (시작일 = 100일) ')
plt.ylabel('수익률(지수)')
plt.legend()
plt.show()
#plt.figure(figsize=(12,6))
#plt.plot(samsung.index, samsung['Close'], label='삼성', color='blue')
#plt.plot(sk.index, sk['Close'], label='sk하이닉스',color='red')
#plt.legend()
#plt.show()
