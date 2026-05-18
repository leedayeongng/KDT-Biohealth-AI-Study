print("프로그램 시작")
try:
    val = int("abc")
    result = 10 / 0
except ValueError as e:
    print("숫자가 아니군")
except ZeroDivisionError as e:
    print("영을 왜!?")
except Exception as e:
    print(str(e))
else:
    print("정상처리")
finally:
    print("마지막에 무조건 처리됨.")

print("프로그램 종료")