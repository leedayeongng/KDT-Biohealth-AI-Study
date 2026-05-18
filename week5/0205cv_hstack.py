import cv2 #사진처리
import numpy as np #배열붙이기


img1 = cv2.imread('./imageNet/cat1.jpg')
img2 = cv2.imread('./imageNet/cat2.jpg')
# img1 높이 vs img2 높이 더 작은값 선택해서 합치기
h = min(img1.shape[0], img2.shape[0]) #min(행)
#높이를 맞춘 뒤 가로로 합치기     shape[0]=높이, shape[1]=너비
img1_r = cv2.resize(img1, (int(img1.shape[1]*h/img1.shape[0]),h))
img2_r = cv2.resize(img2, (int(img2.shape[1]*h/img2.shape[0]), h))
                                    #새 가로 = 원래가로 × (새높이 / 원래높이) 안찌그러지게맞춤
hstack = np.hstack([img1_r, img2_r])
cv2.imshow('hstack', hstack)    #imshow 창띄우기
cv2.waitKey(0) #waitkey 멈추기
cv2.destroyAllWindows()   #destroy 닫기
#충돌할때(밑에 두코드씀)
#pip install easyocr
#pip install --user easyocr

# 이코드들은 cat1+cat2 가로로합쳐서 나란히 보여주는 코드
#사진1,2불러옴 -> 높이 맞춤 -> 비율유지리사이즈 -> 옆으로 붙임 -> 화면출력

