import numpy as np

# 활성 함수 (activation function)
# 신호를 보낼지말지
def step_function(sum):
    if sum > 0: #계산된 합이 0을 넘으면
        return 1 #신호전달
    return 0  #들어온 신호의 합(sum)이 0보다 크면 1(활성화), 작거나 같으면 0(비활성화)을 반환

class Perceptron:
    def __init__(self, input_size):
        # 가중치 초기화 입력이 가중치 2개 + 편향(bias)용 1개 = 총 3개의 자리를 0으로 만듭니다.
         # +1 의 의미(편향, bias) w1x1 + w2x2 + bias에서 bias를 위한 자리를 하나 더만듬
        #요리할 때 '소금(입력1)'을 얼마나 넣을지, '설탕(입력2)'을 얼마나 넣을지 그 비율을 처음에 랜덤하게 정리
        #가중치($w$): 입력 데이터($x$)가 결과에 얼마나 큰 영향을 주는지 정하는 수치
        self.w = np.zeros(input_size + 1)
    def predict(self, inputs):
        # (입력값 * 가중치)를 다 더하고, 거기에 마지막 가중치(편향)를 더합니다.
        sum = np.dot(inputs, self.w[1:]) + self.w[0]
        #np dot : np.dot은 [x1, x2]와 [w1, w2]를 짝지어 곱하고 합치는 '수학적 꼼수
        # 계산된 함율 활성함수에 넣어 0or1 판단
        return step_function(sum) # 문지기에게 물어봐서 0 또는 1을 리턴
    # 학습하기 trin
    def train(self, train_inputs, labels, lr=0.01, epochs=100):
        ## epochs: 전체 데이터를 몇 번 반복해서 공부할 것인가
        for _ in range(epochs):
            for inputs, label in zip(train_inputs, labels):
                #1.# 1. 인공지능이 현재 실력으로 예측해봄
                pred = self.predict(inputs)
                # 2. 틀린 만큼 가중치를 수정합니다 (오답 노트 반영).
                # 오차(정답 - 예측)에 학습률과 입력값을 곱해서 가중치에 더해줍니다.
                print(f'before:{self.w[1:]} , {self.w[0]}')
                self.w[1:] += lr * (label - pred) * inputs
                print(f'after:{self.w[1:]} , {self.w[0]}')
                self.w[0] += lr * (label - pred)
    # 학습데이터
    #0과 1로 조합된 4가지 상황입
train_data = np.array([
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
])
# labels = np.array([0, 0, 0, 1]) # and 연산
#labels = np.array([0, 1, 1, 1]) # or 연산
labels = np.array([0, 1, 1, 0]) #xar연산  #같으면 0, 다르면 1
model = Perceptron(input_size=2) #입력 2개 # 모델 생성: 입력이 2개(0 또는 1)인 인공지능을 만듭니다
model.train(train_data, labels, lr=0.1) # 학습 시작: 준비한 데이터로 100번 반복 학습합니다 (학습률 0.1).

#결과 확인
for i, v in zip(train_data, labels):
    pred = model.predict(i) # 예측해보고
    print(f'입력 :{i}, 예측:{pred}, 정답:{v} ')  # 화면에 찍어줍니다.
print('학습된 내부 가중치')
# 인공지능 뇌 속에 저장된 최종 값들을 보여줍니다.
print(f'가중치(weights):{model.w[1:]}')
print(f'편향(bias):{model.w[0]}')



    # 머신러닝 가장 기초 퍼셉트론 코드 , 인공지능이 예(1) 아니오 (0)를 결정하는 의사결정구조를 담고있따
