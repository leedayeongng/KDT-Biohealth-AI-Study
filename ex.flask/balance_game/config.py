import os

basedir = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.path.join(basedir, 'balance_game_edu.db')
SECRET_KEY = 'edu_balance_secret'

# 학생 실습용 고정 질문 5개 (카테고리 포함)
INITIAL_QUESTIONS = [
    ('초능력', 'SUPERPOWER', '평생 동안 투명인간으로 살기', '평생 동안 마음을 읽는 능력으로 살기'),
    ('음식', 'FOOD', '평생 치킨만 먹기', '평생 피자만 먹기'),
    ('시간', 'TIME', '과거로 돌아가 내 실수 한 개 고치기', '미래로 가서 내 미래의 모습 5분 동안 보기'),
    ('생활', 'LIFE', '여름에 롱패딩 입기', '겨울에 반팔 입기'),
    ('친구', 'FRIENDS', '친구가 1명인 대신 나를 위해 목숨도 바칠 수 있음', '친구가 100명인데 다들 나한테 1만원씩 빚지고 잠수탐'),
    ('여행', 'travel', '여름에 스노쿨링하기', '겨울에 스키타기')
]
