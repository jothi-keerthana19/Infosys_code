from flask import Flask, jsonify, request
from flask_cors import CORS

# Create the Flask app
app = Flask(__name__)
CORS(app)

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

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Loan Application API!"})


# CREATE - Add a new loan application
@app.route('/loan_applications/', methods=['POST'])
def add_application():
    if not request.is_json:
        return jsonify({"error": "Invalid data format. JSON expected."}), 400

    application_data = request.get_json()
    new_id = max(loan_applications.keys()) + 1 if loan_applications else 1
    loan_applications[new_id] = application_data

    return jsonify({"message": "Loan application added successfully", "application_id": new_id}), 201


# READ - Get the list of all loan applications
@app.route('/loan_applications/', methods=['GET'])
def get_loan_applications():
    return jsonify({"loan_applications": loan_applications})


# READ - Get a specific loan application
@app.route('/loan_applications/<int:application_id>', methods=['GET'])
def get_loan_application(application_id):
    loan_application = loan_applications.get(application_id)
    if loan_application:
        return jsonify({application_id: loan_application}), 200
    else:
        return jsonify({"message": "Loan application not found"}), 404


# UPDATE - Update an existing loan application
@app.route('/loan_applications/<int:application_id>', methods=['PUT'])
def update_loan_application(application_id):
    if application_id not in loan_applications:
        return jsonify({"message": "Loan application not found"}), 404

    data = request.get_json()

    if not isinstance(data, dict):
        return jsonify({"message": "Invalid data format"}), 400
    loan_applications[application_id].update(data)

    return jsonify({
        "message": "Loan application updated successfully",
        "application": loan_applications[application_id]
    }), 200


# DELETE - Delete a loan application
@app.route('/loan_applications/<int:application_id>', methods=['DELETE'])
def delete_loan_application(application_id):
    if application_id in loan_applications:
        del loan_applications[application_id]
        return jsonify({"message": "Loan application deleted successfully"}), 200
    else:
        return jsonify({"message": "Loan application not found"}), 404


# Run the application
if __name__ == '__main__':
    app.run(debug=True)
