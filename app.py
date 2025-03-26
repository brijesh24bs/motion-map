from flask import Flask, render_template, request
import joblib
import pandas as pd
import re
import string

def preprocess_text(text):
    text = text.lower()
    text = re.sub(f"[{string.punctuation}]", "", text)
    return text

# Load the trained SVM model and TF-IDF vectorizer
svm_model = joblib.load("models/svm_model.pkl")
tfidf_vectorizer = joblib.load("models/tfidf_vectorizer.pkl")

# Load exercise data
exercise_data = pd.read_csv("data/Condition_to_Exercises.csv")

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/app")
def app_page():
    return render_template("app.html")

@app.route("/diagnose", methods=["POST"])
def diagnose():
    user_input = request.form["symptom"]
    processed_input = preprocess_text(user_input)
    input_vec = tfidf_vectorizer.transform([processed_input]).toarray()
    
    # Predict condition
    predicted_condition = svm_model.predict(input_vec)[0]
    
    # Get recommended exercises
    exercises = exercise_data[exercise_data['condition'] == predicted_condition]
    exercise_list = exercises.to_dict(orient='records')
    
    return render_template("result.html", condition=predicted_condition, exercises=exercise_list)

if __name__ == "__main__":
    app.run(port=5001, debug=True)
