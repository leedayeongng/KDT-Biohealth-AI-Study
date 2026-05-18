import numpy as np

data = np.array([
        [82,93],
        [83,95],
        [84,94],
        [85,96],
        [86,95]
])
#평균제거
x = data - np.mean(data, axis=0)
print(X)
XTX = np.dot(X,T, X)
print(XTX)
cov = XTX / (len(data) - 1)
print('공분산 행렬')
print(cov)
print("np.cov 동일함")
cov_matrix = np.cov(data.T)
print(cov_matrix)

