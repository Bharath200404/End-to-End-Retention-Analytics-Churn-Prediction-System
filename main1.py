import streamlit as st
import pickle
import pandas as pd

# Load model and columns
model = pickle.load(open("telco_churn/model.pkl", "rb"))
columns = pickle.load(open("telco_churn/columns.pkl", "rb"))

st.set_page_config(page_title="Churn Prediction", layout="centered")

st.title("📊 Customer Churn Prediction System")
st.write("Enter customer details to predict churn")

# Inputs
tenure = st.slider("Tenure (months)", 0, 72, 12)
monthly_charges = st.number_input("Monthly Charges", 0.0, 200.0, 50.0)
senior = st.selectbox("Senior Citizen", [0, 1])
paperless = st.selectbox("Paperless Billing", [0, 1])

# Prepare input
input_dict = {col: 0 for col in columns}

input_dict['tenure'] = tenure
input_dict['MonthlyCharges'] = monthly_charges
input_dict['SeniorCitizen'] = senior
input_dict['PaperlessBilling_Yes'] = paperless

input_df = pd.DataFrame([input_dict])

# Predict
import requests

if st.button("Predict"):
    data = {
        "tenure": tenure,
        "MonthlyCharges": monthly_charges,
        "SeniorCitizen": senior,
        "PaperlessBilling": paperless
    }

    response = requests.post("http://127.0.0.1:5000/predict", json=data)

    result = response.json()

    prob = result["churn_probability"]

    st.write(f"Churn Probability: {prob}")

    if prob > 0.7:
        st.error("⚠️ High Risk of Churn")
    elif prob > 0.4:
        st.warning("⚠️ Medium Risk")
    else:
        st.success("✅ Low Risk")
