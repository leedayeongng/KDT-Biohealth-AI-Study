import requests
#requests 라이브러리 불러오기
#인터넷(API)에 요청(request) 보내고 응답(response) 받기 위해 사용

market = "KRW-BTC"
url = f"https://api.upbit.com/v1/ticker?markets={market}" #f-string, 변수값을 바로 넣음
response = requests.get(url) #API 호출
print(response.json())#응답(JSON)**을 파이썬 객체로 변환해서 출력

#“KRW-BTC(비트코인 원화 마켓)의 실시간 가격 정보를 Upbit API에서 가져와서 출력하는 코드”