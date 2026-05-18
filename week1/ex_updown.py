#ctrl+shift+p(검색창)
#python : inter 인터프리터설정
import random
print('='*20)
print('업다운 게임!')
com_num=random.randint(1,10) #1-10 정수 랜덤값
#기회는 단 3번
#사용자 입력을 받아 같으면 '정답!'틀리면 없 or 다운 을 출력
#3번의 기회에 못맞추면 기회를 모두 사용하셨습니다. 정답은 x입니다 출력

import random

print('=' * 20)
print('업다운 게임!')

com_num = random.randint(1, 10)
chance = 3

for i in range(chance):
    user = int(input(f'{i+1}번째 시도 - 숫자를 입력하세요: '))

    if user == com_num:
        print('정답!')
        break
    elif user < com_num:
        print('업')
    else:
        print('다운')
else:
    print(f'기회를 모두 사용하셨습니다. 정답은 {com_num}입니다.')
