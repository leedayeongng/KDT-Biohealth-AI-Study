import random

print('=' * 20)
print('업다운 게임!')

com_num = random.randint(1, 10)

cnt = 3
while cnt > 0:
    user_num=int(input('1 ~ 10 사이의 정수를 입력하세요!'))
    if com_num == user_num:
        print('정답 입니다!')
        break
    elif user_num < com_num:
        print('업')
    else:
        print('다운')
    cnt-=1
    if cnt > 0:
        print(f'남은 기회:{cnt}')
if cnt == 0:
    print(f'기회를 모두 사용하셨습니다.. 정답은 {com_num}입니다.')