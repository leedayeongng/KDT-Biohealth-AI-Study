#pip install pymilvus
from pymilvus import connections, Connections, utility
from PIL import Image
from pymilvus import connections
from transformers import CLIPProcessor, CLIPModel
import torch

connections.connect(
    alias="default",
    host="127.0.0.1",
    port="19530"
)

print("connected!")

# connections.connect('default'
#                      , host='127.0.0.1'   # ← 이걸로 바꿔
#                      ,port='19530'
#                      ,user='user10'
#                      ,password='1234')
# print('연결 완료')


collection_list = utility.list_collections()
for nm in collection_list:
    print(nm)

# utility.update_password('user10','1234','123456')

from sentence_transformers import SentenceTransformer
from transformers import CLIPProcessor, CLIPModel
#pip install -U sentence_transformers
#model = SentenceTransformer('all-MiniLM-L6-v2')
#raw_embedding = model.encode(["Milvus에 저장할 샘플문장^^"])
#print(raw_embedding)
model = CLIPModel.from_pretrained('openai/clip-vit-base-patch32',use_safetensors=True)
processor = CLIPProcessor.from_pretrained('openai/clip-vit-base-patch32', use_safetensors=True)
image = Image.open('C:/dev/datasets/imageNet/dog1.jpg').convert('RGB')
inputs = processor(images=image, return_tensors="pt")
features = model.get_image_features(**inputs)
print(features.shape)
#model = SentenceTransformer('all-MiniLM-L6-v2')
# raw_embedding=model.encode(["Milvus에 저장할 샘플 문장^^"])
# print(raw_embedding)

