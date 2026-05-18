import cv2
import numpy as np

img = cv2.imread('./video/sample.jpg') #사진 → 숫자 배열
print(f'데이터 타입:{type(img)}')
print(f'shape(높이, 너비, 채녈) : {img.shape}')
print(f'size(픽셀 수):{img.size}')
print(f'픽셀 타입{img.dtype}') # unit8(0 ~ 255)
y, x = 100, 100
pixel = img[y, x]
print(f'\n 좌표 ({x}, {y})의 픽셀 값 (BGR):{pixel}')
img[50:150, 50:150] = [255, 255, 255] #흰색 박스
print(f'\n(50,50)부터 (150, 150)까지 ')
cv2.imshow('matrix', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
