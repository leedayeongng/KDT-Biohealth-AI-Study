import torch
from pymilvus import connections, FieldSchema, CollectionSchema, DataType, Collection, utility

# 1. 연결 (사용자님 IP로 설정)
connections.connect(host="192.168.233.4", port="19530")

# 2. 컬렉션 설정 (테이블 설계)
COLLECTION_NAME = "image_search_collection"
DIMENSION = 512

fields = [
    FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
    FieldSchema(name="vector", dtype=DataType.FLOAT_VECTOR, dim=DIMENSION),
    FieldSchema(name="file_path", dtype=DataType.VARCHAR, max_length=500)
]

schema = CollectionSchema(fields, "이미지 벡터 저장소")

# 3. 컬렉션 생성
if utility.has_collection(COLLECTION_NAME):
    utility.drop_collection(COLLECTION_NAME) # 깨끗하게 새로 만들기 위해 기존꺼 삭제

collection = Collection(COLLECTION_NAME, schema)

# 4. 가짜 데이터(랜덤 벡터) 또는 아까 뽑은 features 넣기
# 지금은 테스트를 위해 랜덤 숫자를 넣어볼게요.
import numpy as np
dummy_vector = np.random.random((1, 512)).tolist()
dummy_path = ["C:/dev/test_image.jpg"]

collection.insert([dummy_vector, dummy_path])
collection.flush() # 물리적 저장

print(f"✅ '{COLLECTION_NAME}' 생성 및 데이터 삽입 완료!")