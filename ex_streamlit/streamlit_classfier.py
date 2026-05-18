import streamlit as st
import torch
import torchvision.models as models
from torchvision import transforms
from PIL import Image
import urllib.request
import os

st.set_page_config(page_title="AI Vision", layout="centered")
st.title("이미지분류기")
st.markdown("""**imagetNet dataset 학습모델**
""")
@st.cache_resource
def load_pytorch_model():
    #진행률표시
    with st.spinner("최종 1회 ai 모델 다운로드..."):
        try:
            from torchvision.models import ResNet18_Weights
            model = models.resnet18(weights=ResNet18_Weights.IMAGENET1K_V1)
        except:
            model = models.resnet18(pretrained=True)
        model.eval()
        url = "https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt"
        try:
            res= urllib.request.urlopen(url)
            classes = [line.decode("utf-8").strip() for line in res.readlines()]
        except Exception:
            classes = [f'class #{i}' for i in range(1000)]
        return model, classes
models, imagenet_classes = load_pytorch_model()
#이미지 분류 함수 정의
def get_prediction(image, model, classes):
    transform = transforms.Compose([
        transforms.Resize(256), transforms.CenterCrop(224), transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    tensor = transform(image).unsqueeze(0)
    with torch.no_grad():
        outputs = model(tensor)
    prob = torch.nn.functional.softmax(outputs[0], dim=0)
    top_prob, top_catid = torch.topk(prob, 1)
    return classes[top_catid.item()], top_prob.item() * 100
# 화면 UI
st.divider()
st.subheader("이미지를 돌려주세요!")
uploaded_file = st.file_uploader("이미지 파일 선택(PNG,JPT)",type=["png","jpg","jpeg"])
if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image,caption="업로드된 이미지",use_column_width=True)
    #분석버튼
    if st.button("분석 시작!",use_container_width=True):
        with st.spinner("이미지 분석중..."):
            class_name, confidence = get_prediction(image, models, imagenet_classes)
            st.success(f"분석완료! 이 사진은 **{class_name.upper()}** 같습니다.")
            st.info(f'AI :{confidence:.2f}%**')

            # cd ex_streamlit
            # streamlit run 0325_streamlit_item.py