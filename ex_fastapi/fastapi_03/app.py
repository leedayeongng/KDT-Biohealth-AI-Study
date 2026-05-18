import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import List
import googleapiclient.discovery  # pip install google-api-python-client
import os
from analysis_utils import analyze_sentiment, run_ner, fn_wordcloud
import re


# youtube
API_KEY = 'AIzaSyAhAr34GB4lRyBHkwsyX7aQHWdWostvgQc'
youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey=API_KEY)
app = FastAPI(title="Youtube Comment Analyzer")
STATIC_DIR = os.path.join(os.getcwd(), "static")
app.mount('/static', StaticFiles(directory=STATIC_DIR), name='static')
templates = Jinja2Templates(directory='templates')

class URLRequest(BaseModel):
    url: str

#230313 참고
def get_video_comments(video_id):
    comments = []
    results = youtube.commentThreads().list(part='snippet', videoId=video_id, textFormat='plainText').execute()   #<- 이미 명시되어 있는 방법
    title = youtube.videos().list(part='snippet', id=video_id).execute()['items'][0]['snippet']['title']
    # print(title)
    title = re.sub('[^a-zA-Z0-9가-힣]', '', title)
    #print(results)
    while results:
        for item in results['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)
        if 'nextPageToken' in results:
            results = youtube.commentThreads().list(part='snippet', videoId=video_id, textFormat='plainText', pageToken=results['nextPageToken']).execute()
        else:
            break
    return comments, title

# videoId 추출하는 함수 임의로 만들기 (이번을 위해 그냥 만듬)
def extract_video_id(url):
    video_id = url.split("v=")[1].split('&')[0] # 주소창에 &가 들어가 있으면 넣고, 아니면 지우기
    return video_id

@app.get("/", response_class=HTMLResponse)
async def read_root(request:Request):
    return templates.TemplateResponse(name="index.html", context={}, request=request)
from collections import Counter

@app.post("/analyze")
async def analyze_youtube(request:URLRequest):
    video_id = extract_video_id(request.url)
    if not video_id :
        raise HTTPException(status_code=400, detail="invalid youtube url")
    comments, title = get_video_comments(video_id)
    sentiment_res = analyze_sentiment(comments, max_count=100)

    # NBR 분석
    all_entities = []
    for c in sentiment_res['sample_comments']:
        all_entities.extend(run_ner(c))
    top_ner = [item for item, count in Counter(all_entities).most_common(10)]

    #워드클라우스 생성
    wc_url = fn_wordcloud(sentiment_res['valid_comments'], video_id, STATIC_DIR)

    return {"title" : title,
            "top_entities" : top_ner,
            "wordcloud_url" : wc_url,
            "video_id" : video_id,
            "sentiment" : {
                "positive" : sentiment_res["positive"],
                "negative" : sentiment_res["negative"],
                "total" : sentiment_res["total"]
                },
            "comments_count" : len(sentiment_res["valid_comments"])
            }

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)   # <- 127.0.0.1 = my localhost