import streamlit as st
import pandas as pd
from joblib import load

# Load the pre-trained Random Forest model
#random_forest_model = load('C:/Users/jothi/Downloads/random_forest_model_compressed new/random_forest_model_compressed new')
from joblib import load, Memory

# Use joblib's memory caching feature to optimize loading
memory = Memory(location='cachedir', verbose=0)
random_forest_model = memory.cache(load)(r'C:/Users/jothi/Downloads/random_forest_model_compressed new/random_forest_model_compressed new')

# Now you can use your model as usual

# Streamlit UI for input
st.title("Loan Eligibility Prediction")

# Input fields for the user
person_age = st.number_input("Age", min_value=18, max_value=100, value=30)
person_income = st.number_input("Income", min_value=1000, value=50000)
person_home_ownership = st.selectbox("Home Ownership", ['MORTGAGE', 'RENT', 'OWN', 'OTHER'])
loan_amnt = st.number_input("Loan Amount", min_value=1000, value=10000)
loan_int_rate = st.number_input("Loan Interest Rate", min_value=0.1, max_value=50.0, value=5.0)
loan_grade = st.selectbox("Loan Grade", ['A', 'B', 'C', 'D', 'E', 'F'])
loan_percentage_income = st.number_input("Loan Percentage of Income", min_value=0.0, max_value=1.0, value=0.2)
default_on_file = st.selectbox("Default on File", ['yes', 'no'])
loan_intent = st.selectbox("Loan Intent", ['Personal', 'Business', 'Auto'])
credit_history_length = st.number_input("Credit History Length", min_value=0, max_value=50, value=10)
person_emp_length = st.number_input("Employment Length (years)", min_value=0, max_value=50, value=5)

# Adding missing columns with valid default values
user_input = pd.DataFrame({
    'person_age': [person_age],
    'person_income': [person_income],
    'person_home_ownership': [person_home_ownership],
    'loan_amnt': [loan_amnt],
    'loan_int_rate': [loan_int_rate],
    'loan_grade': [loan_grade],
    'loan_percent_income': [loan_percentage_income],
    'default_on_file': [default_on_file],
    'loan_intent': [loan_intent],
    'credit_history_length': [credit_history_length],
    'person_emp_length': [person_emp_length],
    'cb_person_cred_hist_length': [st.number_input("Credit History Length (0-50)", min_value=0, max_value=50, value=10)],
    'cb_person_default_on_file': [st.selectbox("Has Default on File (yes/no)", ['yes', 'no'])]
})

# Button for prediction
if st.button("Predict"):
    # Make prediction using the loaded model
    random_forest_prediction = random_forest_model.predict(user_input)

    # Display the result
    if random_forest_prediction[0] == 1:
        st.success("You are eligible for the loan!")
    else:
        st.error("You are not eligible for the loan.")
