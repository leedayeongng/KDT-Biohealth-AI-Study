import random
from collections import Counter

def coin_flip():
    if random.random()<0.5:
        return "head"
    else:
        return "tail"
    #동전던지기 횟수
n = 100
result = [coin_flip() for _ in range(n)]
cnt = Counter(result)
print("동전던지기결과")
print(cnt)
