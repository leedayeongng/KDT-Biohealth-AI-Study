# import random  #랜덤숫자
#
# def fn_lotto(cnt):  #fn_lotto이름의 함수를 만들고 cnt(몇개번호를 뽑을지 입력값)
#     arr = random.sample(range(1,46), cnt) #1-45 숫자중에서 중복없이 cnt개 뽑음
#     arr.sort()
#     return arr
#
# def user_lotto(*user_numbers):   #user lotto 함수정의, user number:몇개번호입력해도 모두 받을수있따
#     selected_numbers = list(user_numbers[:5]) #사용자입력한번호최대5까지, 6개이상입력해도 5개
#     whale len(selected_numbers) < 6: #번호가 6개될때까지 반복
#         num = random.randint(1, 45)  # 1-45까지 반복
#         if num not in selected_numbers:    #중복방지
#             selected_numbers.append(num)  #랜덤번호추가
#     selected_numbers.sort()
#     if user_numbers:
#         msg = " ".join(map(str, user_numbers[:5])) + " 번호가 적용된 로또 번호"
#     else:
#         msg = "랜덤으로 생성된 로또 번호"
#     return msg, selected_numbers


def user_lotto(*args):
    user_num = list(args[:5])
    msg=','.join(map(str,user_num)) + "번호가 적용된 로또"
    lotto = set(user_num)
    while len(lotto)<6:
            lotto.add(random.randint(1,45))
    return msg, sorted(list(lotto))
