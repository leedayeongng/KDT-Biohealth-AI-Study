import joblib
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.datasets import fetch_openml

data = fetch_openml(name='diabetes', version=1, as_frame=True)
print(data.frame)
df = data.frame
# plas:혈당, pres:혈압, mass:BMI, age:나이, class: tested_positive[양성],tested_negative[음성]
x=df[['plas', 'pres', 'mass', 'age']]
y=df['class']
y = y.map({'tested_positive':1, 'tested_negative':0})
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=1)
print('최적의 하이퍼파라미터 찾기! (시간이 조금 걸릴수있음.)')
param_grid = {
    'n_estimators': [50, 100, 200, 300], #트리 수
    'max_depth': [None, 5, 10, 15, 20], #트리깊이
    'min_samples_split': [2, 5, 10, 20], #최소 샘플 수
    'min_samples_leaf': [1, 2, 4, 8]    #리프노드최소샘플수
}
base_model = RandomForestClassifier(random_state=1)
#gridSearch setting
grid_search = GridSearchCV(estimator=base_model, param_grid=param_grid
                           , cv=5  #5-fold 교차검증
                           , n_jobs=-1 #모든 cpu 사용
                           , scoring='accuracy')
grid_search.fit(x_train, y_train)
#최적 모델
best_model = grid_search.best_estimator_
print(f'최적의 파라미터 : {grid_search.best_params_}')
#정확도 평가
y_pred = best_model.predict(x_test)
accuracy = accuracy_score(y_test, y_pred)
print(f'최적의 모델 정확도 : {accuracy * 100:.2f}%')
joblib.dump(best_model, 'diabetes.model.pkl')
print('저장 완료!')
#결과
results = pd.DataFrame(grid_search.cv_results_)
results_sorted = results.sort_values(by=['mean_test_score'], ascending=False)
print(results_sorted)


