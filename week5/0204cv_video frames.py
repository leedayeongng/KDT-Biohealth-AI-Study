import cv2
import os
cap = cv2.VideoCapture('./video/Air_Force_One.mp4') #sample.mp4 동영상 파일 열기
count = 0
interval = 10 #10 프레임마다 1장 저장
OUTPUT_PATH = os.path.join('./video', 'frames') #./video/frames 폴더 저장폴더만들기
if not os.path.exists(OUTPUT_PATH):
    os.mkdir(OUTPUT_PATH)
#배경 제거 객체 생성(MOG2 알고리즘)
subtractor = cv2.createBackgroundSubtractorMOG2(history=500
                        #임계값        #그림자 감지
                        ,varThreshold=50, detectShadows=True)

while True:
    ret, frame = cap.read() #ret:성공여부, frame:이미지 데이터
    if not ret:
        print('영상 반복')
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue
    #움직이는 물체 255, 배경 0, 그림자 127
    mask = subtractor.apply(frame)
    cv2.imshow('original', frame)
    cv2.imshow('background mask', mask)
    if cv2.waitKey(30) & 0xff == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
print('완료')

#영상분석
#영상에서 움직이는 물체만 자동으로 찾아내는 프로그램입니다.