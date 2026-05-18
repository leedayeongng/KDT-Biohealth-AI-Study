import os

import cv2
import matplotlib.pyplot as plt
from pandas.core import frame

img = cv2.imread('./video/p.png') #사진 파일 읽기
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#haar cascade 분류기 (openCV 내장모델)
xml_path = os.path.join(cv2.data.haarcascades,
                        'haarcascade_frontalface_default.xml')
face_cascade = cv2.CascadeClassifier(xml_path)
#얼굴 탐지
#scaleFactor 1.1 -> 1.05 더세밀하게 스캔
# minNeighbors 5 > 3 조건완화
faces = face_cascade.detectMultiScale(img_gray
, scaleFactor=1.01, minNeighbors=6, minSize=(20, 20))
print(f'발견된 얼굴 수:{len(faces)}')
#결과 그리기
for (x, y, w, h) in faces:
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
plt.title('face detection')
plt.imshow(img_rgb)
plt.show()


#사진에서 사람얼굴자동으로 찾고 네모박스 표시 OpenCV 내장 AI 모델 사용