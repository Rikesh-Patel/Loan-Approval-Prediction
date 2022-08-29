# Importing essential libraries
from flask import Flask, render_template, request
import pickle
from pycaret.classification import load_model,predict_model
import pandas as pd

# Load the LDA model
filename = 'Loan-Model.pkl'
classifier = load_model(open(filename, 'rb'))

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/predict')
def predict():
     if request.method == 'POST':
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
        
        df = pd.DataFrame([(gender,married,deps,education,self_employed,income,co_income,loan,term,history,area)],
                  columns=["Gender","Married","Dependents","Education","Self_Employed","ApplicantIncome","CoapplicantIncome","LoanAmount","Loan_Amount_Term","Credit_History","Property_Area"])
        my_prediction = ' '.join(predict_model(classifier, df)['Label'].values)
        return render_template('predict.html', prediction = my_prediction)
        


if __name__ == '__main__':
	app.run(debug=True)
