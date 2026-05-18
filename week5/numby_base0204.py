import numpy as np
#pip install opencv-python
# 1. 배열 생성과 속성
print("="*100)
#1차원 배열 vector
arrid = np.array([1, 2, 3, 4, 5, 6])
print(f'1d {arrid}')
print(f'ndim(차원 수): {arrid.ndim}')
print(f'shape(형태): {arrid.shape}')
print(f'dtype(타입): {arrid.dtype}')
#2.reshape(형태변경)
print("="*100)
add2d = arrid.reshape(2, 3)
print(f'reshape(2,3):\n{add2d}')
print(f'shape(형태): {add2d.shape}')
print(f'dtype(타입): {add2d.dtype}')
#3행 -1은 나머지 알아서
arr_auto = arrid.reshape(3, -1)
print(f'reshape(3,-1):\n{arr_auto}')

vector_1d = np.array([1, 2, 3])
print(f'1d vector:{vector_1d.shape}')
#행벡터 (1행 n열)
row_vec = vector_1d.reshape(1, -1)
print(f'row vector(1x3):\n{row_vec}')
print(f'shape:{row_vec.shape}')
#열백터 (n행 1열)
col_vec = vector_1d.reshape(-1,1)
print(f'col vector(3x1):\n{col_vec}')
print(f'shape:{col_vec.shape}')
#행렬의 결함( concat)
print("="*100)
A = np.array([[1, 2]
            ,[3, 4]])
B = np.array([[5, 6],[7, 8]])
print(f'A:\n{A}')
print(f'B:\n{B}')
# 수직 결합
v_stack = np.vstack([A, B])
print(f'\[v_stack] 위아래 결합:\n{v_stack}')
print(f'shape {v_stack.shape}')
#수평 결합
h_stack = np.hstack([A, B])
print(f'\n[hastack] 옆으로 결합:\n{h_stack}')
print(f'shape {h_stack.shape}')
print("="*50)
#브로드캐스팅
C = np.array([[10], [20]]) #2,1 열벡터
result = A + C
print(f'행렬 A\n:{A}')
print(f'열백터 C\n:{C}')
print(f'result(A + C):\n{result}')
