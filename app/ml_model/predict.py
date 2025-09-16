# app/ml_model/predict.py
import pandas as pd
import joblib
import numpy as np
import os
from app.ml_model.utils import preprocess_input

# Absolute paths for safe loading
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, 'mudra_model.pkl')
encoder_path = os.path.join(BASE_DIR, 'encoder_label.pkl')
feature_order_path = os.path.join(BASE_DIR, 'feature_order.pkl')

# Load model, encoders, and feature order
model = joblib.load(model_path)
model_encoders = joblib.load(encoder_path)
feature_order = joblib.load(feature_order_path)

encoders = model_encoders  # alias for readability

def predict_loan_default(input_data: dict, model=model, model_encoders=model_encoders, feature_order=feature_order):
    print("🔹 RAW input_data:", input_data)

    # Step 1: Preprocess for prediction
    try:
        processed_input = preprocess_input(input_data, model_encoders, feature_order)
    except Exception as e:
        print("❌ Preprocessing error:", str(e))
        return "Prediction Failed", 0.0, {}
    print("🔹 Processed input for model:", processed_input)

    # Step 2: Predict
    try:
        X_input = pd.DataFrame([processed_input], columns=feature_order)
        for col in ['business','demography','state_of_bank','borrower_city','borrower_state','name_of_bank']:
            val = X_input[col].iloc[0]
            print(f"{col}: {val} -> {encoders[col].inverse_transform([val])[0]}")
        
        print("🔹 X_input values sent to model:")
        print(X_input)
        print("Shape:", X_input.shape)
        prediction = model.predict(X_input)[0]
        probability = model.predict_proba(X_input)[0][1]

        # ===== SHAP-friendly decoded version =====
        categorical_cols = ['business','low_documentation_loan','demography',
                            'state_of_bank','borrower_city','borrower_state','name_of_bank',
                            'revolving_credit_line']

        X_input_decoded = X_input.copy()
        for col in categorical_cols:
            if col in encoders:
                X_input_decoded[col] = X_input_decoded[col].apply(lambda x: encoders[col].inverse_transform([int(x)])[0])
        # =========================================

    except Exception as e:
        print("❌ Prediction error:", str(e))
        return "Prediction Failed", 0.0, {}

    # Step 3: Decode only the categorical fields using the original input
    decoded_inputs = {}
    for col, val in input_data.items():
        if col in model_encoders:
            encoder = model_encoders[col]
            try:
                # If the value is already a string, just pass it
                if isinstance(val, str):
                    decoded_inputs[col] = val
                else:
                    # If numeric, attempt inverse transform safely
                    decoded_inputs[col] = encoder.inverse_transform([val])[0]
            except Exception:
                # Fallback in case inverse_transform fails
                decoded_inputs[col] = val
        else:
            decoded_inputs[col] = val  # No decoding needed

    # Step 4: Return prediction and decoded inputs
    label = "Likely to Default" if prediction == 1 else "Not Likely to Default"
    return label, round(probability * 100, 2), decoded_inputs, X_input_decoded  # Return decoded X_input for SHAP
