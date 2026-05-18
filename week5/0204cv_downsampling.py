import cv2
import matplotlib.pyplot as plt

img = cv2.imread('./video/p.png')
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
print('다운 샘플링')

# 슬라이싱 [start:end:step]
# [::2] 처음부터 끝까지 2칸씩
down2 = img_rgb[::2, ::2]
down4 = img_rgb[::4, ::4]
down8 = img_rgb[::8, ::8]
print(f' 원본 shape: {img_rgb.shape}')
print(f'1/2 shape: {down2.shape}')
print(f'1/4 shape: {down4.shape}')
print(f'1/8 shape: {down8.shape}')
plt.figure(figsize=(12, 4))
plt.subplot(1,4,1)
plt.imshow(img_rgb)
plt.title('original')
plt.axis('off')
plt.subplot(1,4,2)
plt.imshow(down2)
plt.title('1/2')
plt.axis('off')
plt.subplot(1,4,3)
plt.imshow(down4)
plt.title('1/4')
plt.axis('off')
plt.subplot(1,4,4)
plt.imshow(down8)
plt.title('1/8')
plt.axis('off')
plt.show()