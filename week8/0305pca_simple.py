import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

X = np.array([
    [2,1,1],
    [3,2,0],
    [4,1,2],
    [5,3,1],
    [6,2,3]
])
print('original data \n',X)
#원본3d그래프
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
#원본 3d 그래프
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(X[:,0],X[:,1],X[:,2],c='blue',s=80)
ax.set_xlabel('X1')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()
#평균 계산 및 이동
mean = X.mean(axis=0)
X_center = X - mean
print('mean:',mean)
print('X_center:',X_center)
#중심이동
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
#원본 3d 그래프
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(X_center[:,0],X[:,1],X_center[:,2],c='green',s=80)
ax.set_xlabel('X1')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()
#공분산 행렬 계산
cov = np.cov(X_center.T)
print('cov matrix:',cov)
#고유값 고유백터 계산
eigvals, eigvecs = np.linalg.eig(cov)

print('eigenvalues:', eigvals)
print('eigenvectors:', eigvecs)

#pca 시각화
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(X_center[:,0],X_center[:,1],X_center[:,2],c='blue',s=80)
origin = [0,0,0]
for i in range(3):
    vec = eigvecs[:,i]
    ax.quiver(origin[0], origin[1], origin[2], vec[0], vec[1], vec[2], length=2, color='red')
plt.show()
#pca 투명 3d->2d
PC = eigvecs[:,:2]
X_pca = X_center @ PC
plt.scatter(X_pca[:,0],X_pca[:,1],color='red',s=100)
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.show()
#설명분산
explained_var = eigvals / eigvals.sum()
plt.bar(["PC1", "PC2","PC3"], explained_var)
plt.show()
print(explained_var)
