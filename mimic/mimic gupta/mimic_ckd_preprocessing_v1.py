# feature engineering gupta, 2202 기준
# 2 hour time series resolution
# first 48h
# outlier threshold 0.98
# forward fill + mean imputation
# data summary for features
# labs/vitals + diagnosis feature

import pandas as pd
import numpy as np

# ============================================================
# 0. 파일 로드 및 변수 매핑 사전 정의
# ============================================================
# 환자별 시계열 데이터가 세로로 길게(Long Format) 정리된 원본 파일을 로드합니다.
import os
data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
df = pd.read_csv(os.path.join(data_dir, 'mimic_raw_ckd_bin2h.csv'))
print('원본 데이터 크기:', df.shape)

# MIMIC 데이터베이스 고유의 검사 코드 번호(itemid)를 우리가 알아보기 쉬운 이름으로 변환합니다.
ITEM_MAP = {
    220045: "hr",           # 심박수 (Heart Rate)
    220179: "sbp",          # 수축기 혈압 (Systolic BP)
    220180: "dbp",          # 이완기 혈압 (Diastolic BP)
    220210: "rr",           # 호흡수 (Respiratory Rate)
    220277: "spo2",         # 산소 포화도 (Oxygen Saturation)
    223761: "temp",         # 체온 (Temperature)
    50912:  "creatinine",   # 크레아티닌 (신장 손상 지표)
    51006:  "bun",          # 혈중 요소 질소 (신장 손상 지표)
    50983:  "sodium",       # 나트륨
    50971:  "potassium",    # 칼륨
    50931:  "glucose",      # 혈당
    51301:  "wbc"           # 백혈구 수치 (감염 지표)
}

# ============================================================
# 1. 관찰 기간(Bin) 제한: 입원 직후 48시간까지만
# ==========================================
# 빈(Bin) 1개가 2시간짜리 묶음이므로, 최대 24개의 Bin만 취합니다. (2시간 x 24 = 48시간)
# 즉, ICU에 들어오고 나서 "처음 48시간 동안의 변화"만 보고 생사나 질병 예후를 예측하겠다는 뜻입니다.
MAX_BINS = 24
df = df[(df["bin_2h"] >= 0) & (df["bin_2h"] < MAX_BINS)].copy()
print("48시간/2시간 bin 필터 후:", df.shape)

# ============================================================
# 2. Vital(생체신호) / Lab(혈액검사) 분리 및 이상치(Outlier) 제거
# ============================================================
# 생체신호와 혈액검사 수치를 분리하여 처리합니다.
vital_long = df[["stay_id", "bin_2h", "vital_itemid", "vital_value"]].dropna().copy()
lab_long   = df[["stay_id", "bin_2h", "lab_itemid", "lab_value"]].dropna().copy()

vital_long["vital_itemid"] = vital_long["vital_itemid"].astype(int)
lab_long["lab_itemid"] = lab_long["lab_itemid"].astype(int)

# ITEM_MAP을 사용해 코드 숫자를 실제 영문 이름('hr', 'sbp' 등)으로 교체
vital_long["feature_name"] = vital_long["vital_itemid"].map(ITEM_MAP)
lab_long["feature_name"] = lab_long["lab_itemid"].map(ITEM_MAP)

# 사전(Map)에 등록되지 않은 불필요한 검사 결과들은 쳐냅니다.
vital_long = vital_long.dropna(subset=["feature_name"]).copy()
lab_long = lab_long.dropna(subset=["feature_name"]).copy()

vital_long = vital_long.rename(columns={"vital_value": "value"})
lab_long = lab_long.rename(columns={"lab_value": "value"})

