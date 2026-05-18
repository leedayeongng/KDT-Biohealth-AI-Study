# ============================================================
# Deep Learning benchmark model for MIMIC-IV CKD Data
# PyTorch implementations: LSTM, TCN
# Machine Learning benchmark: XGBoost
# ============================================================

import os
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader, TensorDataset

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_auc_score, average_precision_score
from xgboost import XGBClassifier

# ============================================================
# 재현성을 위한 시드 고정
# ============================================================
def seed_everything(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)

seed_everything()

# ============================================================
# 1. 데이터 로드
# ============================================================
data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')

# Tabular Data (for XGBoost)
df_tabular = pd.read_csv(os.path.join(data_dir, "mimic_ckd_feature_selected.csv"))
# Time-Series Data (for Deep Learning)
df_ts = pd.read_csv(os.path.join(data_dir, "mimic_ckd_time_series.csv"))

print("Tabular shape (XGBoost):", df_tabular.shape)
print("Time-series shape (LSTM/TCN):", df_ts.shape)

ID_COLS = ["subject_id", "hadm_id", "stay_id"]
TARGET_COLS = ["label_mortality", "label_icu_3day"]
MAX_BINS = 24

# ============================================================
# 2. Train/Test Split (Subject 기반 분리)
# ============================================================
unique_subjects = df_tabular["subject_id"].unique()
train_subj, test_subj = train_test_split(unique_subjects, test_size=0.2, random_state=42)

# Tabular Indices (1 row per stay)
train_idx_tab = df_tabular["subject_id"].isin(train_subj)
test_idx_tab  = df_tabular["subject_id"].isin(test_subj)

df_train_tab = df_tabular[train_idx_tab].copy()
df_test_tab  = df_tabular[test_idx_tab].copy()

# ============================================================
# [Part A] 벤치마크 (XGBoost)
# ============================================================
tab_features = [c for c in df_tabular.columns if c not in ID_COLS + TARGET_COLS]
X_train_xgb = df_train_tab[tab_features].values
X_test_xgb  = df_test_tab[tab_features].values

y_train_mort = df_train_tab["label_mortality"].values
y_test_mort  = df_test_tab["label_mortality"].values
y_train_los  = df_train_tab["label_icu_3day"].values
y_test_los   = df_test_tab["label_icu_3day"].values

scaler = StandardScaler()
X_train_xgb = scaler.fit_transform(X_train_xgb)
X_test_xgb  = scaler.transform(X_test_xgb)

def get_scale_pos_weight(y):
    neg = (y == 0).sum()
    pos = (y == 1).sum()
    return neg / (pos + 1e-6)

print("\n=== [XGBoost] Mortality 모델 학습 ===")
xgb_mort = XGBClassifier(n_estimators=100, max_depth=4, learning_rate=0.05, 
                         scale_pos_weight=get_scale_pos_weight(y_train_mort), random_state=42)
xgb_mort.fit(X_train_xgb, y_train_mort)

print("=== [XGBoost] LOS > 3 모델 학습 ===")
xgb_los = XGBClassifier(n_estimators=100, max_depth=4, learning_rate=0.05, 
                        scale_pos_weight=get_scale_pos_weight(y_train_los), random_state=42)
xgb_los.fit(X_train_xgb, y_train_los)

def evaluate_metrics(y_true, prob, name="Model"):
    try:
        auc = roc_auc_score(y_true, prob)
        pr = average_precision_score(y_true, prob)
    except Exception as e:
        auc, pr = 0, 0
    print(f"{name} -> AUC-ROC: {auc:.4f} / PR-AUC: {pr:.4f}")
    return auc, pr

evaluate_metrics(y_test_mort, xgb_mort.predict_proba(X_test_xgb)[:, 1], "[XGBoost] Mortality")
evaluate_metrics(y_test_los, xgb_los.predict_proba(X_test_xgb)[:, 1], "[XGBoost] LOS > 3")


# ============================================================
# [Part B] 딥러닝 데이터셋 준비 (Tensor 3D 생성)
# ============================================================
ts_features = [c for c in df_ts.columns if c not in ["stay_id", "bin_2h"]]
n_features = len(ts_features)

# Time Series df의 stay_id 순서가 df_tabular 순서와 일치하도록 생성
# df_tabular의 stay_id 목록 가져오기
train_stays = df_train_tab["stay_id"].tolist()
test_stays  = df_test_tab["stay_id"].tolist()

