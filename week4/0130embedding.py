#pip install gensim
import requests #웹에서 파일(텍스트) 다운로드
import re #정규표현식(문자 정리용)
from gensim.models.word2vec import Word2Vec #단어를 벡터로 학습하는 모델 (자연어 처리 핵심
res = requests.get('https://www.gutenberg.org/files/2591/2591-0.txt') # Grimm 형제 동화집 텍스트를 가져옴
grimm = res.text[2801:530661]
print(grimm)
grimm = re.sub(r'[^a-zA-Z\.]', ' ', grimm) #알파벳과 .만 남기고 전부 공백으로 치환
sentence = grimm.split('. ') #. 기준으로 문장 나누기
data = [s.split() for s in sentence]
print(data)
#Word2Vec 모델 학습
embedding_model = Word2Vec(data, sg=1 # .load 제거  중심 단어 → 주변 단어 예측
                                    , vector_size=100
                                    , window=3 #앞뒤 3단어까지 문맥으로 봄
                                    , min_count=3 # 3번 이상 등장한 단어만 사용
                                    , workers=4#CPU 4개 사용 (속도 ↑)
                                )
print(embedding_model.wv.most_similar(positive=['king','woman'], negative=['man'])) # 괄호 닫기
vocab = list(embedding_model.wv.key_to_index.keys()) #학습된 모든 단어 목록
while True:
    mode = input('\n 선택(1:유사어, 2:반대어, q:종료):')
    if mode == 'q':
        break
    word = input("기준 단어를 입력:")
    if word not in vocab:
        print("단어 없음 X")
        continue
    if mode == '1':
        print(f"{word}와 유사한 단어:")
        for w, score in embedding_model.wv.most_similar(positive=[word]):
            print(f'{w}: {score:2f}')     #유사어
    elif mode =='2':
        print(f'{word}와 반대의미:')
        for w, score in embedding_model.wv.most_similar(negative=[word]):
            print(f'{w}: {score:2f}')  #반의어

#Grimm 동화 텍스트로 Word2Vec을 학습하여 단어의 의미를 벡터로 표현
#단어 유사도 및 의미 관계를 탐색하는 프로그램이다.