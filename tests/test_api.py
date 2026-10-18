
from fastapi.testclient import TestClient

from src.app import app

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
    assert response.json()["model_loaded"] is True


def test_root_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["prediction_endpoint"] == "/predict"


def test_valid_prediction():
    payload = {
        "age": 55,
        "sex": 1,
        "cp": 2,
        "trestbps": 130,
        "chol": 250,
        "fbs": 0,
        "restecg": 1,
        "thalach": 150,
        "exang": 0,
        "oldpeak": 1.0,
        "slope": 2,
        "ca": 0,
        "thal": 3,
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 200

    result = response.json()
    assert result["prediction"] in [0, 1]
    assert result["label"] in [
        "heart_disease_present",
        "heart_disease_not_detected",
    ]
    assert 0 <= result["confidence"] <= 1
    assert 0 <= result["probability_heart_disease"] <= 1
    assert 0 <= result["probability_no_heart_disease"] <= 1

    probability_sum = (
        result["probability_heart_disease"]
        + result["probability_no_heart_disease"]
    )
    assert abs(probability_sum - 1.0) < 0.001


def test_invalid_age_is_rejected():
    payload = {
        "age": 150,
        "sex": 1,
        "cp": 2,
        "trestbps": 130,
        "chol": 250,
        "fbs": 0,
        "restecg": 1,
        "thalach": 150,
        "exang": 0,
        "oldpeak": 1.0,
        "slope": 2,
        "ca": 0,
        "thal": 3,
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 422


def test_missing_required_field_is_rejected():
    payload = {
        "age": 55,
        "sex": 1,
        "cp": 2,
        "trestbps": 130,
        "chol": 250,
        "fbs": 0,
        "restecg": 1,
        "thalach": 150,
        "exang": 0,
        "oldpeak": 1.0,
        "slope": 2,
        "ca": 0,
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 422
