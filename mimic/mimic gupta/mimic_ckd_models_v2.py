import os
import random
import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score, average_precision_score, roc_curve, precision_recall_curve
from xgboost import XGBClassifier
import matplotlib.pyplot as plt

# 성능 결과를 시각화하기 위해 각 타겟별 예측 확률을 저장할 전역 딕셔너리
results_m = {}
results_l = {}

# 재현성을 위한 난수 시드 고정
def seed_everything(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

seed_everything()

print("=========================================")
print(" MIMIC-IV CKD Pipeline V2 - Modeling")
print("=========================================")

data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
df_tab = pd.read_csv(os.path.join(data_dir, "mimic_ckd_feature_selected_v2.csv")) # 머신러닝용 (2D)
df_ts = pd.read_csv(os.path.join(data_dir, "mimic_ckd_time_series_v2.csv"))       # 딥러닝용 (3D)

print("Tabular shape (XGBoost V2):", df_tab.shape)

# ============================================================
# [A] Tabular 파트 (XGBoost)
# ============================================================
ID_COLS = ["stay_id"]
TARGET_COLS = ["label_mortality", "label_icu_3day"]

# 타겟과 ID를 제외한 모든 변수를 독립변수(X)로 사용합니다. (V2에서는 age, gender도 여기에 포함됩니다)
tab_features = [c for c in df_tab.columns if c not in ID_COLS + TARGET_COLS]

# 8:2 로 Train / Test 환자 그룹 분할
train_stays, test_stays = train_test_split(df_tab["stay_id"].unique(), test_size=0.2, random_state=42)

df_train_tab = df_tab[df_tab["stay_id"].isin(train_stays)].copy()
df_test_tab = df_tab[df_tab["stay_id"].isin(test_stays)].copy()

X_train_xgb = df_train_tab[tab_features].values
X_test_xgb = df_test_tab[tab_features].values

# 예측 타겟 1: 사망 여부 (Mortality)
y_train_m = df_train_tab["label_mortality"].values
y_test_m = df_test_tab["label_mortality"].values

# 예측 타겟 2: 중환자실 3일 초과 여부 (LOS > 3)
y_train_l = df_train_tab["label_icu_3day"].values
y_test_l = df_test_tab["label_icu_3day"].values

# 표준 단위를 맞추기 위한 스케일링
scaler = StandardScaler()
X_train_xgb_scaled = scaler.fit_transform(X_train_xgb)
X_test_xgb_scaled = scaler.transform(X_test_xgb)

# 데이터 불균형(사망자보다 생존자가 압도적으로 많음)을 해결하기 위한 가중치 함수
def get_scale_pos_weight(y):
    neg = (y == 0).sum()
    pos = (y == 1).sum()
    return neg / (pos + 1e-6) # 정답이 1인 소수 그룹이 틀렸을 때 주어지는 패널티 배율

# USE_GRID_SEARCH = False # 시간이 오래 걸리는 작업이므로 On/Off 스위치를 만듭니다.
USE_GRID_SEARCH = True # 시간이 오래 걸리는 작업이므로 On/Off 스위치를 만듭니다.

if USE_GRID_SEARCH:
    print("\n=== [V2 XGBoost] Mortality 최적 하이퍼파라미터 탐색 중 (GridSearchCV) ===")
    param_grid = {
        'n_estimators': [100, 300, 500, 800],
        'max_depth': [3, 5, 7, 9, 11],
        'learning_rate': [0.001, 0.005, 0.01, 0.05, 0.1]
    }
    
    # 🚨 의료 불균형 데이터 핵심: 단순 K-Fold가 아니라, 사망/생존 비율을 각 조각마다 똑같이 유지해주는 Stratified K-Fold를 써야 합니다!
    skf = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)
    
    # GridSearch 과정에서는 PR-AUC(average_precision)가 가장 높은 파라미터 조합을 찾도록 지시합니다.
    xgb_base_m = XGBClassifier(colsample_bytree=0.8, subsample=0.8, scale_pos_weight=get_scale_pos_weight(y_train_m), random_state=42, n_jobs=-1)
    grid_m = GridSearchCV(xgb_base_m, param_grid, cv=skf, scoring='average_precision', verbose=1)
    grid_m.fit(X_train_xgb_scaled, y_train_m)
    print(f"Mortality 최적 파라미터: {grid_m.best_params_}")
    xgb_m = grid_m.best_estimator_

    print("\n=== [V2 XGBoost] LOS > 3 최적 하이퍼파라미터 탐색 중 (GridSearchCV) ===")
    xgb_base_l = XGBClassifier(colsample_bytree=0.8, subsample=0.8, scale_pos_weight=get_scale_pos_weight(y_train_l), random_state=42, n_jobs=-1)
    grid_l = GridSearchCV(xgb_base_l, param_grid, cv=skf, scoring='average_precision', verbose=1)
    grid_l.fit(X_train_xgb_scaled, y_train_l)
    print(f"LOS>3 최적 파라미터: {grid_l.best_params_}")
    xgb_l = grid_l.best_estimator_

