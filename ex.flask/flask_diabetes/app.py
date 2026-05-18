from flask import Flask, render_template, request
import joblib
import pandas as pd

app = Flask(__name__)
print('model load')
model = joblib.load('./diabetes.model.pkl')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        glucose = float(request.form['glucose'])
        blood_pressure = float(request.form['blood_pressure'])
        bmi = float(request.form['bmi'])
        age = float(request.form['age'])
        input_data = pd.DataFrame([[glucose, blood_pressure, bmi, age]], columns=['plas', 'pres', 'mass', 'age'])
        prediction = model.predict(input_data)[0]   #0:정상, 1:위험
        print(prediction)
        probability = model.predict_proba(input_data)[0][1] * 100
        print(probability)
        if prediction == 1:
            result_msg = '당뇨병 발병 위험군으로 시뮬레이션 되었습니다.'
            result_class = 'danger'
        else:
            result_msg = '당뇨병 발병 위험이 낮은 것으로 시뮬레이션 되었습니다.'
            result_class = 'success'
        print(result_msg)
        return render_template('index.html', result=result_msg, result_class=result_class,
                              prob=f'{probability:.2f}%', glucose=glucose, blood_pressure=blood_pressure,bmi=bmi,age=age)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)