from flask import Flask, request, render_template
import pandas as pd
import numpy as np
import re
import string
import joblib

# Initialize the Flask app
app = Flask(__name__)

# Load models and vectorizer
LR = joblib.load('logistic_regression_model.pkl')
DT = joblib.load('decision_tree_model.pkl')
GB = joblib.load('gradient_boosting_model.pkl')
RF = joblib.load('random_forest_model.pkl')
svm_model = joblib.load('svm_model.pkl')
vectorization = joblib.load('vectorizer.pkl')

def wordopt(text):
    text = text.lower()
    text = re.sub(r'\[.*?\]', '', text)  # Remove text within square brackets
    text = re.sub(r'\W', ' ', text)      # Replace non-word characters with a space
    text = re.sub(r'https?://\S+|www\.\S+', '', text)  # Remove URLs
    text = re.sub(r'<.*?>', '', text)   # Remove HTML tags
    text = re.sub(r'[%s]' % re.escape(string.punctuation), '', text)  # Remove punctuation
    text = re.sub(r'\n', '', text)       # Remove newlines
    text = re.sub(r'\w*\d\w*', '', text) # Remove alphanumeric words with digits
    return text

def predict_news(news):
    news = wordopt(news)
    vect = vectorization.transform([news])
    pred_LR = LR.predict(vect)[0]
    pred_DT = DT.predict(vect)[0]
    pred_GB = GB.predict(vect)[0]
    pred_RF = RF.predict(vect)[0]
    pred_SVM = svm_model.predict(vect)[0]
    return {"LR": pred_LR, "DT": pred_DT, "GB": pred_GB, "RF": pred_RF, "SVM": pred_SVM}

@app.route('/', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        news = request.form['news']
        predictions = predict_news(news)
        return render_template('index.html', 
                               news=news, 
                               pred_lr=predictions['LR'],
                               pred_dt=predictions['DT'],
                               pred_gb=predictions['GB'],
                               pred_rf=predictions['RF'],
                               pred_svm=predictions['SVM'])
    else:
        return render_template('index.html')

if __name__ == "__main__":
    print("Starting the Flask application...")
    app.run(debug=True, port=5001)
