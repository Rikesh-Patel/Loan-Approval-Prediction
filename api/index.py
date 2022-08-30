# Importing essential libraries
from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/predict',  methods=['GET','POST']))
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
	
	

        return render_template('predict.html')
        

if __name__ == '__main__':
	app.run(debug=True)
