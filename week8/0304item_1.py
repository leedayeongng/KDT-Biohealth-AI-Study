import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

df_ratings = pd.read_csv('../datasets/recommend/ratings.csv')
df_movies = pd.read_csv('../datasets/recommend/movies.csv')

print(df_ratings)
df_ratings.drop('timestamp', axis=1, inplace=True)
#영화 평점 정보 행렬
user_item_rating=pd.merge(df_ratings, df_movies, on='movieId')
movie_matrix = user_item_rating.pivot_table('rating', index='title', columns='userId')
print(movie_matrix.shape)
# 처리하기 전 NaN data를 0으로 바꾸기
movie_matrix.fillna(0, inplace=True)
item_cf = cosine_similarity(movie_matrix)
result_df = pd.DataFrame(data=item_cf, index=movie_matrix.index, columns=movie_matrix.index)
print(result_df.head(5))
print(result_df.shape)
def get_ite_based(title):
    top_movies = result_df[title].sort_values(ascending=False)[:10]
    return top_movies

while True:
    movie = input("좋아하는 영화 이름을 정확하게 입력하세요:")
    try:
        print("추첨 결과")
        print(get_ite_based(movie))
    except Exception as e:
        print("없는 영화 이름잆니다.")





