from flask import Flask, render_template, request, jsonify #웹사이트
import cv2 # 사진처리
import numpy as np #배열계산
import os #파일경로
import base64  #사진을문자로

app = Flask(__name__)  #웹서버 만들겠다!

#현재파일 디렉토리 경로, 파이썬파일위치찾기
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

#이미지 경로, imagenet 폴더연결
IMAGE_DIR = os.path.join(SCRIPT_DIR, 'imageNet')

#메인페이지 첫화면, httP://127~ 접속하면실행, imagenet폴더안사진목록가져오기
#html로 전달 --> 웹에 사진목록뜸
@app.route('/')
def index():
    images = []
    images = os.listdir(IMAGE_DIR)
    return render_template('filter_viz.html', images=images)

# 필터 커널 정의 (사진필터공식표)
FILTER = {
    'blur' : np.ones((3,3), np.float32) / 9
  , 'sharpen':np.array([[0, -1, 0], [-1, 5,-1], [0, -1, 0]])  #선명
    , 'edge' : np.array([[0,1,0], [1,-4,1], [0,1,0]]) #윤곽선
}
def to_b64(img):
    # html img 사용할 수 있는 base64 문자열로 변환(html은사진을바로못씀->문자로바꾸기)
    _, buffer = cv2.imencode('.png', img)
    return "data:image/png;base64," + base64.b64encode(buffer).decode('utf-8')
#웹에서 필터눌렀을때실행
@app.route('/api/filter', methods = ['POST'])
def apply_filter():   #웹에서 보낸 데이터받기
    filename = request.form.get('filename')      #ex-filename = cat.jpg
    filter_name = request.form.get('filter')   #filter = blur
    path = os.path.join(IMAGE_DIR, filename)  # 이미지불러오기

    # 작동되는지 확인
    # print(filter_name, filename, path)
    # return jsonify ({'error' : 'test'}), 400

    img = cv2.imread(path)
    if filter_name == 'original' or filter_name not in FILTER:
        kernel_list = None #선택할필터ㅋ꺼내기
        res_img = img   #사진에 계산해서 적용
    else : #선택할필터ㅋ꺼내기#사진에 계산해서 적용
        kernel = FILTER[filter_name]
        kernel_list = kernel.tolist()
        res_img = cv2.filter2D(img, -1, kernel)

    return jsonify({'original' : to_b64(img)            # 원본
                       , 'filtered': to_b64(res_img)    # 적용
                       , 'kernel': kernel_list})        # 필터

if __name__ == '__main__':  #프로그램시작버튼
    app.run(debug = True)
# 전체흐름
#브라우저 접속 -> 사진 선택 -> 필터버튼->flask 서버로 전송 -> open cv로 계산
#결과돌려줌 -> 화면출력