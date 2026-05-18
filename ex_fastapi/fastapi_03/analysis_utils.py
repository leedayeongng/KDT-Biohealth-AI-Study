# pip install transformers torch
# pip install protobuf==3.20.*
from transformers import pipeline, BertTokenizer
import os
import re
from collections import Counter
from typing import List, Dict
from typing import List, Dict
from kiwipiepy import Kiwi
from collections import Counter
from wordcloud import WordCloud

analyzer = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
kiwi = Kiwi()
def run_ner(text:str) -> List[str]:
    """ 한글 명사 추출 """
    entities = []
    try:
        result = kiwi.analyze(text)[0][0]
        for token in result:
            if token.tag in ["NNP", "NNG"]:
                entities.append(token.form)
    except:
        pass
    return entities

def fn_wordcloud(comments:List[str], video_id:str, static_dir:str) -> str:
    comment_text = ' '.join(comments)
    word_cnt = Counter(comment_text.split())
    cloud = WordCloud(width=600, height=400
                      , font_path = 'c:/Windows/Fonts/malgun.ttf'
                      , background_color='white').generate_from_frequencies(word_cnt)
    filename = f'wc_{video_id}.png'
    filepath = os.path.join(static_dir, filename)
    cloud.to_file(filepath)
    return f'/static/{filename}'

# typing : 변수 타입 명시
def analyze_sentiment(comments:List[str], max_count:int =50) -> Dict:  # -> 타입을 명시할 때
    """ 댓글 리스트에 대한 감성 분석 """
    valid_comments = []
    for c in comments:
        tokens = tokenizer.tokenize(c)
        if len(tokens) <= 512 :
            valid_comments.append(c)
    sample_comments = valid_comments[:max_count]
    pos_count = 0
    neg_count = 0
    for c in sample_comments:
        res = analyzer(c)[0]
        print(res)
        if 'NEGATIVE' in res['label']:
            neg_count += 1
        elif 'POSITIVE' in res['label']:
            pos_count += 1
    return {'positive' : pos_count
        , 'negative' : neg_count
        , 'total':len(sample_comments)
        , 'valid_comments': valid_comments
        , 'sample_comments' : sample_comments}
# print(analyze_sentiment(['너무 좋습니다. ','응원 합니다.']))
