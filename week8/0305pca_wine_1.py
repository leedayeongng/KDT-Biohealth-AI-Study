import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_wine
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

# 13 특성을 ->2
wine = load_wine()
df = pd.DataFrame(wine.data, columns=wine.feature_names)
df['target'] = wine.target
print(df.head(3))
print(f'\n 데이터 크기 : {df.shape[0]} 개의 와인, {df.shape[1]-1}개의 성분(특성)')
x = df.drop('target', axis=1)
y = df['target']
scaler = StandardScaler()
x_scaled = scaler.fit_transform(x)
pca = PCA(n_components=2) #2차원으로
x_pca = pca.fit_transform(x_scaled)
#결과
df_pca = pd.DataFrame(data=x_pca, columns=['Principal Component 1','Principal Component 2'])
df_pca['target'] = y
print('2d 요약 데이터')
print(df_pca.head(3))
#주성분 설명력
explained_ratio =pca.explained_variance_ratio_
print('정보 보존율 (설명된 분산비율)')
print(f'pc1이 원본 데이터의 약 {explained_ratio[0]*100:.1f}% 정보를 담고있음')
print(f'pc2이 원본 데이터의 약 {explained_ratio[1]*100:.1f}% 정보를 담고있음')
print(f'단 2차원만으로 13차원 정보의 총 {sum(explained_ratio) * 100:.1f}%을 설명함')
sns.scatterplot(
    x="Principal Component 1",
    y="Principal Component 2",
    hue="target",palette=['red','blue','yellow'],data=df_pca,s=100, alpha=0.8
)
plt.xlabel(f'1st pc {explained_ratio[0]*100:.1f}%')
plt.ylabel(f'2st pc {explained_ratio[0]*100:.1f}%')
plt.show()