# 💡 [이상치 클리핑 함수]
# 데이터 입력 실수나 극단적인 값이 학습을 망치는 것을 방지합니다.
# 하위 1%(lower_q)보다 작은 값은 1% 값으로 강제 상승, 상위 99%(upper_q) 넘어가는 값은 99% 값으로 깎아냅니다(clip).
def clip_outliers_by_feature(long_df, value_col="value", feature_col="feature_name", lower_q=0.01, upper_q=0.99):
    clipped_values = []
    for feat, g in long_df.groupby(feature_col):
        lower = g[value_col].quantile(lower_q)
        upper = g[value_col].quantile(upper_q)
        g_copy = g.copy()
        g_copy[value_col] = g_copy[value_col].clip(lower, upper)
        clipped_values.append(g_copy)
    return pd.concat(clipped_values, ignore_index=True) if clipped_values else pd.DataFrame(columns=long_df.columns)

vital_long = clip_outliers_by_feature(vital_long)
lab_long   = clip_outliers_by_feature(lab_long)

# ============================================================
# 3. 2시간 Bin 단위 병합(Aggregation) 및 Wide 변환
# ============================================================
# 동일한 2시간 범위(bin) 안에 혈압이나 심박수를 여러 번 쟀을 수 있으므로, 그것들을 평균(mean)내서 1개의 값으로 통일합니다.
vital_bin = vital_long.groupby(["stay_id", "bin_2h", "feature_name"], as_index=False)["value"].mean()
lab_bin = lab_long.groupby(["stay_id", "bin_2h", "feature_name"], as_index=False)["value"].mean()
ts_long = pd.concat([vital_bin, lab_bin], ignore_index=True)

# 💡 Wide(널찍한) 테이블로 변환
# 행(Row)은 '환자ID + 시간대' 가 되고, 열(Column)은 '혈압', '혈당' 같은 특성들이 되도록 표 구조를 피벗(Pivot)합니다.
ts_wide = ts_long.pivot_table(index=["stay_id", "bin_2h"], columns="feature_name", values="value", aggfunc="mean").reset_index()
ts_wide.columns.name = None

# 환자마다 누락된 시간대 블록이 있을 수 있으니, 모든 환자가 정확히 0~23 (24칸)의 타임 블록을 가지도록 빈 칸을 강제로 끼워 넣습니다.
all_stays = ts_wide["stay_id"].drop_duplicates().tolist()
full_index = pd.MultiIndex.from_product([all_stays, range(MAX_BINS)], names=["stay_id", "bin_2h"])
ts_wide = ts_wide.set_index(["stay_id", "bin_2h"]).reindex(full_index).reset_index()

# ============================================================
# 4. 결측치 채우기 (Imputation: Forward fill + Mean)
# ============================================================
feature_cols = [c for c in ts_wide.columns if c not in ["stay_id", "bin_2h"]]
ts_wide = ts_wide.sort_values(["stay_id", "bin_2h"]).copy()

# 💡 Forward Fill (앞의 값 끌어다 채우기)
# 병원에서는 피검사를 매시간 하지 않으므로 듬성듬성 빈칸이 많습니다.
# "환자의 이전 시간대 검사 수치가 변하지 않고 그대로 유지된다" 라는 의학적 가정하에 빈칸을 채웁니다(ffill).
ts_wide[feature_cols] = ts_wide.groupby("stay_id")[feature_cols].ffill()

# 환자가 입원 직후 피검사를 안해서 이전 값조차 없다면, 전체 환자의 평균(global_means)으로 채워 넣습니다.
global_means = ts_wide[feature_cols].mean()
ts_wide[feature_cols] = ts_wide[feature_cols].fillna(global_means)
# 환자 1명당 정확히 24개의 히스토리 라인이 완성되었습니다.
# 이는 LSTM, TCN 같은 3D 시계열 딥러닝 모델의 입력으로 쓰기 완벽한 형태입니다.
ts_wide.to_csv(os.path.join(data_dir, "mimic_ckd_time_series.csv"), index=False)
print("딥러닝 학습용 Time Series 데이터 저장 완료: data/mimic_ckd_time_series.csv")

