import cv2
import os
cap = cv2.VideoCapture('./video/sample.mp4') #sample.mp4 동영상 파일 열기
count = 0
interval = 10 #10 프레임마다 1장 저장
OUTPUT_PATH = os.path.join('./video', 'frames') #./video/frames 폴더 저장폴더만들기
if not os.path.exists(OUTPUT_PATH):
    os.mkdir(OUTPUT_PATH)

while True:
    ret, frame = cap.read() #ret:성공여부, frame:이미지 데이터
    if not ret:
        break #영상끝
    if count % interval == 0: #10으로 나눈 나머지가 0이면 저장
        file_name = f'frame_{count:04d}.jpg'
        save_path = os.path.join(OUTPUT_PATH, file_name)
        cv2.imwrite(save_path, frame) #사진 파일로 저장
        print(f'saved:{file_name}')
    count += 1
cap.release()
print('완료')

