import os
import joblib
import numpy as np
from sklearn.preprocessing import LabelEncoder

def safe_transform(encoder, val):
    try:
        return encoder.transform([val])[0]
    except ValueError:
        print(f"⚠️ Unseen label during transform: {val}")
        return -1  # only safe if your model can handle it


# ✅ Load encoders once, with absolute path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
encoder_path = os.path.join(BASE_DIR, "encoder_label.pkl")

with open(encoder_path, "rb") as f:
    encoders = joblib.load(f)


def decode_value(field_name, value, encoders):
    if not isinstance(encoders, dict):
        raise TypeError(f"[decode_value] encoders is not a dict, got {type(encoders)}")

    encoder = encoders.get(field_name)
    if encoder:
        try:
            return encoder.inverse_transform([int(value)])[0]
        except Exception:
            return value  # fallback instead of "Invalid"
    return value


def preprocess_input(input_data: dict, encoders: dict, feature_order: list) -> list:
    processed = []

    for feature in feature_order:
        raw_value = input_data.get(feature)

        if feature in encoders:
            encoder = encoders[feature]
            value = str(raw_value).strip() if isinstance(raw_value, str) else raw_value

            try:
                encoded_value = encoder.transform([value])[0]
            except ValueError:
                print(f"⚠️ Unseen label during transform: {value}")
                encoded_value = -1  # careful: only valid if model can handle
            processed.append(encoded_value)

        else:
            # numeric fields
            if raw_value in [None, '', 'NaN']:
                processed.append(0.0)
            else:
                try:
                    processed.append(float(raw_value))
                except (ValueError, TypeError):
                    print(f"⚠️ Could not convert {feature}={raw_value} to float. Defaulting to 0.0.")
                    processed.append(0.0)

    return processed
