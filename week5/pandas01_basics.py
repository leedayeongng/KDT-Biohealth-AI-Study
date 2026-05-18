# pip  install pandas
import pandas as pd

#1.Series (열) Dataframe(행/열)
data_list = [10, 20, 30, 40, 50] #index 디폴트 0~
series = pd.Series(data_list, index=['a', 'b', 'c', 'd', 'e'])
print('\n series')
print(series)
print(f'인덱스 "b" 값: {series["b"]}')
data_dict = {
    '이름' : ['철수','동수', '펭수', '길수']
   ,'나이' : [25, 30, 22, 28]
   ,'직업' : ['개발자', '디자이너', '학생', '기획']
   ,'점수' : [85, 90, 78, 92]
}
df = pd.DataFrame(data_dict)
print('\n dataframe 생성')
print(df)
print(df.head(2))
print(df.tail(2))
print(" 데이터 정보 ")
print(df.info())
print(" 열 선택")
names = df['이름']
print('\n 이름 열 선택')
print(names)
print("여러 열 선택")
subset = df[['이름', '점수']]
print(subset)
#loc : 이름(link)으로
#iloc : 번호(index)로 선택
print('loc[1] : 1번 인덱스(행)데이터')
print(df.loc[1])
print('\niloc[0, 1]: 0번 행, 1번 열의 값')
print(df.iloc[0, 1])
print("필터링 : 나이 25세 여성")
adults = df[df['나이']>=25]
print(adults)
#점수가 90 이상인 사람의 dataframe 출력
high = df[df['점수']>=90]['이름']
print(high)
#3번 인덱스의 이름만 출력하시오
print("======")
print(df.loc[3, '이름'])
print(high.loc[3])
print(high.iloc[1])

#df series 반환
for idx, row in df.iterrows():
    print(idx, row['이름'], row['점수'])
# namedtuple 반환
for row in df.itertuples():
    print(row.이름)
#value만(가장빠름)
for v in df['이름'].values:
    print(v)

df['age_plus'] = df['나이'] + 1
df['age_squared'] = df['나이'] * df['나이']
print(df.head())
#다양한 내장함수
total = df['age_plus'].sum()
median = df['age_plus'].quantile(0.5)
print('total: ', total)
print('median: ', median)