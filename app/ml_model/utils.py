# app/ml_model/utils.py
import numpy as np
import joblib

def safe_transform(encoder, val):
    """
    Safely transform a value using LabelEncoder.
    If the value is unseen, fallback to most common class seen during training.
    """
    try:
        return encoder.transform([val])[0]
    except ValueError:
        most_common = encoder.classes_[0]  # fallback to first class from training
        print(f"⚠️ Unseen label during transform: {val}. Using fallback: {most_common}")
        return encoder.transform([most_common])[0]

# Load encoders once (on app startup)
with open("app/ml_model/encoder_label.pkl", "rb") as f:
    encoders = joblib.load(f)

def decode_value(field_name, value, encoders):
    if not isinstance(encoders, dict):
        raise TypeError(f"[decode_value] encoders is not a dict, got {type(encoders)}")

    encoder = encoders.get(field_name)
    if encoder:
        try:
            return encoder.inverse_transform([int(value)])[0]
        except Exception:
            return f"Invalid ({value})"
    return value  # If no encoder for that field, return as is

def preprocess_input(input_data: dict, encoders: dict, feature_order: list) -> list:
    processed = []

    for feature in feature_order:
        raw_value = input_data.get(feature)

        # If the field has an encoder
        if feature in encoders:
            encoder = encoders[feature]
            value = str(raw_value).strip() if isinstance(raw_value, str) else raw_value

            # Fixed: Use safe_transform to handle unseen labels
            encoded_value = safe_transform(encoder, value)
            processed.append(encoded_value)

        else:
            # For numeric fields, handle missing or invalid data
            if raw_value in [None, '', 'NaN']:
                processed.append(0.0)
            else:
                try:
                    processed.append(float(raw_value))
                except (ValueError, TypeError):
                    print(f"⚠️ Could not convert {feature}={raw_value} to float. Defaulting to 0.0.")
                    processed.append(0.0)

    return processed
