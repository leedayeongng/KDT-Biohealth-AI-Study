import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression   #분류
from mpl_toolkits.mplot3d import Axes3D
from sklearn.datasets import make_circles
from sklearn.linear_model import LinearRegression

np.random.seed(0)
x, y = make_circles(n_samples=200, noise=0.05, factor=0.5)
fig = plt.figure()
plt.scatter(x[:,0], x[:,1], c=y)
plt.title('2d space nonlinear')
plt.xlabel('x1')
plt.ylabel('x1')
plt.show()

def phi(input_x):
    """2차원 데이터(x1,x2)를 3차원으로 확장하는 매핑 함수"""
    x1 = input_x[:,0]
    x2 = input_x[:,1]
    return np.column_stack([x1, x2, x1**2 + x2**2])
x_mapped = phi(x)
#3d 공간 시간화
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x_mapped[:,0], x_mapped[:,1], x_mapped[:,2], c=y)
ax.set_xlabel('x1')
ax.set_ylabel('x2')
ax.set_zlabel('x1^2 + x2^2')
ax.set_title('mapped 3d space')
plt.show()

#2d에서의결정경계
h = 0.02 # 각자 간격
#범위 설정
x_min, x_max = x[:, 0].min() - 1, x[:, 0].max() + 1
y_min, y_max = x[:, 1].min() - 1, x[:, 1].max() + 1
#실제 데이터 최소/최대값보다 1만큼 더 확장
#2d 평면 전체를 촘촘한 격자로
xx, yy = np.meshgrid(np.arange(x_min, x_max, h),np.arange(y_min, y_max, h)
)
#np.c_ x,y 좌표를 양 방향으로 결함
grid = np.c_[xx.ravel(), yy.ravel()]  #ravel()2차원 배열을 1차원으로 펼침
grid_mapped = phi(grid)
model = LogisticRegression()
model.fit(x_mapped,y)
z = model.predict(grid_mapped)
z = z.reshape(xx.shape)
plt.figure()
plt.contour(xx,yy,z,alpha=0.3)
plt.scatter(x[:,0], x[:,1], c=y)
plt.show()