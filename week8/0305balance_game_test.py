import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False

conn=sqlite3.connect('../datasets/balance_game.db')
df_users = pd.read_sql_query('SELECT * FROM users', conn)
df_res = pd.read_sql_query('SELECT * FROM responses', conn)
print(df_users.head())
print(df_res.head())
conn.close()    #----db에서 데이터읽기까지 완료
#1. 데이터 병합 및 피벗
df_merged = pd.merge(df_res, df_users, left_on='user_id', right_on='id')

# 유저 × 질문 형태로 변환
df_pivot = df.pivot_table(
    index='user_id',
    columns='question_id',
    values='answer',
    aggfunc='first'
)

# 결측값 처리
df_pivot = df_pivot.fillna(0)

print(df_pivot.head())
#

2. 차원축소
from sklearn.decomposition import PCA

pca = PCA(n_components=2)
X_pca = pca.fit_transform(pivot)

pca_df = pd.DataFrame(X_pca, columns=['PC1','PC2'])
#3.시각화
plt.figure(figsize=(8,6))

plt.scatter(
    pca_df['PC1'],
    pca_df['PC2'],
    alpha=0.7
)

plt.title('Balance Game User Preference Map (PCA)')
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.grid(True)

plt.show()