# df_ts를 stay_id 기준으로 묶어서 Dict로 만들기 (가속화)
# 각 stay는 24개의 sequence elements를 가짐
ts_scaler = StandardScaler()
df_ts[ts_features] = ts_scaler.fit_transform(df_ts[ts_features]) # (전체 scale로 시퀀스 스케일링)

def create_3d_tensor(stays, df_labels):
    X_list = []
    y_mort_list = []
    y_los_list = []
    
    grouped = df_ts.groupby("stay_id")
    for s_id in stays:
        # 1. 시계열 가져오기 (24 steps, n_features)
        try:
            mat = grouped.get_group(s_id).sort_values("bin_2h")[ts_features].values
        except KeyError:
            # 결측 시 0 패딩 (예비용)
            mat = np.zeros((MAX_BINS, n_features))
        X_list.append(mat)
        
        # 2. 라벨 가져오기
        row = df_labels[df_labels["stay_id"] == s_id].iloc[0]
        y_mort_list.append(row["label_mortality"])
        y_los_list.append(row["label_icu_3day"])
        
    return np.array(X_list), np.array(y_mort_list), np.array(y_los_list)

X_train_ts, y_train_ts_m, y_train_ts_l = create_3d_tensor(train_stays, df_train_tab)
X_test_ts,  y_test_ts_m,  y_test_ts_l  = create_3d_tensor(test_stays, df_test_tab)

X_train_tensor = torch.tensor(X_train_ts, dtype=torch.float32)
X_test_tensor  = torch.tensor(X_test_ts, dtype=torch.float32)

y_train_tensor_m = torch.tensor(y_train_ts_m, dtype=torch.float32)
y_test_tensor_m  = torch.tensor(y_test_ts_m, dtype=torch.float32)

y_train_tensor_l = torch.tensor(y_train_ts_l, dtype=torch.float32)
y_test_tensor_l  = torch.tensor(y_test_ts_l, dtype=torch.float32)

# ============================================================
# 3. 모델 정의 (LSTM, TCN)
# ============================================================
# TCN Helper Modules
class Chomp1d(nn.Module):
    def __init__(self, chomp_size):
        super(Chomp1d, self).__init__()
        self.chomp_size = chomp_size

    def forward(self, x):
        return x[:, :, :-self.chomp_size].contiguous()

class TemporalBlock(nn.Module):
    def __init__(self, n_inputs, n_outputs, kernel_size, stride, dilation, padding, dropout=0.2):
        super(TemporalBlock, self).__init__()
        self.conv1 = nn.Conv1d(n_inputs, n_outputs, kernel_size,
                               stride=stride, padding=padding, dilation=dilation)
        self.chomp1 = Chomp1d(padding)
        self.relu1 = nn.ReLU()
        self.dropout1 = nn.Dropout(dropout)

        self.conv2 = nn.Conv1d(n_outputs, n_outputs, kernel_size,
                               stride=stride, padding=padding, dilation=dilation)
        self.chomp2 = Chomp1d(padding)
        self.relu2 = nn.ReLU()
        self.dropout2 = nn.Dropout(dropout)

        self.net = nn.Sequential(self.conv1, self.chomp1, self.relu1, self.dropout1,
                                 self.conv2, self.chomp2, self.relu2, self.dropout2)
        self.downsample = nn.Conv1d(n_inputs, n_outputs, 1) if n_inputs != n_outputs else None
        self.relu = nn.ReLU()

    def forward(self, x):
        out = self.net(x)
        res = x if self.downsample is None else self.downsample(x)
        return self.relu(out + res)

class TemporalConvNet(nn.Module):
    def __init__(self, num_inputs, num_channels, kernel_size=2, dropout=0.2):
        super(TemporalConvNet, self).__init__()
        layers = []
        num_levels = len(num_channels)
        for i in range(num_levels):
            dilation_size = 2 ** i
            in_channels = num_inputs if i == 0 else num_channels[i-1]
            out_channels = num_channels[i]
            layers += [TemporalBlock(in_channels, out_channels, kernel_size, stride=1, dilation=dilation_size,
                                     padding=(kernel_size-1) * dilation_size, dropout=dropout)]
        self.network = nn.Sequential(*layers)

    def forward(self, x):
        return self.network(x)

