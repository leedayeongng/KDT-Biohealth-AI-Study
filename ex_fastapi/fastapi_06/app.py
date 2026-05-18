#pip install pyttsx3
import tempfile
import pyttsx3
from fastapi import FastAPI, Query
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os

from starlette.responses import RedirectResponse

app = FastAPI()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_PATH = os.path.join(BASE_DIR, 'static')
app.mount('/static', StaticFiles(directory=STATIC_PATH), name='static')
engine = pyttsx3.init()
@app.get('/')
def read_root():
    return RedirectResponse(url='/static/index.html')
@app.get('/tts')
def tts(text:str=Query(...)):
    engine=pyttsx3.init()
    #음성파일생성(임시저장)
    #with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as f:
    #        filename = f.name
    filename ='test.wav'
        #텍스트를 음성파일로
    engine.save_to_file('text', filename)
    #변환작업기다림
    engine.runAndWait()
    #생성된 팡리을 스트리밍 방식으로 전달
    def iterfile():
        with open(filename,'rb') as f:
                yield from f #파일 내용을 조각내어 반환
    return StreamingResponse(iterfile(),media_type='audio/wav')
if __name__ == '__main__':
    uvicorn.run('app:app',host='0.0.0.0',port=8080,reload=True)

