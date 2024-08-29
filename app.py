from flask import Flask, request, render_template, jsonify
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
    pred_LR = int(LR.predict(vect)[0])
    pred_DT = int(DT.predict(vect)[0])
    pred_GB = int(GB.predict(vect)[0])
    pred_RF = int(RF.predict(vect)[0])
    pred_SVM = int(svm_model.predict(vect)[0])
    return {
        "LR": pred_LR,
        "DT": pred_DT,
        "GB": pred_GB,
        "RF": pred_RF,
        "SVM": pred_SVM
    }
@app.route('/', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        try:
            data = request.get_json()
            if 'news' not in data:
                return jsonify({"error": "Error: 'news' field is missing in request"}), 400
            news = data['news']
            predictions = predict_news(news)
            return jsonify(predictions)
        except Exception as e:
            print(f"Error: {e}")
            return jsonify({"error": "Internal Server Error"}), 500
    else:
        return render_template('index.html')


if __name__ == "__main__":
    print("Starting the Flask application...")
    app.run(debug=True, port=5001)
