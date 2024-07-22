from flask import Flask, request, render_template
import joblib
import pandas as pd

app = Flask(__name__)

# Load the model and scaler
model = joblib.load('GradientBoostingClassifier_best_model.pkl')
scaler = joblib.load('scaler.pkl')

# Define the order of features used during training
features_order = [
    'no_of_dependents', 'education', 'self_employed', 'income_annum', 
    'loan_amount', 'loan_term', 'cibil_score', 'residential_assets_value', 
    'commercial_assets_value', 'luxury_assets_value', 'bank_asset_value'
]

# Define simple mappings
education_mapping = {'Graduate': 0, 'Not Graduate': 1}
self_employed_mapping = {'Yes': 0, 'No': 1}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Extract input values from form
        no_of_dependents = int(request.form['no_of_dependents'])
        education = request.form['education']
        self_employed = request.form['self_employed']
        income_annum = float(request.form['income_annum'])
        loan_amount = float(request.form['loan_amount'])
        loan_term = int(request.form['loan_term'])
        cibil_score = float(request.form['cibil_score'])
        residential_assets_value = float(request.form['residential_assets_value'])
        commercial_assets_value = float(request.form['commercial_assets_value'])
        luxury_assets_value = float(request.form['luxury_assets_value'])
        bank_asset_value = float(request.form['bank_asset_value'])
        
        # Encode categorical variables using simple mappings
        education_encoded = education_mapping.get(education, -1)
        self_employed_encoded = self_employed_mapping.get(self_employed, -1)
        
        # Handle invalid inputs
        if education_encoded == -1 or self_employed_encoded == -1:
            return "Invalid input value for education or self-employed."
        
        # Create DataFrame for prediction with the correct column order
        input_data = pd.DataFrame([[
            no_of_dependents, education_encoded, self_employed_encoded, income_annum, 
            loan_amount, loan_term, cibil_score, residential_assets_value, 
            commercial_assets_value, luxury_assets_value, bank_asset_value
        ]], columns=features_order)
        
        # Extract numerical features for scaling
        numerical_features = [
            'no_of_dependents', 'income_annum', 'loan_amount', 'loan_term', 
            'cibil_score', 'residential_assets_value', 'commercial_assets_value', 
            'luxury_assets_value', 'bank_asset_value'
        ]
        
        # Scale numerical features
        input_data[numerical_features] = scaler.transform(input_data[numerical_features])
        
        # Predict using the trained model
        prediction = model.predict(input_data)
        
        # Return the result
        result = "Congratulations! Based on the information provided, your loan will be approved." if prediction[0] == 0 else "We're sorry, but based on the information provided, your loan application will be rejected."
        return render_template('result.html', result=result)
    
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
