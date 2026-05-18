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

#svm 이상치 탐지(oneclasssvm)
#nu:학습데이터중에서 이상치가 차지할 것이라 예상하는 비율 0-1.0
#gamma : 경계선 굴곡을 결정하는 파라미터(클수록 경계가 오밀조밀)
from sklearn.svm import OneClassSVM

model = OneClassSVM(nu=0.08, kernel='rbf',gamma=0.5)
model.fit(df.values)
predictions = model.predict(df.values)
df['Anomaly_SVM'] = predictions
outliers = len(df[df['Anomaly_SVM'] == -1])
print(f'이상치:{outliers} 개')
plt.figure(figsize=(10, 7))
#경계면을 그리기위한 격자생성
xx, yy = np.meshgrid(np.linspace(-9, 9, 500), np.linspace(-9, 9, 500))
#각 격자점에서의 거리,정수계산
z = model.decision_function(np.c_[xx.ravel(), yy.ravel()])
z = z.reshape(xx.shape)
plt.contour(xx, yy, z, levels=[0], linewidths=[0], colors='darkred')
plt.contour(xx, yy, z, levels=[0, z.max()], colors='palevioletred')
normal = df[df['Anomaly_SVM'] == 1]
plt.scatter(normal['Feature_1'], normal['Feature_2'],label='정상')
anomaly = df[df['Anomaly_SVM'] == -1]
plt.scatter(anomaly['Feature_1'], anomaly['Feature_2'],c='red', marker='x', label='이상치')
plt.show()