else:
    print("\n=== [V2 XGBoost] Mortality 모델 학습 (기본값) ===")
    xgb_m = XGBClassifier(n_estimators=300, max_depth=6, learning_rate=0.02, colsample_bytree=0.8, subsample=0.8,
                          scale_pos_weight=get_scale_pos_weight(y_train_m), random_state=42, n_jobs=-1)
    xgb_m.fit(X_train_xgb_scaled, y_train_m)

    print("=== [V2 XGBoost] LOS > 3 모델 학습 (기본값) ===")
    xgb_l = XGBClassifier(n_estimators=300, max_depth=6, learning_rate=0.02, colsample_bytree=0.8, subsample=0.8,
                          scale_pos_weight=get_scale_pos_weight(y_train_l), random_state=42, n_jobs=-1)
    xgb_l.fit(X_train_xgb_scaled, y_train_l)

def evaluate_metrics(y_true, prob, name="Model"):
    try:
        auc = roc_auc_score(y_true, prob)          # 불균형 데이터에서 가장 널리 쓰이는 평가 지표 (ROC 곡선 밑 면적)
        pr = average_precision_score(y_true, prob) # 양성 예측 비율 지표 (AUPRC)
    except:
        auc, pr = 0, 0
    print(f"{name} -> AUC-ROC: {auc:.4f} / PR-AUC: {pr:.4f}")
    return auc, pr

evaluate_metrics(y_test_m, xgb_m.predict_proba(X_test_xgb_scaled)[:, 1], "[V2 XGBoost] Mortality")
evaluate_metrics(y_test_l, xgb_l.predict_proba(X_test_xgb_scaled)[:, 1], "[V2 XGBoost] LOS > 3")

results_m["XGBoost"] = (y_test_m, xgb_m.predict_proba(X_test_xgb_scaled)[:, 1])
results_l["XGBoost"] = (y_test_l, xgb_l.predict_proba(X_test_xgb_scaled)[:, 1])


# ============================================================
# [B] Deep Learning 파트 (LSTM / TCN) 데이터 구축
# ============================================================
print("\n[Data] 딥러닝 입력을 위한 Mask 처리된 3D 텐서 빌드 중...")
MAX_BINS = 24
ts_features = [c for c in df_ts.columns if c not in ["stay_id", "bin_2h"]]

# 3D 텐서로 묶기 전 개별 변수별로 스케일링
df_ts[ts_features] = StandardScaler().fit_transform(df_ts[ts_features])

# 이 부분이 핵심입니다: 환자별로 데이터를 묶어 [환자수, 24(시간), 변수개수] 의 3D 텐서 덩어리를 만듭니다.
def build_dl_dataset(stays, df_labels):
    X_seq_list, X_static_list = [], []
    y_m_list, y_l_list = [], []
    
    grouped = df_ts.groupby("stay_id")
    for s_id in stays:
        # 1. 시계열 데이터(Sequence): (24, 28) 형태의 2D 행렬 1장이 1명의 환자 48시간 변화를 뜻합니다.
        try:
            mat = grouped.get_group(s_id).sort_values("bin_2h")[ts_features].values
        except KeyError:
            mat = np.zeros((MAX_BINS, len(ts_features)))
        X_seq_list.append(mat)
        
        # 2. 정적 데이터(Static & Label): 나이, 성별은 시간에 따라 변하지 않으므로 한쪽에 따로 뺍니다.
        row = df_labels[df_labels["stay_id"] == s_id].iloc[0]
        static = [float(row["anchor_age"]) / 100.0, float(row["gender"])] # 나이는 모델을 위해 100으로 나눠서 0~1 수준 스케일링
        X_static_list.append(static)
        
        # 3. 정답 (사망 여부, 장기 입원 여부)
        y_m_list.append(row["label_mortality"])
        y_l_list.append(row["label_icu_3day"])
        
    # PyTorch에서 돌아가도록 모든 리스트를 Tensor로 변환
    return (torch.tensor(np.array(X_seq_list), dtype=torch.float32),
            torch.tensor(np.array(X_static_list), dtype=torch.float32),
            torch.tensor(np.array(y_m_list), dtype=torch.float32),
            torch.tensor(np.array(y_l_list), dtype=torch.float32))

