import cv2
import os
cap = cv2.VideoCapture('./video/Air_Force_One.mp4') #sample.mp4 동영상 파일 열기


mode = 0 #0 none, 1:blur, 2:edge
while True:
    ret, frame = cap.read() #ret:성공여부, frame:이미지 데이터
    if not ret:
        print('영상 반복')
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue
    if mode == 1: #blur 화면을 흐리게 만들기
        frame = cv2.blur(frame, (15, 15))
        cv2.putText(frame, 'mode:blur', (200, 30)
                    , cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    elif mode == 2:    #EDGE모드 !!! ***
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #흑백변환
        edge = cv2.Canny(gray, 100, 200) #윤곽선추출
        frame = cv2.cvtColor(edge, cv2.COLOR_GRAY2BGR)   #다시컬러
        cv2.putText(frame, 'mode:original', (200, 30)
                    , cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    else:
        cv2.putText(frame,'mode:original',(200,30)
                    , cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255),2)
    cv2.imshow('video',frame)
    key = cv2.waitKey(30) & 0xFF
    if key ==ord('q'):
        break
    elif key ==ord('0'):mode=0
    elif key ==ord('1'):mode=1
    elif key == ord('2'):
        mode = 2
    if cv2.waitKey(30) & 0xff == ord('q'):break

cap.release()
cv2.destroyAllWindows()
print('완료')

#영상분석
#동영상재생, 키보드 0:원본화면, 1:블러효과, q:종료 2:윤곽선