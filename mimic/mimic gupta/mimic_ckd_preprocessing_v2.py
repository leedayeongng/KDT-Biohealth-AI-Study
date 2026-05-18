import pandas as pd
import numpy as np

print("=========================================")
print(" MIMIC-IV CKD Pipeline V2 - Preprocessing")
print("=========================================")

# 0. 파일 로드
import os
data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
df = pd.read_csv(os.path.join(data_dir, 'mimic_raw_ckd_bin2h_v2.csv'))
print('원본 데이터 크기:', df.shape)

# [V1 대비 변경점 1] 의식 수준(GCS)과 소변량(Urine) 특성이 새롭게 추가되었습니다.
ITEM_MAP = {
    220045: "hr",           
    220179: "sbp",          
    220180: "dbp",          
    220210: "rr",           
    220277: "spo2",         
    223761: "temp",         
    223901: "gcs",          # 의식 수준 (Glasgow Coma Scale: 3~15점)
    227489: "urine",        # 소변량 (신부전 환자에게 가장 중요한 지표 발탁)
    50912:  "creatinine",
    51006:  "bun",          
    50983:  "sodium",
    50971:  "potassium",
    50931:  "glucose",      
    51301:  "wbc"           
}

MAX_BINS = 24

# ==========================================================
# 1. 시계열이 아닌 '정적(Static) 데이터' 분리
# ==========================================================
# [V1 대비 변경점 2] 나이, 성별 등 시간이 지나도 변하지 않는 정적 데이터를 따로 추출합니다.
static_df = df[["subject_id", "hadm_id", "stay_id", "anchor_age", "gender", "label_mortality", "label_icu_3day"]].drop_duplicates().copy()
# 인공지능이 계산할 수 있도록 성별(M/F)을 숫자(1/0)로 변환 (Label Encoding)
static_df["gender"] = static_df["gender"].map({"M": 1, "m": 1, "F": 0, "f": 0}).fillna(0)

# ==========================================================
# 2. Time-series(시계열) 데이터 분리 및 Bin 필터
# ==========================================================
ts_df = df[["stay_id", "bin_2h", "itemid", "valuenum"]].dropna().copy()
ts_df = ts_df[(ts_df["bin_2h"] >= 0) & (ts_df["bin_2h"] < MAX_BINS)]

# 매핑 및 드롭
ts_df["feature_name"] = ts_df["itemid"].map(ITEM_MAP)
ts_df = ts_df.dropna(subset=["feature_name"]).copy()

# ==========================================================
# 3. 이상치 제거 (Outlier threshold 0.98 / 0.02)
# ==========================================================
def clip_outliers(long_df, feature_col="feature_name", value_col="valuenum"):
    clipped = []
    for feat, g in long_df.groupby(feature_col):
        lower = g[value_col].quantile(0.01) # 하위 1%
        upper = g[value_col].quantile(0.99) # 상위 1%
        g_copy = g.copy()
        g_copy[value_col] = g_copy[value_col].clip(lower, upper)
        clipped.append(g_copy)
    return pd.concat(clipped, ignore_index=True) if clipped else pd.DataFrame(columns=long_df.columns)

ts_df = clip_outliers(ts_df)

# ==========================================================
# 4. 2시간 단위 Aggregation & 5. Wide 변환
# ==========================================================
ts_bin = ts_df.groupby(["stay_id", "bin_2h", "feature_name"], as_index=False)["valuenum"].mean()

ts_wide = ts_bin.pivot_table(index=["stay_id", "bin_2h"], columns="feature_name", values="valuenum", aggfunc="mean").reset_index()
ts_wide.columns.name = None

all_stays = ts_wide["stay_id"].drop_duplicates().tolist()
full_index = pd.MultiIndex.from_product([all_stays, range(MAX_BINS)], names=["stay_id", "bin_2h"])
ts_wide = ts_wide.set_index(["stay_id", "bin_2h"]).reindex(full_index).reset_index()

# ==========================================================
# 6. 결측치 파악 (Mask Tensor 채널 생성용)
# ==========================================================
# 💡 [V1 대비 변경점 3] 가장 치명적인 차이점입니다!
# 이전에는 빈칸을 이전 값으로 막 채웠습니다. 하지만 딥러닝 모델 입장에선 "이게 진짜 방금 잰 수치인지, 10시간 전 수치를 복사해 온 건지" 알 턱이 없습니다.
# 그래서 병원에서 "실제로 검사를 수행했는지 여부(1/0)"를 별도의 Mask 채널(힌트)로 만들어서 AI에게 같이 줍니다.
feature_cols = [c for c in ts_wide.columns if c not in ["stay_id", "bin_2h"]]
for feat in feature_cols:
    ts_wide[f"{feat}_mask"] = ts_wide[feat].notna().astype(int)

