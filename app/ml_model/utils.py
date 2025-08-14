import numpy as np
import pickle
from sklearn.preprocessing import LabelEncoder
import joblib
def safe_transform(encoder, val):
    try:
        return encoder.transform([val])[0]
    except ValueError:
        print(f"⚠️ Unseen label during transform: {val}")
        return -1  # or any other dummy value your model can handle



# Load encoders once (on app startup)
with open("app/ml_model/encoder_label.pkl", "rb") as f:

    encoders = joblib.load(f)

def decode_value(field_name, value, encoders):
    if not isinstance(encoders, dict):
        raise TypeError(f"[decode_value] encoders is not a dict, got {type(encoders)}")

    """
    Decode a label-encoded value back to its original string label
    using the stored LabelEncoder from encoder_label.pkl.

    Args:
        field_name (str): The name of the feature column.
        value (int/str): The encoded value.
        encoders (dict): Dictionary of LabelEncoders.

    Returns:
        str: The original string label, or the raw value if decoding not possible.
    """
    
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

            try:
                encoded_value = encoder.transform([value])[0]
            except ValueError:
                print(f"⚠️ Unseen label during transform: {value}")
                encoded_value = -1  # Unseen class
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



