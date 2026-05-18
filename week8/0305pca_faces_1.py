import matplotlib.pyplot as plt
from sklearn.datasets import fetch_olivetti_faces
from sklearn.decomposition import PCA
import numpy as np
print("수천 개의 픽셀로 이루어진 얼굴을 -> 몇십개의 핵심특성으로 압축")

faces = fetch_olivetti_faces()
n_samples, h, w = faces.images.shape
X = faces.data #필셀데이터(1차원으로 펼쳐진)
print(f'이미지 개수:{n_samples}')
print(f'이미지 차원(크기):세로{h}px x 가로{w}px = 총 {X.shape[1]} 차원')

n_components = 60
print(f'{X.shape[1]}을 ->{n_components}으로')
pca = PCA(n_components=n_components, svd_solver='randomized', whiten=True).fit(X)
eigenfaces = pca.components_.reshape(n_components, h, w)
print(f'압축 완료:{pca.explained_variance_ratio_[0]}')
print('복원')
X_pca = pca.transform(X) #60차원으로 줄임
X_projected = pca.inverse_transform(X_pca) #다시원래차원으로 복원

#시각화(원본 vs 복원 vs 고유얼굴 특징)
fig, axes = plt.subplots(
    3, 5,
    figsize=(15,9),
    subplot_kw={'xticks':[], 'yticks':[]},
    gridspec_kw=dict(hspace=0.3, wspace=0.1)
)
for i in range(5):
    #첫번째줄 : 원본얼굴
    axes[0,i].imshow(X[i].reshape(h,w), cmap='bone')
    axes[0,i].set_title('original 4096 pixels', fontsize=10)
    #두번째줄 : 복원얼굴
    axes[1, i].imshow(X_projected[i].reshape(h, w), cmap='bone')
    axes[1, i].set_title('reconstructed 4096 pixels', fontsize=10)
    #세번째줄 pca 60특성
    axes[2, i].imshow(eigenfaces[i], cmap='bone')
    axes[2, i].set_title('eigenfaces 60 pixels', fontsize=10)
plt.show()