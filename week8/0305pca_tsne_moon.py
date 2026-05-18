import matplotlib.pyplot as plt
from sklearn.datasets import make_moons
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
#태국운영데이터생성
x,y = make_moons(n_samples=500, noise=0.1, random_state=42)

#pca 2->1 차원으로
pca = PCA(n_components=1)
x_pca = pca.fit_transform(x)
#perplexity 이웃범위
tsne=TSNE(n_components=1,random_state=42,init='pca',perplexity=30)
x_tsne = tsne.fit_transform(x)

fig,ax=plt.subplots(1,3,figsize=(18,5))
#좌측원본
ax[0].scatter(x[:,0], x[:,1], c=y, cmap='coolwarm', edgecolors='k')
ax[0].grid(True,linestyle='--',alpha=0.4)
#중앙 pca
ax[1].scatter(x_pca[:,0], [0]*len(x_pca), c=y, cmap='coolwarm')
ax[1].grid(True,linestyle='--',alpha=0.4)
#우측 t-sne
ax[2].scatter(x_tsne[:,0], [0]*len(x_tsne), c=y, cmap='coolwarm')
ax[2].grid(True,linestyle='--',alpha=0.4)
plt.show()