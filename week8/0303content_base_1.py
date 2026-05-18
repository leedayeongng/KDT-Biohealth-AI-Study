import pandas as pd
import numpy as np


def cos_sim(x,y):
    return np.dot(x,y)/(np.linalg.norm(x)*np.linalg.norm(y))

df = pd.read_excel('../datasets/recommend/items_user.xlsx', sheet_name='item_table')
history_df = pd.read_excel('../datasets/recommend/items_user.xlsx', sheet_name='purchase_history')

print(df.head())
print(history_df.head())

df_enc=pd.get_dummies(df, columns=['color'])
print(df_enc)
df_enc['light'] = df['weight'] <= 200
df_enc['heavy'] = df['weight'] > 200
df_enc['small'] = df['item_size'] <=95
df_enc['big'] = df['item_size'] > 95
df_enc['low'] = df['price'] <=50000
df_enc['medium'] = (df['price'] > 50000) & (df['price'] <=500000)
df_enc['high'] = (df['price'] > 50000)
print(df_enc.head())
item_profile = df_enc.drop(columns=['item_id', 'weight', 'item_size', 'price'])
item_profile = item_profile.astype(int)
item_profile.index = df['item_id']
print(item_profile.head())
# 유지 프로파일 생성
user_items = history_df[history_df['mem_id'] == "user1"]["item_id"]
user_profile = item_profile.loc[user_items].mean()
print(user_profile.round(2))

#아이템과 유사도계산
unseen_items = item_profile.drop(index=user_items)
similarities = unseen_items.apply(lambda x: cos_sim(user_profile,x), axis = 1)
similarities = similarities.round(3)
print(similarities)
#유사도 기준 추천
recommend = similarities.sort_values(ascending = False).head(3)
print(recommend)