class MIMICModel(nn.Module):
    """LSTM 또는 TCN을 선택할 수 있는 범용 래퍼 클래스"""
    def __init__(self, input_size, model_type='lstm', hidden_dim=32):
        super(MIMICModel, self).__init__()
        self.model_type = model_type
        
        if self.model_type == 'lstm':
            self.rnn = nn.LSTM(input_size=input_size, hidden_size=hidden_dim, 
                               num_layers=1, batch_first=True, dropout=0.2 if hidden_dim>1 else 0)
            self.fc = nn.Linear(hidden_dim, 1)
        elif self.model_type == 'tcn':
            # 2-layer TCN
            self.tcn = TemporalConvNet(input_size, num_channels=[hidden_dim, hidden_dim], kernel_size=3)
            self.fc = nn.Linear(hidden_dim, 1)
            
    def forward(self, x):
        # x: (batch, seq_len, features)
        if self.model_type == 'lstm':
            out, (hn, cn) = self.rnn(x)  # out: (batch, seq, hidden)
            last_out = out[:, -1, :]     # 마지막 timestep (batch, hidden)
            return torch.sigmoid(self.fc(last_out).squeeze(-1))
            
        elif self.model_type == 'tcn':
            x = x.transpose(1, 2)        # (batch, features, seq_len) - Conv1d 대응
            out = self.tcn(x)            # (batch, hidden_dim, seq_len)
            last_out = out[:, :, -1]     # 마지막 timestep
            return torch.sigmoid(self.fc(last_out).squeeze(-1))

# ============================================================
# 4. 모델 훈련 함수
# ============================================================
def train_dl_model(X_tr, y_tr, X_val, y_val, model_type, target_name):
    # Dataloader 생성
    batch_size = 64
    train_dataset = TensorDataset(X_tr, y_tr)
    val_dataset   = TensorDataset(X_val, y_val)
    train_loader  = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
    val_loader    = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    # 모델 초기화
    model = MIMICModel(input_size=n_features, model_type=model_type, hidden_dim=32).to(device)
    
    # 불균형 데이터 보정을 위한 BCE weight 설정
    pos_weight = (y_tr == 0).sum() / ((y_tr == 1).sum() + 1e-6)
    
    # BCELoss 사용 (마지막에 sigmoid를 씌움)
    # 직접 BCELoss 쓰거나 (sigmoid 포함된 구조) / 여기선 sigmoid를 모델에 포함함
    criterion = nn.BCELoss(weight=None) 
    
    # optimizer
    optimizer = optim.Adam(model.parameters(), lr=1e-3, weight_decay=1e-5)
    
    print(f"\n=> Training {model_type.upper()} for {target_name} on {device}")
    
    epochs = 15
    for epoch in range(epochs):
        model.train()
        total_loss = 0
        
        for xb, yb in train_loader:
            xb, yb = xb.to(device), yb.to(device)
            
            optimizer.zero_grad()
            preds = model(xb)
            
            # Loss 계산 시 positive weight 적용
            loss = criterion(preds, yb)
            # 수동으로 weight 계산
            weight = torch.where(yb == 1, pos_weight.clone().detach(), torch.ones_like(yb))
            loss = (loss * weight).mean()
            
            loss.backward()
            optimizer.step()
            total_loss += loss.item()
            
    # Evaluation
    model.eval()
    all_preds = []
    all_labels = []
    with torch.no_grad():
         for xb, yb in val_loader:
             xb = xb.to(device)
             preds = model(xb).cpu().numpy()
             all_preds.extend(preds)
             all_labels.extend(yb.numpy())
             
    all_preds = np.array(all_preds)
    all_labels = np.array(all_labels)
    
    evaluate_metrics(all_labels, all_preds, f"[{model_type.upper()}] {target_name}")
    return model

# ============================================================
# 5. 모델 학습 및 평가 파이프라인
# ============================================================

# 5.1 LSTM Train/Eval
lstm_morticity = train_dl_model(X_train_tensor, y_train_tensor_m, X_test_tensor, y_test_tensor_m, 'lstm', 'Mortality')
lstm_los       = train_dl_model(X_train_tensor, y_train_tensor_l, X_test_tensor, y_test_tensor_l, 'lstm', 'LOS > 3')

# 5.2 TCN Train/Eval
tcn_morticity = train_dl_model(X_train_tensor, y_train_tensor_m, X_test_tensor, y_test_tensor_m, 'tcn', 'Mortality')
tcn_los       = train_dl_model(X_train_tensor, y_train_tensor_l, X_test_tensor, y_test_tensor_l, 'tcn', 'LOS > 3')

print("\n--- 모든 학습 및 벤치마크 평가가 완료되었습니다 ---")
