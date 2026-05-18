from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

#pip install eunjeon
from eunjeon import Mecab
reviews = [
"이 제품 정말 좋아요. 다음에도 구매의향 있습니다.",
"배송이 너무 늦어서 실망했습니다.",
"가격 대비 품질이 훌륭합니다.",
"설명과 똑같은 제품이 와서 만족합니다.",
"제품이 고장나서 AS를 받았습니다.",
"AS 처리 과정이 너무 번거로웠습니다.",
"추천하고 싶은 제품입니다.",
"포장이 꼼꼼해서 기분이 좋았습니다.",
"생각보다 품질이 별로라 아쉬웠습니다.",
"사용해보니 기능이 정말 편리합니다.",
"가격이 조금 비싸지만 성능은 만족스럽습니다.",
"설치 방법이 어려워서 처음엔 힘들었습니다."
]

#한국어 형태소 분석기
mecab = Mecab()
print(mecab.pos(reviews[1])) #pos 품사 태깅
print(mecab.nouns(reviews[1])) #nouns명사만 추출
# def fn_token(doc):
#     return mecab.nouns(doc)
def fn_token(doc):
    tokens = []
    pos_text = mecab.pos(doc)
    for word, pos in mecab.pos(doc):
        tokens.append(f'{word} {pos}')
    return tokens
model = TfidfVectorizer(tokenizer=fn_token
                        , stop_words=["이/JKS", "기/JKS","을/JKO","는/JK"])
tfidf = model.fit_transform(reviews)
while True:
    word = input("검색 단어:")
    q_tfidf = model.transform([word])
    cos_sim = cosine_similarity(q_tfidf, tfidf).flatten()
    idxs = cos_sim.argsort()[:-3:-1]
    for idx in idxs:
        print(reviews[idx])
