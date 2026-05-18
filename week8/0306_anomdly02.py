import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# 한글 폰트 설정
plt.rcParams['font.family'] = 'Malgun Gothic'
plt.rcParams['axes.unicode_minus'] = False
# -------------------------------------------------------------
# [공통 데이터셋 생성] 5개의 예제에서 동일하게 사용할 2D 데이터
# -------------------------------------------------------------
np.random.seed(42)
# 1. 정상 군집 A (조밀한 그룹)
cluster_a = np.random.normal(loc=[2, 2], scale=[0.5, 0.5], size=(100, 2))
# 2. 정상 군집 B (좀 더 퍼진 그룹)
cluster_b = np.random.normal(loc=[-2, -2], scale=[0.8, 0.8], size=(100, 2))
# 3. 전역 이상치 (Global Outliers) - 완전히 동떨어진 곳
global_outliers = np.random.uniform(low=-8, high=8, size=(10, 2))
# 4. 국지적 이상치 (Local Outliers) - 군집 주변에 교묘하게 숨어있는
local_outliers_a = np.random.normal(loc=[3.5, 3.5], scale=[0.1, 0.1], size=(3, 2))
local_outliers_b = np.random.normal(loc=[-4, -4], scale=[0.1, 0.1], size=(2, 2))

# 모든 데이터 병합
X = np.vstack([cluster_a, cluster_b, global_outliers, local_outliers_a, local_outliers_b])
df = pd.DataFrame(X, columns=['Feature_1', 'Feature_2'])
print(f"2D 가상 데이터셋 총 {len(df)}개 샘플)\n")

from sklearn.cluster import DBSCAN
#군집화(DBSCAN) 방식 이상치 탐지
#eps(주변 변경) min_samples(최소 샘플수)없으면 -1 <--이상치로 분류
model = DBSCAN(eps=0.6, min_samples=4)
predictions = model.fit_predict(df.values)
df['Anomaly_DBSCAN'] = [1 if p!= -1 else -1 for p in predictions]
outliers_cnt = len(df[df['Anomaly_DBSCAN'] == -1])
print(f'총 {outliers_cnt}개의 이상치가 발견됨.')

plt.figure(figsize=(10,7))
normal = df[df['Anomaly_DBSCAN'] == 1]
plt.scatter(normal['Feature_1'], normal['Feature_2'],label='점심')
anomaly = df[df['Anomaly_DBSCAN'] == -1]
plt.scatter(anomaly['Feature_1'], anomaly['Feature_2'],label='이상화')
plt.show()