# ==========================================================
# 7. 결측치 대치 (Forward Fill + Global Mean)
# ==========================================================
ts_wide = ts_wide.sort_values(["stay_id", "bin_2h"]).copy()
ts_wide[feature_cols] = ts_wide.groupby("stay_id")[feature_cols].ffill()

global_means = ts_wide[feature_cols].mean()
ts_wide[feature_cols] = ts_wide[feature_cols].fillna(global_means)

# ★ Deep Learning용 3D 텐서. (이제 Value 값과 그 값이 진짠지 알려주는 Mask 값이 2배로 불어나 있습니다)
ts_wide.to_csv(os.path.join(data_dir, "mimic_ckd_time_series_v2.csv"), index=False)
print("딥러닝(V2)용 Time Series 데이터 저장 완료 (Mask 포함): data/mimic_ckd_time_series_v2.csv")

# ==========================================================
# 8. Data Summary 통계 추출 (XGBoost용 2D 압축)
# ==========================================================
summary_frames = []
for feat in feature_cols:
    g = ts_wide.groupby("stay_id")[feat]
    g_mask = ts_wide.groupby("stay_id")[f"{feat}_mask"]

    # XGBoost는 시계열을 모르므로, 마스크 정보를 "결측률(Missing Rate)"이라는 1개의 실수값으로 요약해서 던져줍니다.
    feat_df = pd.DataFrame({
        f"{feat}_mean": g.mean(),
        f"{feat}_std": g.std(),
        f"{feat}_min": g.min(),
        f"{feat}_max": g.max(),
        f"{feat}_last": g.last(),
        f"{feat}_missing_rate": 1.0 - g_mask.mean() 
    })
    summary_frames.append(feat_df)

summary_df = pd.concat(summary_frames, axis=1).reset_index()

# 의학 지식 파생변수 생성 (맥압, 평균동맥압, BUN/Cr 비율)
derived_df = pd.DataFrame({"stay_id": ts_wide["stay_id"].unique()})
# 혈압
if set(["sbp", "dbp"]).issubset(set(feature_cols)):
    ts_wide["pulse_pressure"] = ts_wide["sbp"] - ts_wide["dbp"]
    ts_wide["map_calc"] = (ts_wide["sbp"] + 2 * ts_wide["dbp"]) / 3
    pp_stats = ts_wide.groupby("stay_id")["pulse_pressure"].agg(["mean", "max", "last"]).add_prefix("pulse_pressure_").reset_index()
    map_stats = ts_wide.groupby("stay_id")["map_calc"].agg(["mean", "min", "last"]).add_prefix("map_").reset_index()
    derived_df = derived_df.merge(pp_stats, on="stay_id", how="left").merge(map_stats, on="stay_id", how="left")
# BUN/Cr
if set(["bun", "creatinine"]).issubset(set(feature_cols)):
    tmp = ts_wide.groupby("stay_id")[["bun", "creatinine"]].last().reset_index()
    tmp["bun_creatinine_ratio_last"] = tmp["bun"] / (tmp["creatinine"] + 1e-6)
    derived_df = derived_df.merge(tmp[["stay_id", "bun_creatinine_ratio_last"]], on="stay_id", how="left")

# ==========================================================
# 9. 라벨 결합 및 Tabular 최종 데이터셋 구성
# ==========================================================
final_df = (
    static_df # 💡 [V1 대비] 나이, 성별 정보가 병합 과정 최상단에 붙습니다.
    .merge(summary_df, on="stay_id", how="left")
    .merge(derived_df, on="stay_id", how="left")
)

# 잔여 결측치 처리
num_cols = final_df.select_dtypes(include=[np.number]).columns.tolist()
final_df[num_cols] = final_df[num_cols].fillna(final_df[num_cols].mean())

model_df = final_df.drop(columns=["subject_id", "hadm_id"])
model_df.to_csv(os.path.join(data_dir, "mimic_ckd_feature_selected_v2.csv"), index=False)
print("XGBoost(V2)용 Tabular 데이터 저장 완료:", model_df.shape)
