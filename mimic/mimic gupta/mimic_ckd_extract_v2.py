import pandas as pd
import psycopg2

# db 연결
conn = psycopg2.connect(
    host='localhost', dbname='mimic4', user='bio4', password='bio4'
)

query = """
WITH ckd_hadm AS (
    -- 1. CKD cohort
    SELECT DISTINCT hadm_id
    FROM mimiciv_hosp.diagnoses_icd
    WHERE (icd_version = 9 AND icd_code LIKE '585%')
       OR (icd_version = 10 AND icd_code LIKE 'N18%')
)
, ckd_icu AS (
    -- 2. ICU 연결과 환자 Demographics(Age, Gender) 추가
    SELECT 
           i.subject_id
         , i.hadm_id
         , i.stay_id
         , i.intime
         , i.outtime
         , i.los
         , a.hospital_expire_flag
         , p.anchor_age
         , p.gender
    FROM mimiciv_icu.icustays i
    JOIN mimiciv_hosp.admissions a ON i.hadm_id = a.hadm_id
    JOIN mimiciv_hosp.patients p ON i.subject_id = p.subject_id
    WHERE i.hadm_id IN (SELECT hadm_id FROM ckd_hadm)
)
, ckd_icu_48h AS (
    -- 3. 48시간 이상 stay
    SELECT *
    FROM ckd_icu
    WHERE outtime >= intime + INTERVAL '48 hour'
)
, events_union AS (
    -- 4. Vitals & GCS (chartevents)
    SELECT c.stay_id, ce.charttime, ce.itemid, ce.valuenum,
           FLOOR(EXTRACT(EPOCH FROM (ce.charttime - c.intime))/7200) AS bin_2h
    FROM ckd_icu_48h c
    JOIN mimiciv_icu.chartevents ce ON c.stay_id = ce.stay_id
    WHERE ce.charttime BETWEEN c.intime AND c.intime + INTERVAL '48 hour'
      AND ce.valuenum IS NOT NULL
      AND ce.itemid IN (
          220045, -- HR
          220179, -- SBP
          220180, -- DBP
          220210, -- RR
          220277, -- SpO2
          223761, -- Temp
          223901  -- GCS Total
      )
      
    UNION ALL
    
    -- 5. Labs (labevents)
    SELECT c.stay_id, le.charttime, le.itemid, le.valuenum,
           FLOOR(EXTRACT(EPOCH FROM (le.charttime - c.intime))/7200) AS bin_2h
    FROM ckd_icu_48h c
    JOIN mimiciv_hosp.labevents le ON c.hadm_id = le.hadm_id
    WHERE le.charttime BETWEEN c.intime AND c.intime + INTERVAL '48 hour'
      AND le.valuenum IS NOT NULL
      AND le.itemid IN (
          50912, -- Creatinine
          51006, -- BUN
          50983, -- Sodium
          50971, -- Potassium
          50931, -- Glucose
          51301  -- WBC
      )
      
    UNION ALL
    
    -- 6. Urine Output (outputevents)
    SELECT c.stay_id, oe.charttime, oe.itemid, oe.value AS valuenum,
           FLOOR(EXTRACT(EPOCH FROM (oe.charttime - c.intime))/7200) AS bin_2h
    FROM ckd_icu_48h c
    JOIN mimiciv_icu.outputevents oe ON c.stay_id = oe.stay_id
    WHERE oe.charttime BETWEEN c.intime AND c.intime + INTERVAL '48 hour'
      AND oe.value IS NOT NULL
      AND oe.itemid = 227489   -- Urine Output
)

-- 최종 Raw Dataset 생성
SELECT 
      c.subject_id
    , c.hadm_id
    , c.stay_id
    , c.anchor_age
    , c.gender
    , c.hospital_expire_flag AS label_mortality
    , CASE WHEN c.los >= 3 THEN 1 ELSE 0 END AS label_icu_3day
    , e.charttime
    , e.itemid
    , e.valuenum
    , e.bin_2h
FROM events_union e
JOIN ckd_icu_48h c ON e.stay_id = c.stay_id
ORDER BY c.stay_id, e.bin_2h, e.charttime;
"""

print("SQL 쿼리 실행 중 (V2 파이프라인)...")
df = pd.read_sql(query, conn)
print('데이터 추출 완료:', df.shape)

df.to_csv('mimic_raw_ckd_bin2h_v2.csv', index=False)
print('저장 완료: mimic_raw_ckd_bin2h_v2.csv')
