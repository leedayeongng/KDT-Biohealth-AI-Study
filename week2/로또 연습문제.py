# 함수명  : user_lotto
# input  : 0 ~ n
# output : 로또번호, 'x x 번호가 적용된 로또 번호' <-- message리턴
# 사용자가 입력한 번호를 포함시켜서 로또번호 생성
# 단 6개 이상이 들어오면 5개까지 포함시키고 1개 랜덤값
from week1.lotto마지막문제 import *
msg,data = user_lotto()
print(msg)
print(data)
msg,data=user_lotto(12,2)
print(msg)
print(data)
msg,data=user_lotto(1,2,3,4,5,6)
print(msg)
print(data)

