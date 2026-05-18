import pandas as pd
#데이터 전처리
#누락된 값, 중복, 이상한 문자 등 ..을 깨끗하게 만드는 과정

data = {
    '이름': ['철수', '영희', '민수', '철수', '지수', '동현'],
    '나이': ['25', '30', None, '25', '28', '35'],
    '성별': ['남', '여', '남', '남', '남', None],
    '점수': [85, 90, 78, 85, None, 88]
}

df = pd.DataFrame(data)

print('원본')
print(df)
print(df.info())
print(f'결측치 수:\n{df.isnull().sum()}')
df_dropped = df.dropna() #결측치 행 삭제
print(df_dropped)
#결측치 채우기
df_filled = df.copy()
df_filled['점수'] = df_filled['점수'].fillna(0) #0으로 채움
print(df_filled)
print(f'중복된 행의 수:{df.duplicated().sum()}')
df_unique = df.drop_duplicates() #중복 제거
print(df_unique)
#나이 컬럼 문자열 or none --> int로
df_clean = df_unique.copy()
df_clean['나이'] = df_clean['나이'].fillna(20)
df_clean['나이'] = df_clean['나이'].astype(int)
print(df_clean.info())

def get_age_group(age):
    if age >= 30:
        return '30대 여성'
    elif age >= 20:
        return '20대'
    else:
        return '10대 이하'
df_clean['연령대'] = df_clean['나이'].apply(get_age_group)#함수적용
print(df_clean)