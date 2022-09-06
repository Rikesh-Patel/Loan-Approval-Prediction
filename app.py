# Importing essential libraries
from flask import Flask, render_template, request
import pandas as pd
import joblib

# Load the LDA model
pipe = joblib.load('Loan-Model.pkl')

app = Flask(__name__)

@app.route('/')
def home():
        if 1==1:
                return render_template('templates/predict.html')
        else:
	        return render_template('templates/index.html')

@app.route('/predict')
def predict():
        gender = request.form['gender']
        married = request.form['married']
        deps = request.form['dep']
        education = request.form['education']
        self_employed = request.form['self_employed']
        income = float(request.form['income'])
        co_income = float(request.form['co_income'])
        loan = float(request.form['loan'])
        term = float(request.form['term'])
        history = float(request.form['history'])
        area = request.form['area']
        
        data = pd.DataFrame([(gender,married,deps,education,self_employed,income,co_income,loan,term,history,area)], columns=["Gender","Married","Dependents","Education","Self_Employed","ApplicantIncome","CoapplicantIncome","LoanAmount","Loan_Amount_Term","Credit_History","Property_Area"])
        my_prediction = int(pipe.predict(data))
        
        return render_template('predict.html', prediction = my_prediction)

        

if __name__ == '__main__':
	app.run(debug=True)
