import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.metrics import accuracy_score
import joblib

train_df = pd.read_csv('../../datasets/decision/train_loan_80.csv')
test_df = pd.read_csv('../../datasets/decision/test_loan_20.csv')

#컬럼 조회 후 뽑아내기
print(train_df.columns)
# Index(['Gender', 'Married', 'Dependents', 'Education', 'Self_Employed',
#        'ApplicantIncome', 'CoapplicantIncome', 'LoanAmount',
#        'Loan_Amount_Term', 'Credit_History', 'Property_Area', 'Loan_Status'],
#       dtype='object')
features = ['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Married']

#결측치 있는 행 삭제
train_df = train_df.dropna(subset=features + ['Loan_Status'])
test_df = test_df.dropna(subset=features + ['Loan_Status'])
# print(train_df.head())
x_train = train_df[features].copy()
y_train = train_df['Loan_Status'].copy()
x_test = test_df[features].copy()
y_test = test_df['Loan_Status'].copy()
#print(x_train.head())

# no:0, yes:1
for x_data in [x_train, x_test]:
    x_data['Married'] = x_data['Married'].map({'No':0, 'Yes':1})
y_train = y_train.map({'N':0, 'Y':1})
y_test = y_test.map({'N':0, 'Y':1})
param_grid = {
    'max_depth' : [3, 4, 5, 6, 7]
    , 'min_samples_split' : [2, 5, 10]
    , 'min_samples_leaf' : [1, 2, 4]
    , 'random_state' : [42]
}

grid_search = GridSearchCV(DecisionTreeClassifier(), param_grid=param_grid, cv=5, n_jobs=-1, scoring='accuracy')
print('DT 학습!')
grid_search.fit(x_train, y_train)
best_model = grid_search.best_estimator_
print(f'최적 파라미터: {grid_search.best_params_}')
y_pred = best_model.predict(x_test)
print(f'모델 정확도 : {accuracy_score(y_test, y_pred)*100:.2f}%')
joblib.dump(best_model, 'loan_model.pkl')

#트리 규칙
tree_rules = export_text(best_model, feature_names = features)
print('학습된 의사결정나무 대출 심사 규칙')
print(tree_rules)