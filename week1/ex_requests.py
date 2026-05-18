# import requests
#
# api_url = 'http://open.er-api.com/v6/latest/USD'
# res = requests.get(api_url)
# print(res)
# print(res.status_code) #응답토드 200 정상
# print(res.text)
# #json 파싱
# data=res.json()
# usd_to_krw=data['rates']['KRW']
# print(f'1달러 : {usd_to_krw}원')

# import requests
# api_url = 'http://open.er-api.com/v6/latest/USD'
# res=requests.get(api_url)
#
# data = res.json()
#
# rates = data['rates']
#
# for currency, rate in rates.items():
#     print(f'{currency}: {rate}')


print(res.text)
data=res.json()
usd_to_krw = data['rates']['KRW']
print(f'1달러:{usd_to_krw}원')
for k in data['rates']:
    print(f'k:{k}, v:{data['rates'][k]}')
print('='*50)
print('달러 환전!')
while True:
    msg=input('달러 -> 원화 달러를 입력하세요(종료:q)=')
 if msg=='q':
     break
 amount = float(msg) * used_to_krw
 print(f'{float(msg)} 달러는 원화로 {amount} 입니다.'