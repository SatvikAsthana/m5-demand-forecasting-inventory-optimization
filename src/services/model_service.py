import joblib
import os

MODEL_PATH = "models/lgbm_model.pkl"

def load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(
            "Trained model not found. Run model training first."
        )
    
    model = joblib.load(MODEL_PATH)
    return model
