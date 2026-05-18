
#pip install fastapi
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict
#html,css,js같은 정적파일을 호스팅하기위한 모듈
from fastapi.staticfiles import StaticFiles
#루트 경로로 오면 특정 url로 보내기위한 모듈
from fastapi.responses import RedirectResponse
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')

app = FastAPI(
    title="FastAPI REST API",
    description="""
        /docs (swagger UI)테스트 방법
        1.브라우저에서 http://127.0.0.1:8000/docs 로 접속
    """,
    version="1.0.0",
)
#STATIC 이라는 URL주소로 요청이 오면 폴더안에 있는 파일을 읽어서 그대로 연결
app.mount('/static', StaticFiles(directory=STATIC_DIR), name='static')
@app.get("/")
def read_root():
    return RedirectResponse(url="/static/index.html")


#pydantic 데이터 모델 정의
#이 클래스는 / docs 페이지 하다느이 schemas 영역에 모델 구조로 자동으로 문서화됨
class Item(BaseModel):
    id : int = Field(..., description="아이템 고유 ID번호",example=1)
    name : str = Field(..., description="아이템의 이름", example="마우스")
    description : str = Field(None, description="아이템 설명(선택사항)", example="좋은 무선 마우스")
    price : float = Field(..., description="아이템 가격", example=10000.0)

# 예제
db :Dict [int, Item] = {}
#Read All(GET)
@app.get("/items/", response_model=List[Item], summary="모든 아이템 조회")
def get_all_items():
    return list(db.values())
#read specific item(get)
@app.get("/items/{item_id}",response_model=Item,summary="특정아이템조회")
def get_item(item_id:int):
    if item_id in db:
        raise HTTPException(status_code=404, detail='해당 아이템을 찾을 수 없습니다.')
    return db[item_id]
#update(put)
@app.put("/items/{item_id}", response_model=Item, summary="기존 아이템 수정")
def update_item(item_id: int, item: Item):
    if item_id not in db:
        raise HTTPException(status_code=404, detail='수정할 아이템을 찾을 수 없습니다.')

    if item_id != item.id:
        raise HTTPException(status_code=400, detail='경로의 id와 전달 본문의 id가 일치해야합니다.')

    db[item_id] = item
    return item
#delete(delete)
@app.delete("/itmes/{item_id}",status_code=204,summary="특정아이템삭제")
def delete_item(item_id: int):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="삭제할 아이템을 찾을 수 없습니다.")
    del db[item_id]



#create (post)
@app.post("/items/",response_model=Item, status_code=201, summary='새로운 아이템 생성')
def create_item(item: Item):
    if item.id in db:
        raise HTTPException(status_code=400, detail="이미 존재하는 ID 입니다.")
    db[item.id] = item
    return item


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8080, reload=True)    #pip install fastapi
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict
#html,css,js같은 정적파일을 호스팅하기위한 모듈
from fastapi.staticfiles import StaticFiles
#루트 경로로 오면 특정 url로 보내기위한 모듈
from fastapi.responses import RedirectResponse
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, 'static')

app = FastAPI(
    title="FastAPI REST API 예제",
    description="""...""",
    version="1.0.0",
)
#STATIC 이라는 URL주소로 요청이 오면 폴더안에 있는 파일을 읽어서 그대로 연결
app.mount('/static', StaticFiles(directory=STATIC_DIR), name='static')
@app.get("/")
def read_root():
    return RedirectResponse(url="/static/index.html")


#pydantic 데이터 모델 정의
#이 클래스는 / docs 페이지 하다느이 schemas 영역에 모델 구조로 자동으로 문서화됨
class Item(BaseModel):
    id : int = Field(..., description="아이템 고유 ID번호",example=1)
    name : str = Field(..., description="아이템의 이름", example="마우스")
    description : str = Field(None, description="아이템 설명(선택사항)", example="좋은 무선 마우스")
    price : float = Field(..., description="아이템 가격", example=10000.0)

# 예제
db :Dict [int, Item] = {}
#Read All(GET)
@app.get("/items/", response_model=List[Item], summary="모든 아이템 조회")
def get_all_items():
    return list(db.values())
#read specific item(get)
@app.get("/items/{item_id}",response_model=Item,summary="특정아이템조회")
def get_item(item_id:int):
    if item_id in db:
        raise HTTPException(status_code=404, detail='해당 아이템을 찾을 수 없습니다.')
    return db[item_id]
#update(put)
@app.put("/items/{item_id}", response_model=Item, summary="기존 아이템 수정")
def update_item(item_id: int, item: Item):
    if item_id not in db:
        raise HTTPException(status_code=404, detail='수정할 아이템을 찾을 수 없습니다.')

    if item_id != item.id:
        raise HTTPException(status_code=400, detail='경로의 id와 전달 본문의 id가 일치해야합니다.')

    db[item_id] = item
    return item
#delete(delete)
@app.delete("/itmes/{item_id}",status_code=204,summary="특정아이템삭제")
def delete_item(item_id: int):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="삭제할 아이템을 찾을 수 없습니다.")
    del db[item_id]



#create (post)
@app.post("/items/",response_model=Item, status_code=201, summary='새로운 아이템 생성')
def create_item(item: Item):
    if item.id in db:
        raise HTTPException(status_code=400, detail="이미 존재하는 ID 입니다.")
    db[item.id] = item
    return item


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="127.0.0.1", port=8080, reload=True)