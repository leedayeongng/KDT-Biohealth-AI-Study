import easyocr  #글자읽는 ai
import cv2 #이미지처리
import os
#라이브러리 충돌 무시하고 실행
# os.environ['KMP_DUPLICATE_LIB_OK']='True'
# #수치연산 엔진을 INTEL 최적화 모드로 고정
# os.environ['MKL_SERVICE_FORCE_INTEL'] = '1'
img = cv2.imread('./imageNet/111.png') #111.png를 열겠다
reader = easyocr.Reader(['en', 'ko'], gpu=False) #영어 + 한글 읽고 gpu안쓰고cpu쓸게
result = reader.readtext(img) #AI가 사진 분석함
for bbox, text, prob in result:  #읽은 글자 콘솔에 출력
    print(text)

img_display = img.copy() #원본 안 망가뜨리려고 복사본 생성
GREEN = (0, 255, 0) #초록색 RGB 박스생성
for bbox, text, prob in result: #하나씩 처리
    (tl, tr, br, bl) = bbox #조ㅏ표꺼내기
    tl = (int(tl[0]), int(tl[1]))
    br = (int(br[0]), int(br[1]))
    #박스 그리기
    cv2.rectangle(img_display, tl, br, GREEN, 2)
# cv2.imshow('ocr result', img_display)
cv2.imwrite('./ocr.png', img_display)
# cv2.waitKey(0) #원래는 화면 띄우는 코드이다
# cv2.destroyAllWindows()

#사진입력, easyocr분석, 글자추출, 좌표계산 ,박스그림, 파일저장
#번역앱카메라, 사진찍으면 글자잡아주는거,