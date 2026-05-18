import cv2

#픽셀 밝기값이 특정 임계값보다 높으면 흰색, 낮으면 검은색 변환
img = cv2.imread('./imageNet/cat1.jpg', cv2.IMREAD_GRAYSCALE)
ret, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
cv2.imshow('thresholding', thresh)

gaussian = cv2.GaussianBlur(img, (15, 15), 0)  #핵심, 사진흐리게하기
cv2.imshow('blur', gaussian)

cv2.waitKey(0) #
cv2.destroyAllWindows()