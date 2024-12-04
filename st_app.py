import streamlit as st
import pandas as pd
import joblib

model = joblib.load(r"C:\Users\jothi\Downloads\loan_status_Eligibility_predictor.pkl")
scaler = joblib.load(r"C:\Users\jothi\Downloads\vector.pkl")

st.set_page_config(page_title="Loan Eligibility Predictor", page_icon="🏦", layout="wide")

st.markdown(
    """
    <style>
        .title {text-align: center; font-size: 48px; color: #4CAF50; font-weight: bold;}
        .subheader {text-align: center; font-size: 20px; color: #777;}
        .result {font-size: 36px; font-weight: bold; color: #444; text-align: center;}
        .approved {color: #4CAF50;}
        .denied {color: #F44336;}
        .stButton button {background-color: #4CAF50; color: white; border-radius: 8px; font-size: 18px;}
        .stButton button:hover {background-color: #45a049;}
    </style>
    <div class="title">🏦 Loan Eligibility Predictor</div>
    <div class="subheader">Check if you qualify for a loan based on your details</div>
    """,
    unsafe_allow_html=True
)

st.sidebar.header("📝 Enter Your Details")

col1, col2 = st.columns(2)

with col1:
    gender = st.selectbox("Gender", ["Male", "Female"])
    married = st.selectbox("Marital Status", ["Yes", "No"])
    dependents = st.selectbox("Number of Dependents", ["0", "1", "2", "3+"])
    education = st.selectbox("Education Level", ["Graduate", "Not Graduate"])

with col2:
    self_employed = st.selectbox("Self Employed", ["Yes", "No"])
    applicant_income = st.number_input("Applicant Income (in thousands)", min_value=0, step=100)
    coapplicant_income = st.number_input("Coapplicant Income (in thousands)", min_value=0, step=50)
    loan_amount = st.number_input("Loan Amount (in thousands)", min_value=0, step=10)

loan_term = st.slider("Loan Term (in days)", min_value=60, max_value=360, step=60, value=180)
credit_history = st.radio("Credit History", [1.0, 0.0], horizontal=True)
property_area = st.selectbox("Property Area", ["Urban", "Rural", "Semiurban"])

input_data = pd.DataFrame({
    'Gender': [1 if gender == 'Male' else 0],
    'Married': [1 if married == 'Yes' else 0],
    'Dependents': [int(dependents.replace("+", ""))],
    'Education': [0 if education == 'Graduate' else 1],
    'Self_Employed': [1 if self_employed == 'Yes' else 0],
    'ApplicantIncome': [applicant_income],
    'CoapplicantIncome': [coapplicant_income],
    'LoanAmount': [loan_amount],
    'Loan_Amount_Term': [loan_term],
    'Credit_History': [credit_history],
    'Property_Area': [1 if property_area == 'Urban' else 0],
})

numeric_cols = ['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term']
input_data[numeric_cols] = scaler.transform(input_data[numeric_cols])

if st.button("🔍 Predict Eligibility"):
    prediction = model.predict(input_data)
    if prediction[0] == 1:
        st.markdown('<div class="result approved">✅ Loan Approved</div>', unsafe_allow_html=True)
    else:
        st.markdown('<div class="result denied">❌ Loan Not Approved</div>', unsafe_allow_html=True)
