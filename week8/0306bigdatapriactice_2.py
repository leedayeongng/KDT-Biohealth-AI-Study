#- **trash_bag** 데이터셋은 지역별 종량제 봉투 가격에 대한 정보를 포함한다.

import pandas as pd
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# 데이터 로드
df = pd.read_csv(
    'https://raw.githubusercontent.com/YoungjinBD/dataset/main/trash_bag.csv',
    encoding='cp949'
)
print(df.head(5))

#각 용량별 가격 컬럼은 각 항의 조건을 만족하는 해당 종량제 봉투가 존재하면
# 가격을 값으로, 존재하지 않으면 0을 값으로 갖는다.
#1.용도가 ’음식물쓰레기’이고 사용
# 대상이 ’가정용’인 2L 봉투 가격의 평균을 정수로 출력하시오. (소수점 내림)
# • 데이터 : trash_bag.csv
#출력
#2.  BMI(Body Mass Index, 체질량 지수) 는 몸무게(kg)를 키(m)의 제곱으로 나누어 계산된다.
#BMI에 따른 비만도 분류는 다음과 같다.
# students 데이터셋은 각 학교의
# 학년별 총 전입학생, 총 전출학생, 전체학생수정보를 포함한다
#주어진 bmi 데이터셋에서 비만도가 정상에 속하는 인원수와 과체중에 속하는 인원수의  차이를 정수로 출력


print(df.head(5))
print(df['용도'].unique())
print(df['사용대상'].unique())
df_home_trash = df[(df['용도']=='음식물쓰레기')&(df['사용대상']=='가정용')]
print(df_home_trash.head())
result_df = df_home_trash[df_home_trash['2L 가격']!=0]
print(result_df.head())
result=result_df['2l가격'].mean()
print(int(result))