from flask import Flask, jsonify, request
from flask_cors import CORS
import pickle
import numpy as np
import os
import joblib
import pandas as pd

# Create Flask app
app = Flask(__name__)
CORS(app)

# Define paths for  vectorizer and model 
VECTOR_FILE_PATH = r"C:\Users\jothi\Downloads\vector.pkl"
MODEL_FILE_PATH = r"C:\Users\jothi\Downloads\loan_status_Eligibility_predictor.pkl"

# Load the model 
try:
    model = joblib.load(r"C:\Users\jothi\Downloads\loan_status_Eligibility_predictor.pkl")
    scaler = joblib.load(r"C:\Users\jothi\Downloads\vector.pkl")
except Exception as e:
    print(f"Error loading model or scaler: {e}")
except FileNotFoundError as e:
    raise FileNotFoundError(f"Required file not found: {e}")


# Mock database to store loan applications
loan_applications = {
    1: {
        "Gender": 1,
        "Married": 1,
        "Dependents": 0,
        "Education": 0,
        "Self_Employed": 0,
        "ApplicantIncome": 5000,
        "CoapplicantIncome": 2000,
        "LoanAmount": 150,
        "Loan_Amount_Term": 180,
        "Credit_History": 1.0,
        "Property_Area": 1
    }
}

# Endpoint to get all loan applications
@app.route("/loan_applications/", methods=["GET"])
def get_loan_applications():
    return jsonify({"loan_applications": loan_applications})

# Endpoint to get a specific loan application
@app.route('/loan_applications/<int:application_id>', methods=['GET'])
def get_loan_application(application_id):
    loan_application = loan_applications.get(application_id)
    if loan_application:
        return jsonify({application_id: loan_application}), 200
    else:
        return jsonify({"message": "Loan application not found"}), 404

# Endpoint to add a new loan application
@app.route('/loan_applications/', methods=['POST'])
def add_application():
    new_id = max(loan_applications.keys()) + 1 if loan_applications else 1
    application_data = request.get_json()
    loan_applications[new_id] = application_data
    return jsonify({"message": "Loan application added successfully", "application_id": new_id}), 201

# Endpoint to update a loan application
@app.route('/loan_applications/<int:application_id>', methods=['PUT'])
def update_loan_application(application_id):
    loan_application = loan_applications.get(application_id)
    if loan_application:
        data = request.get_json()
        loan_applications[application_id] = data
        return jsonify({"message": "Loan application updated successfully", "application_id": application_id}), 200
    else:
        return jsonify({"message": "Loan application not found"}), 404

# Endpoint to delete a loan application
@app.route('/loan_applications/<int:application_id>', methods=['DELETE'])
def delete_loan_application(application_id):
    if application_id in loan_applications:
        del loan_applications[application_id]
        return jsonify({"message": "Loan application deleted successfully"}), 200
    else:
        return jsonify({"message": "Loan application not found"}), 404

# Endpoint to predict loan eligibility
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        input_data = pd.DataFrame({
            'Gender': [data['Gender']],
            'Married': [data['Married']],
            'Dependents': [data['Dependents']],
            'Education': [data['Education']],
            'Self_Employed': [data['Self_Employed']],
            'ApplicantIncome': [data['ApplicantIncome']],
            'CoapplicantIncome': [data['CoapplicantIncome']],
            'LoanAmount': [data['LoanAmount']],
            'Loan_Amount_Term': [data['Loan_Amount_Term']],
            'Credit_History': [data['Credit_History']],
            'Property_Area': [data['Property_Area']],
        })

        numeric_cols = ['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term']

        input_data[numeric_cols] = scaler.transform(input_data[numeric_cols])

        prediction = model.predict(input_data)

        result = "Eligible" if prediction[0] == 1 else "Not Eligible"
        return jsonify({"message": "Prediction successful", "eligibility": result})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(debug=True)
