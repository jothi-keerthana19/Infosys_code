from flask import Flask, jsonify, request, send_file, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import joblib
import pandas as pd
import datetime
import os
import csv
import json
import logging

# App Configuration
app = Flask(__name__)
CORS(app)
app.config['TEMPLATES_AUTO_RELOAD'] = True

logging.basicConfig(level=logging.DEBUG)
# Set up the database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'instance', 'loan_eligibility.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/form')
def form():
    return render_template('form.html')


@app.route('/about')
def about():
    return render_template('about.html')


# Loan Application Model
class LoanApplication(db.Model):
    __tablename__ = "loan_applications"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    gender = db.Column(db.String(50), nullable=False)
    married = db.Column(db.String(50), nullable=False)
    dependents = db.Column(db.String(50), nullable=False)
    education = db.Column(db.String(50), nullable=False)
    self_employed = db.Column(db.String(50), nullable=False)
    applicant_income = db.Column(db.Float, nullable=False)
    coapplicant_income = db.Column(db.Float, nullable=False)
    loan_amount = db.Column(db.Float, nullable=False)
    loan_amount_term = db.Column(db.Float, nullable=False)
    credit_history = db.Column(db.Float, nullable=False)
    property_area = db.Column(db.String(50), nullable=False)
    eligibility = db.Column(db.String(50), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now)


# Load Model and Scaler
model_path = r"C:\Users\jothi\Downloads\loan_status_Eligibility_predictor.pkl"
scaler_path = r"C:\Users\jothi\Downloads\vector.pkl"

try:
    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)
except Exception as e:
    print(f"Error loading model or scaler: {e}")


# Helper Function: Validate Input
def validate_input(data):
    required_fields = [
        'Gender', 'Married', 'Dependents', 'Education', 'Self_Employed',
        'ApplicantIncome', 'CoapplicantIncome', 'LoanAmount',
        'Loan_Amount_Term', 'Credit_History', 'Property_Area'
    ]
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing field: {field}")


# Helper Function to Encode Categorical Values
"""def encode_input(data):
    encoding = {
        'Gender': {'Male': 0, 'Female': 1},
        'Married': {'No': 0, 'Yes': 1},
        'Education': {'Graduate': 0, 'Not Graduate': 1},
        'Self_Employed': {'No': 0, 'Yes': 1},
        'Property_Area': {'Urban': 0, 'Semiurban': 1, 'Rural': 2}
    }
    for key, mapping in encoding.items():
        if key in data:
            data[key] = mapping.get(data[key], -1)  # Default to -1 if not found
    return data"""


# CRUD Operations
@app.route('/loan_applications', methods=['POST'])
def add_loan_application():
    data = request.get_json()
    try:
        validate_input(data)
        new_application = LoanApplication(
            gender=data['Gender'],
            married=data['Married'],
            dependents=data['Dependents'],
            education=data['Education'],
            self_employed=data['Self_Employed'],
            applicant_income=data['ApplicantIncome'],
            coapplicant_income=data['CoapplicantIncome'],
            loan_amount=data['LoanAmount'],
            loan_amount_term=data['Loan_Amount_Term'],
            credit_history=data['Credit_History'],
            property_area=data['Property_Area'],
            eligibility=data.get('Eligibility', 'Pending')
        )
        db.session.add(new_application)
        db.session.commit()
        return jsonify({"message": "Loan application added successfully"}), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/loan_applications', methods=['GET'])
def get_all_applications():
    try:
        applications = LoanApplication.query.all()
        result = [
            {
                "id": app.id,
                "gender": app.gender,
                "married": app.married,
                "dependents": app.dependents,
                "education": app.education,
                "self_employed": app.self_employed,
                "applicant_income": app.applicant_income,
                "coapplicant_income": app.coapplicant_income,
                "loan_amount": app.loan_amount,
                "loan_amount_term": app.loan_amount_term,
                "credit_history": app.credit_history,
                "property_area": app.property_area,
                "eligibility": app.eligibility,
                "timestamp": app.timestamp
            } for app in applications
        ]
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/loan_applications/<int:application_id>', methods=['PUT'])
def update_application(application_id):
    loan_application = LoanApplication.query.get(application_id)
    if loan_application:
        data = request.get_json()
        try:
            for key, value in data.items():
                setattr(loan_application, key.lower(), value)
            db.session.commit()
            return jsonify({"message": "Loan application updated successfully"})
        except Exception as e:
            return jsonify({"error": str(e)}), 400
    else:
        return jsonify({"error": "Loan application not found"}), 404


@app.route('/loan_applications/<int:application_id>', methods=['DELETE'])
def delete_application(application_id):
    loan_application = LoanApplication.query.get(application_id)
    if loan_application:
        db.session.delete(loan_application)
        db.session.commit()
        return jsonify({"message": "Loan application deleted successfully"})
    else:
        return jsonify({"error": "Loan application not found"}), 404


