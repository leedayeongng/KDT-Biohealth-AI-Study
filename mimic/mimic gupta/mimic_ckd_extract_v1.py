import pandas as pd
import psycopg2

# db 연결
conn = psycopg2.connect(
    host='localhost', dbname='mimic4', user='bio4', password='bio4'
)
# sql 실행
query ="""
    
WITH ckd_hadm AS (
    -- 1. CKD cohort
    SELECT DISTINCT hadm_id
    FROM mimiciv_hosp.diagnoses_icd
    WHERE (icd_version = 9 AND icd_code LIKE '585%')
       OR (icd_version = 10 AND icd_code LIKE 'N18%')
)
,ckd_icu AS (
-- 2. ICU 연결
    SELECT 
           i.subject_id  -- 환자id 
	     , i.hadm_id     -- 입원id
	     , i.stay_id     -- icu체류id
	     , i.intime      -- 입원시간
	     , i.outtime     -- 퇴원시간
	     , i.los         -- 체류일
         , a.hospital_expire_flag
    FROM mimiciv_icu.icustays i
    JOIN mimiciv_hosp.admissions a
        ON i.hadm_id = a.hadm_id
    WHERE i.hadm_id IN (SELECT hadm_id FROM ckd_hadm)
)
,ckd_icu_48h as(
    -- 3. 48시간 이상 stay
SELECT *
FROM ckd_icu
WHERE outtime >= intime + INTERVAL '48 hour'
)
, vitals as(
		-- vital 
		select c.subject_id 
		      ,c.hadm_id 
		      ,c.stay_id 
		      ,c.intime 
		      ,ce.charttime 
		      ,ce.itemid 
		      ,ce.valuenum 
		      ,floor(extract(epoch from (ce.charttime - c.intime))/7200) as bin_2h
		from ckd_icu_48h c
		join mimiciv_icu.chartevents ce 
		on c.stay_id  = ce.stay_id 
		where ce.charttime between c.intime and c.intime + interval '48 hour'
		and ce.valuenum is not null
		and ce.itemid in (
		   	    220045, -- HR 심박수
				220179, -- sbp수축 혈압
				220180, -- dbp이와기 혈압
				220210, -- rr 호흡수
				220277, -- spo2혈중 산소 포화도
				223761  -- temp 체온 
		)
)
, labs as(
	-- lab 
	select c.subject_id
	      ,c.hadm_id
	      ,c.stay_id
	      ,c.intime
	      ,le.charttime
	      ,le.itemid
	      ,le.valuenum
	      ,floor(extract(epoch from (le.charttime-c.intime))/7200) as bin_2h
	from ckd_icu_48h c
	join mimiciv_hosp.labevents le
	on c.hadm_id = le.hadm_id 
	where le.charttime between c.intime and c.intime + interval '48 hour'
	and le.valuenum is not null
	and le.itemid in (
	   	    50912 , -- Creatinine 신장 기능 지표 (신부전 핵심)
	   	    51006 , -- BUN 혈중 요소 질소
	   	    50983 , -- Sodium 나트륨 (전해질)
	   	    50971 , -- Potassium 칼륨 (전해질)
	   	    50931 , -- Glucose 혈당 (Serum)
	   	    51301   -- WBC 백혈구 수치 (염증 지표)
	)
)
-- 최종 raw dataset
select v.subject_id
      ,v.hadm_id
      ,v.stay_id
      ,v.charttime
      ,v.itemid as vital_itemid
      ,v.valuenum as vital_value
      ,v.bin_2h
      ,l.itemid as lab_itemid
      ,l.valuenum as lab_value
      ,c.hospital_expire_flag as label_mortality
      ,case when c.los >= 3 then 1 else 0 end as label_icu_3day
from vitals v
left join labs l
on v.stay_id = l.stay_id 
and v.bin_2h = l.bin_2h
join ckd_icu_48h c
on v.stay_id = c.stay_id 
order by v.stay_id, v.bin_2h, v.charttime;
"""
# 저장
df = pd.read_sql(query, conn)
print('데이터 로드 완료:', df.shape)
import os
data_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data')
os.makedirs(data_dir, exist_ok=True)
df.to_csv(os.path.join(data_dir, 'mimic_raw_ckd_bin2h.csv'), index=False)
print(f'저장 완료: {data_dir}/mimic_raw_ckd_bin2h.csv')