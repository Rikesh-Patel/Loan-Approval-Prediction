# Importing essential libraries
from flask import Flask, render_template, request
import pandas as pd
#from joblib import load


# Load the LDA model
#pipe = load('Loan-Model.pkl')
#import joblib
app = Flask(__name__)

@app.route('/')
def home():
	  return render_template('index.html')

@app.route('/predict')
def predict():
#         gender = request.form['gender']
#         married = request.form['married']
#         deps = request.form['dep']
#         education = request.form['education']
#         self_employed = request.form['self_employed']
#         income = float(request.form['income'])
#         co_income = float(request.form['co_income'])
#         loan = float(request.form['loan'])
#         term = float(request.form['term'])
#         history = float(request.form['history'])
#         area = request.form['area']
        
        # data = pd.DataFrame([(gender,married,deps,education,self_employed,income,co_income,loan,term,history,area)], columns=["Gender","Married","Dependents","Education","Self_Employed","ApplicantIncome","CoapplicantIncome","LoanAmount","Loan_Amount_Term","Credit_History","Property_Area"])
        url= 'https://loan5.herokuapp.com/api'
        import json 
        import requests 
        # sample data
        data={'Gender':1, 'Married':1, 'Dependents':2, 'Education':0, 'Self_Employed':1,'Credit_History':0,'Property_Area':1, 'Income':1} 
        data = json.dumps(data) 
        # test working 
        requests.post(url, data) 
        send_req = requests.post(url, data) 
        #my_prediction = int(pipe.predict(data))
        return render_template('predict.html', prediction = 'Y')
        
if __name__ == '__main__':
	app.run(debug=True)
