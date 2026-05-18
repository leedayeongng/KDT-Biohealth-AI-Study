import requests
url='https://stock.naver.com/api/polling/domestic/NXT/stock?itemCodes=047040%2C005930%2C010140%2C034020%2C022100%2C454910%2C018880%2C005380%2C200880%2C003490](https://stock.naver.com/api/polling/domestic/NXT/stock?itemCodes=047040%2C005930%2C010140%2C034020%2C022100%2C454910%2C018880%2C005380%2C200880%2C003490'
res=requests.get(url)
print(res.status_code)
print(res.text)
if res.status_code==200:
    print(res.json())