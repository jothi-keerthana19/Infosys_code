import streamlit as st
import pandas as pd
import joblib
from time import sleep
import random

# Load the trained model and scaler
model = joblib.load(r"C:\\Users\\jothi\\Downloads\\loan_status_Eligibility_predictor.pkl")
scaler = joblib.load(r"C:\\Users\\jothi\\Downloads\\vector.pkl")

# Set up the page configuration
st.set_page_config(page_title="Loan Eligibility Predictor", page_icon="🏦", layout="wide")

# Styling for the page
st.markdown(
    """
    <style>
        .title {text-align: center; font-size: 48px; color: #2980B9; font-weight: bold; padding-top: 50px;}
        .subheader {text-align: center; font-size: 24px; color: #2c3e50;}
        .description {font-size: 18px; color: #7f8c8d; text-align: center; margin-bottom: 20px;}
        .result {font-size: 36px; font-weight: bold; color: #444; text-align: center; padding-top: 20px;}
        .approved {color: #4CAF50;}
        .denied {color: #F44336;}
        .stButton button {background-color: #2980B9; color: white; border-radius: 10px; font-size: 18px; padding: 10px 20px;}
        .stButton button:hover {background-color: #3498DB;}
        .section-title {font-size: 24px; color: #333; font-weight: bold; margin-top: 40px; text-align: center;}
        .center-content {display: flex; flex-direction: column; align-items: center; justify-content: center; margin-top: 30px;}
        .navbar {
            display: flex;
            flex-direction: column;
            background-color: #2980B9;
            padding: 15px 0;
            position: sticky;
            top: 0;
            z-index: 10;
        }
        .navbar button {
            background-color: #2980B9;
            color: white;
            font-size: 18px;
            border: none;
            padding: 15px;
            margin: 0 15px;
            border-radius: 5px;
            transition: background-color 0.3s;
        }
        .navbar button:hover {
            background-color: #3498DB;
        }
        .page-home {background-color: #F1F8FF;}
        .page-about {background-color: #FFF3E0;}
        .page-prediction {background-color: #E8F5E9;}
        .banner { 
            background: #f4f4f9; 
            padding: 50px 20px;
            margin-top: 50px;
            text-align: center;
            border-radius: 10px;
        }
        .banner h2 { font-size: 40px; color: #2980B9; }
        .banner p { font-size: 18px; color: #777; margin-top: 10px; }
        .banner ul { text-align: left; list-style-type: square; color: #555; font-size: 16px;}
        .banner ul li { margin-left: 20px; }
        .balloon-burst {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            animation: burst 2s ease-out;
        }
        @keyframes burst {
            0% { transform: translate(-50%, -50%) scale(1); opacity: 1; }
            100% { transform: translate(-50%, -200%) scale(0); opacity: 0; }
        }
        .prediction-loading {
            animation: loading 2s infinite;
        }
        @keyframes loading {
            0% { opacity: 0; }
            50% { opacity: 1; }
            100% { opacity: 0; }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Home Page
def home_page():
    st.markdown('<div class="title">Loan Eligibility Predictor</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="center-content">
            <h1>🏦 Welcome to the Loan Eligibility Predictor</h1>
            <h3>Your One-Stop Solution for Checking Loan Eligibility</h3>
            <p>Find out if you qualify for a loan quickly by entering your details below. Our predictive model will give you an instant decision on your eligibility!</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Centered image with reduced size
    st.image(
        r"D:\Infosys_code\Infosys_code\static\images\newban.webp",
        caption="Powered by advanced machine learning models and seamless user experience.",
        use_container_width=True,
        width=600,
    )


# About Page
def about_page():
    st.markdown('<div class="section-title">About</div>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="center-content">
            <p>Our Loan Eligibility Predictor uses advanced machine learning models to determine whether you're eligible for a loan based on various key factors like income, credit history, and more.</p>
            <p>We believe in simplifying the loan process, and our tool helps you take control of your financial decisions by providing quick and accurate loan eligibility results.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="banner">
            <h2>Why Choose Our Loan Eligibility Predictor?</h2>
            <p>Our machine learning-based predictor quickly analyzes your financial data and predicts your eligibility for loans, saving you time and effort.</p>
            <h2>How It Works</h2>
            <p>Provide basic financial details, and our system instantly determines your loan eligibility.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="banner">
            <h2>What We Analyze</h2>
            <ul>
                <li><strong>Applicant's Income</strong> - Determines the repayment capacity.</li>
                <li><strong>Credit History</strong> - A good credit score can significantly improve your chances of approval.</li>
                <li><strong>Loan Amount</strong> - The total loan amount you're requesting.</li>
                <li><strong>Marital Status</strong> - Married applicants may receive different considerations than single applicants.</li>
                <li><strong>Self-Employment Status</strong> - Self-employed individuals may face different criteria.</li>
                <li><strong>Dependents</strong> - A higher number of dependents can affect eligibility.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )


# Prediction Page
def prediction_page():
    st.markdown('<div class="section-title">Loan Eligibility Prediction</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="subheader">Enter Your Financial Details Below to Check Your Loan Eligibility</div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        gender = st.selectbox("Gender", ["Male", "Female"])
        married = st.selectbox("Marital Status", ["Yes", "No"])
        dependents = st.selectbox("Number of Dependents", ["0", "1", "2", "3+"] )
        education = st.selectbox("Education Level", ["Graduate", "Not Graduate"])

    with col2:
        self_employed = st.selectbox("Self Employed", ["Yes", "No"])
        applicant_income = st.number_input("Applicant Income", min_value=0, step=100)
        coapplicant_income = st.number_input("Coapplicant Income", min_value=0, step=50)
        loan_amount = st.number_input("Loan Amount", min_value=0, step=10)

    loan_term = st.slider("Loan Term (in days)", min_value=60, max_value=360, step=60)
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
        'Property_Area': [1 if property_area == 'Urban' else (2 if property_area == 'Semiurban' else 0)],
    })

    numeric_cols = ['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term']
    input_data[numeric_cols] = scaler.transform(input_data[numeric_cols])

    if st.button("🔍 Predict Eligibility"):
        with st.spinner("Calculating your eligibility..."):
            sleep(2)
            prediction = model.predict(input_data)
            if prediction == 1:
                st.markdown('<div class="result approved prediction-loading">Congratulations! You are eligible for the loan. 🎉</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div class="result denied prediction-loading">Sorry, you are not eligible for the loan. 💔</div>', unsafe_allow_html=True)


# Navigation Sidebar
st.sidebar.title("Navigation")
pages = {
    "Home": home_page,
    "About": about_page,
    "Loan Eligibility Prediction": prediction_page,
}
selection = st.sidebar.radio("Go to", list(pages.keys()))
page = pages[selection]
page()

