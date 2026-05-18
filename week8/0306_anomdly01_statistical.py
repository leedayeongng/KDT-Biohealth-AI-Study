import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import lineStyles

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

#iqr 방식 이상치 탐지

def get_outliers_iqr(data, column):
    #1사분위수 (q1) 3사분위수 (q3) 계산
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)

    #IQR (중간 50%)
    IQR = Q3 - Q1
    #상한선과 하한선 (보통 1.5배수 사용)
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    #이상치
    outlier_idx = data[(data[column] > upper_bound) | (data[column] < lower_bound)].index
    return outlier_idx, lower_bound, upper_bound
outlier_idx_f1, f1_low, f1_high = get_outliers_iqr(df, 'Feature_1')
outlier_idx_f2, f2_low, f2_high = get_outliers_iqr(df, 'Feature_2')
#두특성중 하나라도 상자를 벗어난 데이터는 최종이상치로 판단
final_outliers = list(set(outlier_idx_f1).union(set(outlier_idx_f2)))
print(f'총{len(final_outliers)}개의 이상치가 발견됨')
df['Anomaly_IQR'] = 1
df.loc[final_outliers, 'Anomaly_IQR'] = -1
plt.figure(figsize=(10, 7))
#정상 데이터 회색
normal_data = df[df['Anomaly_IQR'] == 1]
plt.scatter(normal_data['Feature_1'], normal_data['Feature_2'], c='lightgray', label = '정상데이터')
anomaly_data = df[df['Anomaly_IQR'] == -1]
plt.scatter(anomaly_data['Feature_1'],anomaly_data['Feature_2'],c='red',marker='x',label='이상치')
#경계선
plt.axvline(f1_low, color='blue', linestyle='--', label='feature 1 경계(하한)')
plt.axvline(f1_high, color='blue', linestyle='--', label='feature 1 경계(상한)')

plt.axhline(f2_low, color='green', linestyle=':', label='feature 2 경계(하한)')
plt.axhline(f2_high, color='green', linestyle=':', label='feature 2 경계(상한)')
plt.xlabel('Feature_1')
plt.ylabel('Feature_2')
plt.show()