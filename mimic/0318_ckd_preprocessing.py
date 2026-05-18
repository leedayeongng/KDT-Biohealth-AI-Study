# feature enginnering gupta, 2202 기준
# 2 hour time series resolution
# first 48h
# outlier threshold 0.98
# forward fill + mean imputation
# data summary for features
# labs/vitals + diagnosis feature

import pandas as pd
import numpy as np
df = pd.read_csv('mimic_raw_ckd_bin2h.csv')
print('원본:',df.shape)
#features 생성을 위해 item map 생성
ITEM_MAP = {
    220045:"HR",
    220179:"SBP",
    220180:"DBP",
    220210:"RR",
    220277:"SPO2",
    223761:"TEMP"
}
#bin 범위 체크
df = df[(df['bin_2h']>=0)&(df['bin_2h']<24)].copy()
print('48시간/2시간 bin 필터 후:', df.shape)
#vital/lab 분리 (feature 생성 위해)
#outlier(이상치)제거