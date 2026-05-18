import pandas as pd
import math

lst = [10, 11, 11.2, 13, 15.5, 18, 19.8, 20, 31, 33, 39.5, 42]
s=pd.Series(lst)

# - 제1사분위수와 제3사분위수를 구하시오.
q1 = s.quantile(0.25)
q3 = s.quantile(0.75)
print('q1:', q1)
print('q3:', q3)
# - 제1사분위수와 제3사분위수의 차이의 절댓값을 구하시오.
diff = abs(q3-q1)
print('차이:',diff)
# - 그 값을 정수로 출력하시오.(소수점 내림)
result = math.floor(diff)
print('정수:',result)


import pandas as pd

df = pd.read_csv('https://raw.githubusercontent.com/YoungjinBD/dataset/main/facebook.csv')
print(df.head())
print(df.columns)
df.info()
#이 중 love 반응(num_loves)와 wow 반응(num_wows)을 매우 긍정적인 반응이라고 정의할 때,
# 전체 반응 수(num_reaction) 중 매우 긍정적인 반응 수가 차지하는 비율을 계산하시오.
df['ratio']= (df['num_loves'] + df['num_wows'])/df['num_reactions']
print(df['ratio'])

#그리고 그 비율이 0.4 보다 크고 0.5보다 작으면,  0.4<ratio<0.5
# 유형이 비디오에 해당하는 경우를 정수로 출력하시오. status_type =='video'
result = df[(df['ratio']>0.4) & (df['ratio']<0.5) & (df['status_type'] == 'video')]
print(len(result))

print(df['status_type'].unique())
pd.set_option('display.max_rows', None)
print(df.head())

#- **netflix 데이터셋은 넷플릭스에 등록된 컨텐츠의 메타 데이터이다.**
import pandas as pd
df = pd.read_csv('https://raw.githubusercontent.com/YoungjinBD/dataset/main/netflix.csv')
print(df.head())
print(df.info())


#     2018년 01월 넷플릭스에 등록된 컨텐츠 중에서
#     ’United Kingdom’이 단독 제작한 컨텐츠의 수를 정수로 출력하시오.
result_df = df[
    (df['date_added'].str.contains('January')) &
    (df['date_added'].str.contains('2018')) &
    (df['country'] == 'United Kingdom')
]
result_uk = result_df[result_df['country']=='united kingdom']
print(result_df.head(10))
print(len(result_df))

