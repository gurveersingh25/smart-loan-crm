import os
import gdown

FILE_ID = "1rzNdMETYmnJGJWLgZOAErfY_GE6sxUZh"
URL = f"https://drive.google.com/uc?id={FILE_ID}"
OUTPUT_PATH = "app/ml_model/mudra_model.pkl"

if not os.path.exists(OUTPUT_PATH):
    print("Downloading the model from Google Drive...")
    gdown.download(URL, OUTPUT_PATH, quiet=False)
else:
    print("Model file already exists. Skipping download.")
