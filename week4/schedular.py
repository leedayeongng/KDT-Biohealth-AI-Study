#pip install apscheduler
import datetime #현재시간출력
from apscheduler.schedulers.blocking import BlockingScheduler
#메인 스레드를 차단하면서 반복 작업 실행 이걸 쓰면 프로그램이 종료되지 않고 계속 스케줄러가 돌아감



#interval :주기적으로
#cron : 워ㄴ하는 시간 패턴
#주기적으로(interval) 실행될 함수 밑 /실행될 때마다 "interval" + 현재 시각 출력
def fn_interval():
    print('interval')
    print(datetime.datetime.now())
def fn_cron():
    print('cron')
    print(datetime.datetime.now())
#cron 스케줄에 맞춰 실행될 함수,특정 시간/요일/날짜 패턴으로 반복  #실행될 때마다 "cron" + 현재 시각 출력

worker = BlockingScheduler() #BlockingScheduler 객체 생성
#worker.add_job(fn_interval, 'interval', seconds=10)
#worker.add_job(fn_interval, 'interval', minutes=1) #1분마다
worker.add_job(fn_interval, 'interval', hours=1) #1시간마다
#매월 1일 9시 10분
worker.add_job(fn_cron, 'cron', day='1', hour='09', minute='10')
#매일
worker.add_job(fn_cron, 'cron', hour='16', minute='13')
#월-금 24시
worker.add_job(fn_cron, 'cron', day_of_week='wed,fri',hour='14')
worker.start()
print('시작!')

#1시간마다 fn_interval 실행

#매월 1일 09:10, 매일 16:13, 수·금 14:00에 fn_cron 실행