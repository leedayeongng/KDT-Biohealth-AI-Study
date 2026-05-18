from flask import Flask, render_template, request
import joblib
import pandas as pd
from xai_explainer import explain_decision
model = joblib.load('loan_model.pkl')
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])   #get 처음페이지들어올때, 주소창접속, post 폼제출
def index():
    if request.method == 'POST':  #포스트일때만 실행
        #사용자 입력 데이터로 변경
        # app_income = 0.0
        # coapp_income = 0.0
        # loan_amount = 0.0
        # married = 0.0
        app_income = float(request.form['app_income'])
        coapp_income = float(request.form['coapp_income'])
        loan_amount = float(request.form['loan_amount'])
        married = float(request.form['married'])
        input_data = pd.DataFrame([[app_income, coapp_income, loan_amount, married]]
            ,columns=['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Married'])
        pred = model.predict(input_data)[0] # 0:거절, 1:승인
        explanations = explain_decision(model, input_data)
        if pred == 1:
            result_msg ="대출 승인 가능"
            result_class="success"
        else:
            result_msg = "대출 승인 거절"
            result_class="danger"

        #확률, 입력데이터 리턴추가
        return render_template('index.html', result=result_msg, explanations=explanations, result_class=result_class)
    #post가 아닐때 기본화면만 보여줌
    return render_template('index.html')  #post가 아니면(get 이면)실행

if __name__ == '__main__':
    app.run(debug=True)