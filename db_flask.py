from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import joblib
import pandas as pd
import datetime
import os

app = Flask(__name__)
CORS(app)

# Database Configuration
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'instance', 'loan_eligibility.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)


# Define the LoanApplication Model
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


# Load the model and scaler
try:
    model = joblib.load(r"C:\Users\jothi\Downloads\loan_status_Eligibility_predictor.pkl")
    scaler = joblib.load(r"C:\Users\jothi\Downloads\vector.pkl")
except Exception as e:
    print(f"Error loading model or scaler: {e}")


# Prediction Route
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Parse the input JSON
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

        # Scale numeric columns
        numeric_cols = ['ApplicantIncome', 'CoapplicantIncome', 'LoanAmount', 'Loan_Amount_Term']
        input_data[numeric_cols] = scaler.transform(input_data[numeric_cols])

        # Make prediction
        prediction = model.predict(input_data)
        eligibility = "Eligible" if prediction[0] == 1 else "Not Eligible"

        # Save to the database
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

        return jsonify({
            "message": "Prediction successful",
            "eligibility": eligibility,
            "application_id": new_application.id
        })
    except Exception as e:
        return jsonify({"error": str(e)})


# Route to Get All Applications
@app.route('/applications', methods=['GET'])
def get_applications():
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


# Update an existing loan application
@app.route('/loan_applications/<int:application_id>', methods=['PUT'])
def update_loan_application(application_id):
    loan_application = LoanApplication.query.get(application_id)
    if loan_application:
        data = request.get_json()
        loan_application.gender = data['Gender']
        loan_application.married = data['Married']
        loan_application.dependents = data['Dependents']
        loan_application.education = data['Education']
        loan_application.self_employed = data['Self_Employed']
        loan_application.applicant_income = data['ApplicantIncome']
        loan_application.coapplicant_income = data['CoapplicantIncome']
        loan_application.loan_amount = data['LoanAmount']
        loan_application.loan_amount_term = data['Loan_Amount_Term']
        loan_application.credit_history = data['Credit_History']
        loan_application.property_area = data['Property_Area']
        db.session.commit()
        return jsonify({"message": "Loan application updated successfully"})
    else:
        return jsonify({"error": "Loan application not found"}), 404


# Delete an existing loan application
@app.route('/loan_applications/<int:application_id>', methods=['DELETE'])
def delete_loan_application(application_id):
    loan_application = LoanApplication.query.get(application_id)
    if loan_application:
        db.session.delete(loan_application)
        db.session.commit()
        return jsonify({"message": "Loan application deleted successfully"})
    else:
        return jsonify({"error": "Loan application not found"}), 404

if __name__ == '__main__':

    app.run(debug=True)
