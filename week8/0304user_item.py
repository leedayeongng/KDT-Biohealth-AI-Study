import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

df_ratings = pd.read_csv('../datasets/recommend/ratings.csv')
df_movies = pd.read_csv('../datasets/recommend/movies.csv')

print(df_ratings)
df_ratings.drop('timestamp', axis=1, inplace=True)

user_item_rating=pd.merge(df_ratings, df_movies, on='movieId')
#사용자 아이템
user_matrix = user_item_rating.pivot_table('rating', index='userId', columns='title')
user_matrix.fillna(0, inplace=True)
print(user_matrix)
#비슷한 취향을 가진 유저
user_cf = cosine_similarity(user_matrix)
result_df = pd.DataFrame(data=user_cf, index=user_matrix.index, columns=user_matrix.index)
print(result_df.shape)
def get_user_movie_recommend(sim_user_id, target_user_id):
    """유사한 사용자가 남긴 평점이 높은 영화에서 타겟 사용자가 아직 시청하지 않음 영화"""
    sim_user_history = user_item_rating[user_item_rating['userId'] == sim_user_id]
    target_user_history = user_item_rating[user_item_rating['userId'] == target_user_id]
    #제외 연산 ~
    unseen_movies = sim_user_history[~sim_user_history['movieId'].isin(target_user_history['movieId'].values.tolist())]
    top_movie = unseen_movies.sort_values(by='rating', ascending=False)[:6]
    return top_movie['title'].values.tolist()[:1]

def recommend_for_target_user(target_id):
    """타겟유저와 유사한 고객상위 5명을 찾고 영화추천"""
    sorted_users = result_df[target_id].sort_values(ascending=False)[:6]
    sim_user_id = sorted_users.index.tolist()[1:]
    print(f'취향이 비슷한 유저:{sim_user_id}')
    data = []
    for sim_id in sim_user_id:
        recommended_items = get_user_movie_recommend(sim_id, target_id)
        data = data + recommended_items
    return set(data) #중복영화제거
target = 9
my_best = user_item_rating[user_item_rating['userId'] == target].sort_values(by='rating', ascending=False)[:5]
print(my_best[['movieId', 'title','rating']])
print(f'{target} 사용자 맞춤 추천')
movies = recommend_for_target_user(target)
for movie in movies:
    print(f'-{movie}')