@app.route('/predict/', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        # Encoding mappings for categorical data
        def encode_input(input_data):
            # Encoding mappings
            gender_map = {"Male": 0, "Female": 1}
            married_map = {"Yes": 1, "No": 0}
            education_map = {"Graduate": 1, "Not Graduate": 0}
            self_employed_map = {"Yes": 1, "No": 0}
            property_area_map = {"Urban": 2, "Semiurban": 1, "Rural": 0}

            # Encode values
            encoded_data = {
                'Gender': gender_map[input_data['Gender']],
                'Married': married_map[input_data['Married']],
                'Dependents': int(input_data['Dependents']) if input_data['Dependents'] != "3+" else 3,
                'Education': education_map[input_data['Education']],
                'Self_Employed': self_employed_map[input_data['Self_Employed']],
                'ApplicantIncome': float(input_data['ApplicantIncome']),
                'CoapplicantIncome': float(input_data['CoapplicantIncome']),
                'LoanAmount': float(input_data['LoanAmount']),
                'Loan_Amount_Term': float(input_data['Loan_Amount_Term']),
                'Credit_History': float(input_data['Credit_History']),
                'Property_Area': property_area_map[input_data['Property_Area']]
            }
            return encoded_data

        # Check if `id` is provided in the data
        application_id = data.get('id')
        if application_id:
            # Fetch the existing record by ID
            loan_application = LoanApplication.query.get(application_id)
            if not loan_application:
                return jsonify({"error": f"No loan application found with ID {application_id}"}), 404

            # Update existing data with new values if provided
            for key, value in data.items():
                if hasattr(loan_application, key.lower()) and key != 'id':
                    setattr(loan_application, key.lower(), value)

            # Prepare data for prediction
            prediction_data = {
                'Gender': loan_application.gender,
                'Married': loan_application.married,
                'Dependents': loan_application.dependents,
                'Education': loan_application.education,
                'Self_Employed': loan_application.self_employed,
                'ApplicantIncome': loan_application.applicant_income,
                'CoapplicantIncome': loan_application.coapplicant_income,
                'LoanAmount': loan_application.loan_amount,
                'Loan_Amount_Term': loan_application.loan_amount_term,
                'Credit_History': loan_application.credit_history,
                'Property_Area': loan_application.property_area
            }
            # Encode the fetched data
            prediction_data = encode_input(prediction_data)
        else:
            # Validate input for new data
            validate_input(data)
            prediction_data = encode_input(data)

        # Prepare DataFrame for prediction
        input_data = pd.DataFrame([prediction_data])

        # Scale numeric columns
        numeric_cols = ['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term']
        input_data[numeric_cols] = scaler.transform(input_data[numeric_cols])

        # Make prediction
        prediction = model.predict(input_data)
        eligibility = "Eligible" if prediction[0] == 1 else "Not Eligible"

        if application_id:
            # Update eligibility for existing application
            loan_application.eligibility = eligibility
            db.session.commit()
            return jsonify({"message": f"Prediction updated for ID {application_id}", "eligibility": eligibility}), 200
        else:
            # Save new application with prediction
            new_application = LoanApplication(
                gender=data['Gender'],
                married=data['Married'],
                dependents=data['Dependents'],
                education=data['Education'],
                self_employed=data['Self_Employed'],
                applicant_income=data['ApplicantIncome'],
                coapplicant_income=data['CoapplicantIncome'],
                loan_amount=data['LoanAmount'],
                loan_amount_term=data['Loan_Amount_Term'],
                credit_history=data['Credit_History'],
                property_area=data['Property_Area'],
                eligibility=eligibility
            )
            db.session.add(new_application)
            db.session.commit()
            return jsonify({"message": "Prediction successful for new data", "eligibility": eligibility}), 201
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
    
@app.route('/save_to_csv', methods=['GET'])
def save_to_csv():
    try:
        # Fetch all loan applications from the database
        applications = LoanApplication.query.all()

        # Prepare the data for the CSV
        data = [
            {
                "id": app.id,
                "gender": app.gender,
                "married": app.married,
                "dependents": app.dependents,
                "education": app.education,
                "self_employed": app.self_employed,
                "applicant_income": app.applicant_income,
                "coapplicant_income": app.coapplicant_income,
                "loan_amount": app.loan_amount,
                "loan_amount_term": app.loan_amount_term,
                "credit_history": app.credit_history,
                "property_area": app.property_area,
                "eligibility": app.eligibility,
                "timestamp": app.timestamp
            } for app in applications
        ]
        print("Data to be saved:", data)
        df = pd.DataFrame(data)
        print("DataFrame created:", df.head())
        file_path = os.path.join(basedir, 'static', 'loan_applications_report.csv')
        df.to_csv(file_path, index=False)

        return jsonify({"message": f"Loan applications successfully saved to {file_path}"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

# Run Application
if __name__ == "__main__":
    with app.app_context():
        db.create_all()  
    app.run(debug=True)

