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
prob = model.predict_proba(input_df)[0][1]

st.write(f"Churn Probability: {prob:.2f}")

if prob > 0.5:
    st.error("⚠️ Customer is likely to churn")
else:
    st.success("✅ Customer will stay")
