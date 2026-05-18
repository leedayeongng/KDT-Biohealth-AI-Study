import time
import threading
def down(nm, sec):
    print(f'{nm} 다운 시작..')
    time.sleep(sec)
    print(f'{nm}완료! {sec} 초 소요')

start = time.time()
down('파일A', 3)
down('파일B', 2)
end = time.time()
print(f' 작업 종료 : 총{end - start:.1f}초')
print('2번째 작업!')
t1 = threading.Thread(target=down, args=('파일C', 5))
t2 = threading.Thread(target=down, args=('파일D', 2))
t1.start()#시키고 바로 다음으로 넘어감(Non-blocking)
t2.start()
t1.join() #기다림
print('==============================종료!!!')


