
import random
print("=" * 50)
print("*로또 번호 생성기*")
# 1~45 중복되지 않은 6개의 숫자를
# 사용자의 입력 수량만큼 생성!
# 테스트 후 exe파일로 배포!




cnt = int(input("생성 수량?"))
for i in range(cnt):
    user_lotto = set()
    while len(user_lotto)<6:
        number = random.randint(1,45)
        user_lotto.add(number)
        print(f'행운의 로또 번호! {i+1}:{user_lotto}')
    print("="*50)
input("Good Luck")

