from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from gensim.downloader import BASE_DIR
from pydantic import BaseModel
from typing import List, Optional
import psycopg2
from psycopg2.extras import DictCursor
from googletrans import Translator
import asyncio
import os
import re
import uvicorn

app = FastAPI(title = 'MIMIC-IV Code Dictionary')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')
app.mount('/static', StaticFiles(directory=STATIC_DIR), name='static')
translator = Translator()
DB_CONFIG = {
    "dbname":"mimic4_data", "user":"bio4", "password":"bio4", "host":"localhost", "port":5432
}
#번역저장
translator_cache = {}
class CodeResult(BaseModel):
    code_type : str
    code : str
    english : str
    korean_name : str

@app.get('/')
def read_root():
    return RedirectResponse(url='/static/index.html')

# db접속
def get_db_conn():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f'DB connection error:{e}')
        return None
# 번역처리 (비동기함수)
async def translate_text(text:str) -> str:
    if not text:
        return ""
    if text in translator_cache:
        return translator_cache[text]
    try:
        result = translator.translate(text, src='en', dest='ko')
        translated = getattr(result, 'text', '')
        translator_cache[text] = translated
        return translated
    except Exception as e:
        print(f'translate error:{e}')
        return "[번역실패]"
#사용자 요청 처리
@app.get('/api/search', response_model = List[CodeResult])
async def search_codes(q:str = Query(..., min_length=2, description='search keyword')):
    # 1. 한국어가 포함된 검색어 체크
    if bool(re.search(r'[가-힣]', q)):
        try:
            ko_to_en = translator.translate(q, src='ko', dest='en')
            q_db = getattr(ko_to_en, 'text', q)
            print(f'input:{q}, trans:{q_db}')
        except Exception as e:
            print(f'query trans error : {e}')
            q_db = q

    # 2. db조회
    conn = get_db_conn()
    search_term = f'%{q_db.lower()}%%'
    results = []
    try:
        with conn.cursor(cursor_factory=DictCursor) as cur:
            query_items = """
                select itemid, label from mimiciv_icu.d_items di 
                where lower(di.label) like %s or cast(di.itemid as text) like %s
                limit 15;
            """
            cur.execute(query_items, (search_term, search_term))
            for row  in cur.fetchall():
                results.append({
                    "type":"측정 항복(Item)",
                    "code":str(row['itemid']),
                    "env":row['label']
                })
            # diagnosis
            query_diag = """
                select icd_code, long_title
                from mimiciv_hosp.d_icd_diagnoses did
                where lower(did.long_title) like %s or did.icd_code like %s limit 15;
            """
            cur.execute(query_diag, (search_term, search_term))
            for row in cur.fetchall():
                results.append({
                    "type":"ICD진단", "code":row['icd_code'], "env":row['long_title']
                })
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=f'database query error:{e}') #문제가 생기면 어디에서 문제가 생겼는지
    finally:
        if conn:
            conn.close()
    # 3. 번역
    final_results= []
    # 여러 항목의 번역 병렬 처리
    async def process_item(item):
        korean_desc = await translate_text(item['env'])
        return CodeResult(
            code_type=item['type'],
            code=item['code'],
            english=item['env'],
            korean_name=korean_desc
        )
    tasks = [process_item(item) for item in results]
    final_results = await asyncio.gather(*tasks)
    return final_results


# 사용자 요청 처리
if __name__ == '__main__':
    uvicorn.run('app:app', host='127.0.0.1', port=8080, reload=True)