# ============================================================
# 5. Data Summary Feature 생성 (XGBoost, Random Forest 용)
# ============================================================
# 머신러닝 알고리즘들은 "시간 흐름"을 모릅니다. 환자 1명당 1줄의 데이터만 줘야 합니다.
# 48시간(24개의 묶음)을 가로로 길게 눌러서, 평균/최대치/최소치 같은 통계 정보를 요약(Summary)합니다.
summary_frames = []
for feat in feature_cols:
    g = ts_wide.groupby("stay_id")[feat]
    feat_df = pd.DataFrame({
        f"{feat}_mean": g.mean(), # 48시간 평균
        f"{feat}_std": g.std(),   # 변화량(표준편차)
        f"{feat}_min": g.min(),   # 최소값
        f"{feat}_max": g.max(),   # 최대값
        f"{feat}_last": g.last(), # 마지막 측정값 (퇴원 직전의 최신 상태)
    })
    summary_frames.append(feat_df)
summary_df = pd.concat(summary_frames, axis=1).reset_index()

# 💡 결측률 변수 추가
# 검사를 안했다는 사실 자체(결측률)도 정보가 됨. (아프면 검사를 많이 하니까)
raw_wide = ts_long.pivot_table(index=["stay_id", "bin_2h"]
, columns="feature_name", values="value", aggfunc="mean").reset_index()
raw_wide.columns.name = None
raw_wide = raw_wide.set_index(["stay_id", "bin_2h"]).reindex(full_index).reset_index()
raw_feature_cols = [c for c in raw_wide.columns if c not in ["stay_id", "bin_2h"]]

missing_rate_df = raw_wide.groupby("stay_id")[raw_feature_cols].apply(lambda x: x.isna().mean())
missing_rate_df.columns = [f"{c}_missing_rate" for c in missing_rate_df.columns]
missing_rate_df = missing_rate_df.reset_index()
summary_df = summary_df.merge(missing_rate_df, on="stay_id", how="left")

# ============================================================
# 7. 라벨 결합 및 Tabular(2D 표) 최종 데이터셋 구성 (파생변수 제외 - 논문 Baseline)
# ============================================================
# 환자 기본 정보와 타겟 정답(사망 여부, 중환자실 3일 초과 여부)을 붙입니다.
labels = df[["stay_id", "label_mortality", "label_icu_3day"]].drop_duplicates().copy()
id_df = df[["subject_id", "hadm_id", "stay_id"]].drop_duplicates().copy()

final_df = (
    id_df
    .merge(summary_df, on="stay_id", how="left")
    .merge(labels, on="stay_id", how="left")
)

# 자잘한 빈칸들을 최종적으로 열 평균값으로 채움
num_cols = final_df.select_dtypes(include=[np.number]).columns.tolist()
final_df[num_cols] = final_df[num_cols].fillna(final_df[num_cols].mean())

# 💡 Feature Selection (쓰레기 방출)
# 모든 환자가 빈칸이 무려 80%를 넘거나, 모든 환자의 데이터가 똑같아서(nunique <= 1) 아무 변별력이 없는 칼럼을 버석버석 쳐냅니다.
feature_cols_final = [c for c in final_df.columns if c not in ["subject_id", "hadm_id", "stay_id", "label_mortality", "label_icu_3day"]]
drop_candidates = [c for c in feature_cols_final if final_df[c].isna().mean() > 0.80 or final_df[c].nunique() <= 1]
selected_features = [c for c in feature_cols_final if c not in drop_candidates]

model_df = final_df[["subject_id", "hadm_id", "stay_id", "label_mortality", "label_icu_3day"] + selected_features].copy()

print("최종 선택된 Tabular feature 수:", len(selected_features))
print("최종 크기:", model_df.shape)

# 환자당 1열씩 1차원으로 쭉 눌러담긴 데이터. XGBoost/LightGBM 같은 트리 기반 머신러닝에 직행할 수 있습니다.
model_df.to_csv(os.path.join(data_dir, "mimic_ckd_feature_selected.csv"), index=False)
print("XGBoost용 Tabular 데이터 저장 완료: data/mimic_ckd_feature_selected.csv")
