import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# ==============================================================================
# 🎮 [BalanceGame_Edu: - 콘텐츠 기반 필터링(Cosine Similarity)] 🎮
# ==============================================================================
# 구현 내용:
# 1. 사용자의 응답 데이터를 형태가 있는 벡터(Vector)로 변환하기 (Numpy)
# 2. 코사인 유사도(Cosine Similarity)를 통해 두 사람의 성향 차이 수치화하기
# 3. 모든 친구들과의 궁합을 계산하여 제일 잘 맞는 사람(Best) 찾기
# ==============================================================================
def make_user_profile(answer_list):
    """
    [Step 1] 사용자의 응답 데이터를 숫자 벡터로 변환
    - A 선택: 1 / B 선택: 0 으로 변환하여 계산 가능한 형태로 만듭니다.
    """
    # 1. 'A', 'B' 문자를 숫자 1과 0으로 바꿉니다.
    # (이 과정이 없으면 수학 계산이 불가능해서 0%만 나옵니다!)
    numeric_answers = [1 if a == 'A' else 0 for a in answer_list]

    # 2. 계산을 위해 numpy 배열로 만들고 모양을 맞춥니다.
    user_vector = np.array(numeric_answers).reshape(1, -1)

    return user_vector

def calculate_similarity(my_vec, friend_vec):
    """
    [Step 2] 두 사람의 프로파일 벡터가 주어졌을 때, 코사인 유사도(각도)를 계산합니다.
    - 완전히 똑같으면 1.0 (100%)
    - 완전히 반대면 -1.0 혹은 0.0 에 가까운 값이 나옵니다.
    """
    sim_matrix = cosine_similarity(my_vec, friend_vec)
    sim_score = sim_matrix[0][0]
    percent = round(sim_score * 100, 1)
    if percent < 0:
        percent = 0.0
    return percent


def find_best_and_worst_match(my_name, my_answers, all_friends_data):
    """
    [Step 3] DB에 들어있는 모든 친구들의 정보 목록을 돌면서, 
    나와 가장 잘 맞는 친구 1명(Best)과 안 맞는 친구 1명(Worst)을 뽑아냅니다.
    """
    match_results = []
    my_profile_vec = make_user_profile(my_answers)
    for friend in all_friends_data:
        friend_name = friend['name']
        friend_profile_vec = make_user_profile(friend['answers'])
        current_score = calculate_similarity(my_profile_vec, friend_profile_vec)
        match_results.append({'name': friend_name, 'score': current_score})
    print(f'--[{my_name}님 유사도 분석 결과]')
    for r in match_results:
        print(f'이름:{r["name"]} 유사도 :{r["score"]}')
    match_results.sort(key=lambda x: x['score'], reverse=True)

    best_match  = match_results[0]
    worst_match = match_results[-1]
    return best_match, worst_match
