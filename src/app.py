
from pathlib import Path
import logging

import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field, ConfigDict


# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = PROJECT_ROOT / "models" / "heart_disease_model.joblib"

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the trained preprocessing + classification pipeline
if not MODEL_PATH.exists():
    raise FileNotFoundError(
        f"Model file not found: {MODEL_PATH}. "
        "Run src/train_models.py first."
    )

model = joblib.load(MODEL_PATH)

app = FastAPI(
    title="Heart Disease Prediction API",
    description=(
        "Predicts the presence of heart disease using "
        "a trained machine-learning pipeline."
    ),
    version="1.0.0",
)


class HeartDiseaseInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    age: float = Field(ge=1, le=120)
    sex: int = Field(ge=0, le=1)
    cp: int = Field(ge=1, le=4)
    trestbps: float = Field(gt=0, le=300)
    chol: float = Field(gt=0, le=700)
    fbs: int = Field(ge=0, le=1)
    restecg: int = Field(ge=0, le=2)
    thalach: float = Field(gt=0, le=300)
    exang: int = Field(ge=0, le=1)
    oldpeak: float = Field(ge=-10, le=20)
    slope: int = Field(ge=1, le=3)
    ca: int = Field(ge=0, le=3)
    thal: int = Field(ge=3, le=7)


@app.get("/")
def root():
    return {
        "message": "Heart Disease Prediction API is running",
        "docs": "/docs",
        "prediction_endpoint": "/predict",
    }


@app.get("/health")
def health():
    return {"status": "healthy", "model_loaded": True}


@app.post("/predict")
def predict(data: HeartDiseaseInput):
    try:
        input_df = pd.DataFrame([data.model_dump()])

        # The saved pipeline performs preprocessing automatically.
        prediction = int(model.predict(input_df)[0])

        probabilities = model.predict_proba(input_df)[0]
        classes = list(model.classes_)
        positive_index = classes.index(1)
        negative_index = classes.index(0)

        heart_disease_probability = float(probabilities[positive_index])
        no_heart_disease_probability = float(probabilities[negative_index])

        result = {
            "prediction": prediction,
            "label": (
                "heart_disease_present"
                if prediction == 1
                else "heart_disease_not_detected"
            ),
            "confidence": round(float(probabilities[classes.index(prediction)]), 4),
            "probability_heart_disease": round(
                heart_disease_probability, 4
            ),
            "probability_no_heart_disease": round(
                no_heart_disease_probability, 4
            ),
        }

        logger.info("Prediction request processed successfully")
        return result

    except Exception:
        logger.exception("Prediction request failed")
        raise
