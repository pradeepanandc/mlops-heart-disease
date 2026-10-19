
from pathlib import Path
import logging
import time

import joblib
import pandas as pd
from fastapi import FastAPI, Request, Response
from pydantic import BaseModel, Field, ConfigDict
from prometheus_client import (
    Counter,
    Histogram,
    generate_latest,
    CONTENT_TYPE_LATEST,
)

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODEL_PATH = PROJECT_ROOT / "models" / "heart_disease_model.joblib"

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Prometheus metrics
REQUEST_COUNT = Counter(
    "api_requests_total",
    "Total number of API requests",
    ["method", "endpoint", "http_status"],
)

REQUEST_LATENCY = Histogram(
    "api_request_duration_seconds",
    "API request processing time in seconds",
    ["method", "endpoint"],
)

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


# Request logging and monitoring middleware
@app.middleware("http")
async def monitor_requests(request: Request, call_next):
    start_time = time.perf_counter()
    status_code = 500

    try:
        response = await call_next(request)
        status_code = response.status_code
        return response
    except Exception:
        logger.exception(
            "Request failed: %s %s",
            request.method,
            request.url.path,
        )
        raise
    finally:
        duration = time.perf_counter() - start_time

        # Avoid recording the metrics endpoint itself to prevent
        # monitoring scrapes from inflating request metrics.
        if request.url.path != "/metrics":
            REQUEST_COUNT.labels(
                method=request.method,
                endpoint=request.url.path,
                http_status=str(status_code),
            ).inc()

            REQUEST_LATENCY.labels(
                method=request.method,
                endpoint=request.url.path,
            ).observe(duration)

        logger.info(
            "method=%s path=%s status=%s duration_seconds=%.4f",
            request.method,
            request.url.path,
            status_code,
            duration,
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
        "metrics_endpoint": "/metrics",
    }


@app.get("/health")
def health():
    return {"status": "healthy", "model_loaded": True}


@app.get("/metrics", include_in_schema=False)
def metrics():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )


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
            "confidence": round(
                float(probabilities[classes.index(prediction)]), 4
            ),
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
