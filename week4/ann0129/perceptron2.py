
#pip install scikit-learn
# perceptron
from sklearn.neural_network import MLPClassifier # 다층 퍼셉트론: 층을 여러 개 쌓은 고수 (XOR 해결 가능)
from sklearn.linear_model import Perceptron # 단층 퍼셉트론: 층이 하나뿐인 초보 (직선만 그음, XOR 불가능)
# 2. 데이터 준비 (XOR 문제)
# 입력값(x): 문제집(x)과 정답지(y) 준비
x = [[0, 0], [1, 0], [0, 1], [1, 1]]
# # XOR 문제 (서로 다를 때만 1!)
y = [0, 1, 1, 0]
#XOR 문제(정답 [0, 1, 1, 0])를 평면에 점으로 찍으면, 직선 하나로는 절대 0과1을 가를 수 없습니다. 이걸 선형 비분리(Linearly Inseparable)
# hidden_layer_sizes=(4, ): 입력과 출력 사이에 4개의 뇌세포(은닉층)를 추가함 -> 복잡한 생각을 하게 함
# activation='tanh': 계산 결과를 부드러운 '곡선'으로 만듦 (비선형성 부여) -> 직선이 아닌 모양으로 나눌 수 있음
model = MLPClassifier(hidden_layer_sizes=(4, ), activation='tanh'
                      ,max_iter=1000, random_state=1)
#p_model = Perceptron()은 수학적으로 **선형 분리(Linear Separation)**만 가능
# 단층 퍼셉트론
# max_iter=1000: 문제집을 최대 1000번 반복해서 풀어보라는 뜻 (학습 횟수)
# random_state=1: 매번 실행할 때마다 결과가 달라지지 않게 고정함
p_model = Perceptron(max_iter=1000, random_state=1)
#model.fit(x, y)
# 4. 학습 단계 (공부 시키기)
# fit(x, y): "문제(x)와 정답(y)을 줄 테니 관계를 찾아봐!"라고 명령하는 핵심 함수
# model.fit(x, y)   # (고수 모델을 공부시키려면 이 주석을 푸세요)
#p_model.fit(x, y) # 현재는 초보 모델만 공부시키는 중
model.fit(x, y)
#print(mode.predict(x))
#print(p_model.predict(x))
print(model.predict(x))ter=1000, random_state=1)
# [이론 포인트]
# p_model은 '직선' 하나만 그을 수 있어서 XOR 문제를 절대 못 풀어요. (결과가 [0,0,0,0] 등으로 틀림)
# 반면 model(MLP)은 '은닉층'과 '곡선 함수' 덕분에 완벽하게 맞힐 수 있습니다.

#다층 퍼셉트론(MLP)*