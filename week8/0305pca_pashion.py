import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import fetch_openml
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
print("패션 쇼핑몰 아이템 수만장의 티셔츠, 바지 .. 이미지를 2차원으로")
X,y = fetch_openml('Fashion-MNIST',version=1,return_X_y=True,as_frame=False)
#학습 속도를 위해 5000개랜덤 추출
print(X.shape)
plt.figure(figsize=(10,6))
for i in range(10):
    plt.subplot(2,5,i+1)
    img=X[i].reshape(28,28)
    plt.imshow(img,cmap='gray')
    plt.axis('off')
plt.show()
np.random.seed(42)
indices = np.random.choice(X.shape[0],5000, replace=False)
x_subset = X[indices]
y_subset = y[indices].astype(int)
class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress'
            , 'Coat','Sandal','Shirt','Sneaker','Bag',
            'Ankle boot']
y_names = [class_names[label] for label in y_subset]
scaler = StandardScaler()
x_scaled = scaler.fit_transform(x_subset)
pca = PCA(n_components=2)
x_pca = pca.fit_transform(x_scaled)
pca_df = pd.DataFrame(data=x_pca, columns=['PC1','PC2'])
pca_df['Item_Type'] = y_names
print(f'{pca.explained_variance_ratio_[0]*100:.1f}%')
print(f'{pca.explained_variance_ratio_[1]*100:.1f}%')
plt.figure(figsize=(14,10))
sns.scatterplot(x='PC1',y='PC2',hue='Item_Type',palette='tab10',data=pca_df, s=30, alpha=0.7)
plt.show()