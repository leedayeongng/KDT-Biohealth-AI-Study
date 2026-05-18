import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

print('PCA vs t-SNE(비선형 차원 축소)')
digits = load_digits()
x=digits.data
y=digits.target
print(f'데이터크기: {x.shape[0]} 개의 샘플, {x.shape[1]} 차원(픽셀')
#pca
pca = PCA(n_components=2)
x_pca = pca.fit_transform(x)
#t-sne
tsne = TSNE(n_components=2, random_state=42)
x_tsne = tsne.fit_transform(x)
#시각화
fig,ax=plt.subplots(1,2,figsize=(16,7))
#좌측 PCA
scatter_pca = ax[0].scatter(x_pca[:,0], x_pca[:,1], c=y, cmap='tab10')
ax[0].grid(True, linestyle='--',alpha=0.5)
#우측 t-SNE
scatter_tsne = ax[1].scatter(x_tsne[:,0], x_tsne[:,1], c=y, cmap='tab10')
ax[1].grid(True, linestyle='--',alpha=0.5)
plt.show()