X_tr_seq, X_tr_stat, y_tr_m, y_tr_l = build_dl_dataset(train_stays, df_train_tab)
X_te_seq, X_te_stat, y_te_m, y_te_l = build_dl_dataset(test_stays, df_test_tab)


# ============================================================
# [C] Deep Learning 아키텍처 정의 (Hybrid Model)
# ============================================================
class HybridMIMICModel(nn.Module):
    """
    하이브리드 아키텍처 설계
    시간의 흐름이 담긴 시계열(Sequence) 정보는 LSTM/TCN에 통과시키고, 
    변하지 않는 나이/성별(Static) 정보는 마지막에 합쳐서 의사 결정을 내리는 실전 의료 인공지능 구조입니다.
    """
    def __init__(self, seq_in, static_in, model_type='lstm', hidden_dim=64):
        super(HybridMIMICModel, self).__init__()
        self.model_type = model_type
        
        if self.model_type == 'lstm':
            # 장/단기 기억을 모두 가진 LSTM 모듈
            self.rnn = nn.LSTM(seq_in, hidden_dim, num_layers=2, batch_first=True, dropout=0.3)
            
            # 최종 의사결정을 내릴 Fully Connected 구조
            self.fc = nn.Sequential(
                nn.Linear(hidden_dim + static_in, 32), # 시계열 출력 + 정적 정보 병합점
                nn.ReLU(), 
                nn.Dropout(0.3), 
                nn.Linear(32, 1) # 생사 여부 1개 출력
            )
            
        elif self.model_type == 'tcn':
            # 시간 축으로의 팽창 합성곱(Dilated Conv)을 활용한 시계열 심층 신경망(TCN) 블록
            self.conv1 = nn.Conv1d(seq_in, hidden_dim, kernel_size=3, padding=2, dilation=1)
            self.relu1 = nn.ReLU()
            self.bn1 = nn.BatchNorm1d(hidden_dim)
            self.conv2 = nn.Conv1d(hidden_dim, hidden_dim, kernel_size=3, padding=4, dilation=2)
            self.relu2 = nn.ReLU()
            self.bn2 = nn.BatchNorm1d(hidden_dim)
            self.fc = nn.Sequential(
                nn.Linear(hidden_dim + static_in, 32), 
                nn.ReLU(), 
                nn.Dropout(0.3), 
                nn.Linear(32, 1)
            )

    def forward(self, x_seq, x_stat):
        if self.model_type == 'lstm':
            out, _ = self.rnn(x_seq)
            # 환자의 48시간 흐름을 모두 겪고 난 '가장 마지막(last_out)' 기억 상태를 뽑아냄
            last_out = out[:, -1, :] 
            
        elif self.model_type == 'tcn':
            # Conv1D는 입력 모양이 반대여야 하므로 전치(Transpose)
            x = x_seq.transpose(1, 2)
            out = self.relu1(self.bn1(self.conv1(x)))
            out = self.relu2(self.bn2(self.conv2(out)))
            # 합성곱 연산이 끝난 후 가장 끝 시간대의 정보 추출
            last_out = out[:, :, -1]
            
        # 시계열 메모리와 환자 기본 정보(나이/성별) 결합 (Concatenate)
        # 예: [64차원 LSTM 지식] + [2차원 나이,성별 지식] = [66차원 융합 지식]
        combined = torch.cat([last_out, x_stat], dim=1)
        
        # 0과 1사이 확률로 리턴 (이진 분류)
        return torch.sigmoid(self.fc(combined).squeeze(-1))

