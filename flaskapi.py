from flask import Flask, request, jsonify
import pickle
import pandas as pd

app = Flask(__name__)

# Load model
model = pickle.load(open("C:\\Users\\bharath hs\\Downloads\\churn_project\\telco_churn\\model.pkl", "rb"))
columns = pickle.load(open("C:\\Users\\bharath hs\\Downloads\\churn_project\\telco_churn\\columns.pkl", "rb"))

@app.route("/")
def home():
    return "Churn Prediction API is running"

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    input_dict = {col: 0 for col in columns}

    input_dict['tenure'] = data.get('tenure', 0)
    input_dict['MonthlyCharges'] = data.get('MonthlyCharges', 0)
    input_dict['SeniorCitizen'] = data.get('SeniorCitizen', 0)
    input_dict['PaperlessBilling_Yes'] = data.get('PaperlessBilling', 0)

    input_df = pd.DataFrame([input_dict])

    prob = model.predict_proba(input_df)[0][1]
    prediction = int(prob > 0.5)

    return jsonify({
        "churn_probability": round(prob, 2),
        "prediction": prediction
    })

if __name__ == "__main__":
    app.run(debug=True)