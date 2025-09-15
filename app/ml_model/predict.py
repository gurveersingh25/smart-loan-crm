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

# Global caches (start empty, load on first use)
_model = None
_model_encoders = None
_feature_order = None


def get_model():
    """Lazy load model + encoders + feature order"""
    global _model, _model_encoders, _feature_order
    if _model is None:
        print("🔹 Loading model into memory...")
        _model = joblib.load(model_path)
        _model_encoders = joblib.load(encoder_path)
        _feature_order = joblib.load(feature_order_path)
    return _model, _model_encoders, _feature_order


def predict_loan_default(input_data: dict):
    print("🔹 RAW input_data:", input_data)

    # Step 1: Lazy load
    model, model_encoders, feature_order = get_model()

    # Step 2: Preprocess input
    processed_input = preprocess_input(input_data, model_encoders, feature_order)
    print("🔹 Processed input for model:", processed_input)

    # Step 3: Predict
    try:
        X_input = pd.DataFrame([processed_input], columns=feature_order)
        prediction = model.predict(X_input)[0]
        probability = model.predict_proba(X_input)[0][1]
    except Exception as e:
        print("❌ Prediction error:", str(e))
        return "Prediction Failed", 0.0, {}

    # Step 4: Decode categorical fields
    decoded_inputs = {}
    for col, val in input_data.items():
        if col in model_encoders:
            encoder = model_encoders[col]
            try:
                if isinstance(val, str):
                    decoded_inputs[col] = val
                else:
                    decoded_inputs[col] = encoder.inverse_transform([val])[0]
            except Exception:
                decoded_inputs[col] = val
        else:
            decoded_inputs[col] = val

    # Step 5: Return results
    label = "Likely to Default" if prediction == 1 else "Not Likely to Default"
    return label, round(probability * 100, 2), decoded_inputs
