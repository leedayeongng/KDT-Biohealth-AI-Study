import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

songs = pd.read_csv('../datasets/recommend/korean_music.csv')
users = pd.read_csv('../datasets/recommend/users.csv')

songs['idx'] = songs.index
songs['mood'] = songs['mood'].fillna('').apply(lambda x:x.split(','))
songs['instrument'] = songs['instrument'].fillna('').apply(lambda x:x.split(','))

print(songs.head())
mood_dummies = pd.get_dummies(songs.explode('mood')[['idx', 'mood']]).groupby('idx').max()
instr_dummies = pd.get_dummies(songs.explode('instrument')[['idx', 'instrument']]).groupby('idx').max()
other_dummies = pd.get_dummies(songs[['genre', 'tempo','vocal','year']])
meta = songs[['song_id', 'title']]
song_vector = pd.concat([meta, other_dummies, mood_dummies, instr_dummies], axis=1)
song_vector = song_vector.set_index('song_id')
print(song_vector)
print(song_vector.shape)
user_id = 'user1'
#유자가 좋아하는곡
user_row = users[users['user_id'] == user_id]
liked_songs = user_row.iloc[0]['liked_songs'].split(',')
# print(liked_vectors)
#유저 프로파일 = 백터평균
liked_vectors = song_vector.loc[liked_songs].drop(columns='title')
user_vec = liked_vectors.mean().values.reshape(1, -1)
print(user_vec)
#비교대상백터(미청취곡)
candidate_df = song_vector.drop(index=liked_songs)
candidate_vec = candidate_df.drop(columns=['title']).values
#코사인유사도계산
sims = cosine_similarity(user_vec, candidate_vec).flatten() #[[]] ->[]
candidate_df['similarity'] = sims
#상위 5곡
top5 = candidate_df.sort_values('similarity', ascending=False).head(5)
print(top5[['title', 'similarity']])
