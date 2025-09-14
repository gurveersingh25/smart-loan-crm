import os
import gdown
import joblib

FILE_ID = "1rzNdMETYmnJGJWLgZOAErfY_GE6sxUZh"
URL = f"https://drive.google.com/uc?id={FILE_ID}"
MODEL_PATH = "app/ml_model/mudra_model.pkl"

def get_model():
    if not os.path.exists(MODEL_PATH):
        os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
        print("Downloading the model from Google Drive...")
        gdown.download(URL, MODEL_PATH, quiet=False)
    return joblib.load(MODEL_PATH)