def train_dl(X_seq_tr, X_stat_tr, y_tr, X_seq_te, X_stat_te, y_te, m_type, target_name):
    # PyTorch Data Loader에 묶어주기
    loader_tr = DataLoader(TensorDataset(X_seq_tr, X_stat_tr, y_tr), batch_size=128, shuffle=True)
    loader_te = DataLoader(TensorDataset(X_seq_te, X_stat_te, y_te), batch_size=128, shuffle=False)
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    # 딥러닝 모델 인스턴스 생성
    model = HybridMIMICModel(seq_in=len(ts_features), static_in=2, model_type=m_type, hidden_dim=256).to(device)
    
    # 불균형 데이터 패널티 세팅
    pos_weight = (y_tr == 0).sum() / ((y_tr == 1).sum() + 1e-6)
    criterion = nn.BCELoss(weight=None)
    
    # 옵티마이저 (기울기 최적화 가속기) 설정
    optimizer = optim.AdamW(model.parameters(), lr=1e-3, weight_decay=1e-4)

    print(f"\n=> Training [V2 {m_type.upper()}] for {target_name} on {device}")
    
    # 40 Epochs 반복 학습
    for epoch in range(20):
        model.train()
        for xs, xstat, yb in loader_tr:
            xs, xstat, yb = xs.to(device), xstat.to(device), yb.to(device)
            optimizer.zero_grad()
            preds = model(xs, xstat)
            
            # 불균형 정답에 대해, 소수 집단(1)을 틀린 경우 'pos_weight' 배율만큼 Loss(벌점)를 증폭시킵니다.
            w = torch.where(yb==1, pos_weight.clone().detach(), torch.ones_like(yb))
            loss = (criterion(preds, yb) * w).mean()
            
            loss.backward()
            optimizer.step()
            
    # Evaluation (평가)
    model.eval()
    all_preds = []
    with torch.no_grad():
        for xs, xstat, _ in loader_te:
            xs, xstat = xs.to(device), xstat.to(device)
            all_preds.extend(model(xs, xstat).cpu().numpy())
            
    prob = np.array(all_preds)
    evaluate_metrics(y_te.numpy(), prob, f"[V2 {m_type.upper()}] {target_name}")
    
    # 딕셔너리에 그래프용 데이터 저장
    if target_name == 'Mortality':
        results_m[m_type.upper()] = (y_te.numpy(), prob)
    else:
        results_l[m_type.upper()] = (y_te.numpy(), prob)

# 각 타겟과 딥러닝 알고리즘별로 4번의 학습 평가 진행
train_dl(X_tr_seq, X_tr_stat, y_tr_m, X_te_seq, X_te_stat, y_te_m, 'lstm', 'Mortality')
train_dl(X_tr_seq, X_tr_stat, y_tr_l, X_te_seq, X_te_stat, y_te_l, 'lstm', 'LOS > 3')

train_dl(X_tr_seq, X_tr_stat, y_tr_m, X_te_seq, X_te_stat, y_te_m, 'tcn', 'Mortality')
train_dl(X_tr_seq, X_tr_stat, y_tr_l, X_te_seq, X_te_stat, y_te_l, 'tcn', 'LOS > 3')

print("\n=== V2 벤치마크 평가가 완료되었습니다 ===")

def plot_curves(results_dict, target_title, filename):
    plt.figure(figsize=(12, 5))
    
    # 1. ROC Curve
    plt.subplot(1, 2, 1)
    for name, (y_t, y_p) in results_dict.items():
        fpr, tpr, _ = roc_curve(y_t, y_p)
        auc = roc_auc_score(y_t, y_p)
        plt.plot(fpr, tpr, label=f"{name} (AUC={auc:.3f})")
    plt.plot([0,1], [0,1], 'k--', label="Random (0.500)")
    plt.title(f"ROC Curve - {target_title}")
    plt.xlabel("False Positive Rate")
    plt.ylabel("True Positive Rate")
    plt.legend(loc="lower right")
    plt.grid(True, alpha=0.3)
    
    # 2. PR Curve
    plt.subplot(1, 2, 2)
    pos_ratio = 0
    for name, (y_t, y_p) in results_dict.items():
        prec, rec, _ = precision_recall_curve(y_t, y_p)
        pr = average_precision_score(y_t, y_p)
        plt.plot(rec, prec, label=f"{name} (PR={pr:.3f})")
        pos_ratio = sum(y_t)/len(y_t)
        
    plt.plot([0,1], [pos_ratio, pos_ratio], 'k--', label=f"Baseline ({pos_ratio:.3f})")
    plt.title(f"PR Curve - {target_title}")
    plt.xlabel("Recall (Sensitivity)")
    plt.ylabel("Precision (PPV)")
    plt.legend(loc="upper right")
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    print(f"그래프 저장 완료: {filename}")

save_dir = os.path.dirname(os.path.abspath(__file__))
plot_curves(results_m, "Target: Mortality", os.path.join(save_dir, "curve_mortality.png"))
plot_curves(results_l, "Target: LOS > 3 Days", os.path.join(save_dir, "curve_los.png"))
