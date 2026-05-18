import os
import joblib
from sklearn. datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

iris = load_iris()
x,y = iris.data, iris.target

x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=42)
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(x_train, y_train)
y_pred = model.predict(x_test)
acc = accuracy_score(y_test, y_pred)
print(f'모델 훈련 완료! 테스트 정확도:{acc:.4f}')

#모델 저장
os.makedirs('models', exist_ok=True)
model_path = "models/iris.model.pkl"
joblib.dump(model, model_path)
print(f'모델이 {model_path}에 저장됨.')