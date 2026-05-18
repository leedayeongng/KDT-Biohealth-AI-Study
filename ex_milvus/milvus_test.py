import os
import torch
from pymilvus import connections, utility
from PIL import Image
from transformers import CLIPProcessor, CLIPModel

# 1. Milvus 연결
try:
    connections.connect(alias="default", host="127.0.0.1", port="19530")
    print("✅ Milvus 연결 성공!")
except Exception as e:
    print(f"❌ Milvus 연결 실패: {e}")

# 2. 기존 컬렉션 확인
print("기존 컬렉션 목록:", utility.list_collections())

# 3. 모델 로드 (HuggingFace에서 다운로드)
print("⏳ 모델 로딩 중...")
model = CLIPModel.from_pretrained('openai/clip-vit-base-patch32', use_safetensors=True)
processor = CLIPProcessor.from_pretrained('openai/clip-vit-base-patch32', use_fast=True)

# 4. 이미지 처리 (경로 확인 필수!)
img_path = 'C:/dev/workspace.python/datasets/imageNet/dog1.jpg'

if os.path.exists(img_path):
    image = Image.open(img_path).convert('RGB')

    # 5. 벡터 추출 (Embedding)
    inputs = processor(images=image, return_tensors="pt")

    with torch.no_grad():
        # model.get_image_features를 호출하면 최종 벡터가 나옵니다.
        # 만약 객체가 반환된다면 그 안에서 진짜 데이터인 .pooler_output 등을 꺼내야 합니다.
        outputs = model.get_image_features(**inputs)

        # 💡 핵심 수정: 객체에서 텐서만 추출하기
        # 만약 outputs에 데이터가 직접 담겨있지 않다면 필드명을 통해 접근해야 합니다.
        if hasattr(outputs, "pooler_output"):
            features = outputs.pooler_output
        else:
            features = outputs  # 보통 get_image_features는 텐서를 직접 줍니다.

    print("🚀 이미지 분석 완료!")
    # features가 텐서이므로 이제 .shape과 .detach()가 작동합니다.
    print(f"추출된 벡터 모양(shape): {features.shape}")
    print(f"첫 5개 숫자 예시: {features[0][:5].tolist()}")