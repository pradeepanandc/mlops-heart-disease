# MLOps Heart Disease Prediction

## 1. Project Overview

This project implements an end-to-end MLOps workflow for binary heart disease classification using the Cleveland Heart Disease dataset. It covers exploratory data analysis, model training and evaluation, MLflow experiment tracking, a FastAPI prediction service, automated testing, Docker packaging, GitHub Actions CI/CD, Kubernetes deployment, and Prometheus/Grafana monitoring.

## 2. Project Objectives

- Explore and preprocess the dataset.
- Train and compare classification models.
- Track experiments, parameters, metrics, and artifacts using MLflow.
- Package the selected model as a reusable preprocessing and prediction pipeline.
- Implement automated tests and CI/CD.
- Containerize and deploy the prediction API.
- Monitor API requests, latency, and application logs.

## 3. Dataset

The project uses the Cleveland Heart Disease dataset.

- Raw data: `data/raw/processed.cleveland.data`
- Prepared data: `data/processed/heart_disease.csv`
- Records: 303
- Input features: 13
- Original target: converted to binary classification, where `0` means no heart disease and `1` means heart disease present.

Original target values greater than zero are grouped into the positive class. Missing feature values are handled within the model preprocessing pipeline.

## 4. Technology Stack

- Python, pandas, NumPy
- scikit-learn
- Matplotlib and Seaborn
- Jupyter Notebook
- MLflow
- FastAPI and Uvicorn
- pytest and FastAPI TestClient
- Git and GitHub Actions
- Docker
- Kubernetes
- Prometheus and Grafana

## 5. Project Structure

```text
mlops-heart-disease/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── src/
├── tests/
├── models/
├── results/
├── screenshots/
├── docs/
├── k8s/
├── monitoring/
├── .github/workflows/
├── Dockerfile
├── requirements.txt
├── requirements-docker.txt
├── README.md
├── REPORT.md
└── DELIVERABLES.md
```

## 6. Environment Setup

Run commands from the project root in Windows PowerShell.

Activate the existing virtual environment:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the project dependencies:

```powershell
python -m pip install -r requirements.txt
```

Prepare the dataset:

```powershell
python src/prepare_data.py
```

Train and evaluate the models:

```powershell
python src/train_models.py
```

The training script saves the selected model under `models/` and evaluation artifacts under `results/`.

## 7. Model Development Results

Two classification models were evaluated: Logistic Regression and Random Forest.

Random Forest was selected based on its higher mean five-fold cross-validation ROC-AUC.

| Metric | Logistic Regression | Random Forest |
|---|---:|---:|
| Mean CV ROC-AUC | 0.894 | 0.904 |
| Test accuracy | 0.885 | 0.885 |
| Test precision | 0.839 | 0.818 |
| Test recall | 0.929 | 0.964 |
| Test F1-score | 0.881 | 0.885 |
| Test ROC-AUC | 0.966 | 0.951 |

Detailed metrics are available in `results/model_metrics.json` and `REPORT.md`. The test set contains 61 records, so results should be interpreted cautiously.

## 8. MLflow Experiment Tracking

MLflow uses the local SQLite database `mlflow.db` and the experiment `heart-disease-classification`.

The training runs track model parameters, evaluation metrics, classification reports, confusion matrices, and ROC curve plots. The fitted selected pipeline is saved locally as `models/heart_disease_model.joblib`; it is not logged as an MLflow model artifact.

## 9. Prediction API

The FastAPI service loads `models/heart_disease_model.joblib`.

Endpoints:

- `GET /` — API information.
- `GET /health` — health check.
- `POST /predict` — accepts 13 input features and returns a prediction, label, confidence, and class probabilities.
- `GET /metrics` — Prometheus-compatible metrics.

### Run locally

```powershell
.\.venv\Scripts\Activate.ps1
python -m uvicorn src.app:app --reload --host 127.0.0.1 --port 8000
```

Open:

- API documentation: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health
- Metrics: http://127.0.0.1:8000/metrics

### Run automated tests

```powershell
python -m pytest tests/test_api.py -v
```

Five API tests passed, covering the root endpoint, health endpoint, successful prediction, invalid age rejection, and missing required field rejection.

## 10. Docker Packaging

The API is packaged using the root-level `Dockerfile` and `requirements-docker.txt`.

The current Kubernetes deployment uses the local image `heart-disease-api:1.1`.

Build the image when required:

```powershell
docker build -t heart-disease-api:1.1 .
```

Run the container locally, provided port 8000 is available:

```powershell
docker run --rm --name heart-disease-api-container -p 8000:8000 heart-disease-api:1.1
```

Verify the service at http://127.0.0.1:8000/health and test predictions through http://127.0.0.1:8000/docs.

## 11. CI/CD with GitHub Actions

The workflow is defined in `.github/workflows/main.yml` and runs on pushes and pull requests targeting `main`.

It checks out the repository, sets up Python 3.11, installs dependencies, checks Python syntax, runs API tests, trains and evaluates the models, and uploads training artifacts.

The workflow has completed successfully on GitHub. Training artifacts are retained by the workflow for seven days.

## 12. Kubernetes Deployment

Kubernetes manifests are located in `k8s/`:

- `k8s/deployment.yaml` — deployment, container configuration, and health probes.
- `k8s/service.yaml` — NodePort service configuration.

The deployment was verified as running, and the API health check and prediction endpoint were tested through `kubectl port-forward`. The configured NodePort did not work directly through localhost, so port forwarding was used for verification. No externally accessible cloud endpoint has been established.

## 13. Monitoring and Logging

The API logs request method, path, HTTP status, and request duration. Prometheus metrics are exposed through `/metrics`.

Monitoring configuration is located in `monitoring/`:

- `monitoring/docker-compose.yml` starts Prometheus and Grafana.
- `monitoring/prometheus.yml` configures Prometheus to scrape the API.

The Prometheus target was verified as UP. Grafana was connected to Prometheus, and the saved **Heart Disease API Monitoring** dashboard includes panels for total API requests and average API request latency.

See the monitoring screenshots in `screenshots/`.

## 14. Evidence and Documentation

Important evidence files include:

- EDA: `screenshots/eda Heart Disease Target Class Distribution.png`, `screenshots/eda_correlation_heatmap.png`, `screenshots/eda_numerical_histograms.png`
- API: `screenshots/api_health_check.png`, `screenshots/api_prediction_success.png`, `screenshots/api_input_validation_error.png`, `screenshots/api_tests_passed.png`
- Kubernetes: `screenshots/kubernetes_health_check.png`, `screenshots/kubernetes_swagger_docs.png`, `screenshots/kubernetes_prediction_success.png`
- Monitoring: `screenshots/api_metrics_endpoint.png`, `screenshots/prometheus_target_health.png`, `screenshots/grafana_heart_disease_monitoring_dashboard.png`

Other key files include `REPORT.md`, `DELIVERABLES.md`, `docs/progress_log.md`, the training and data preparation scripts, the model, tests, workflow, Dockerfile, Kubernetes manifests, and monitoring configuration.

## 15. Limitations and Conclusion

The project demonstrates a practical MLOps pipeline spanning data preparation, model evaluation, experiment tracking, API development, automated testing, containerization, CI/CD, Kubernetes, and monitoring.

The model is experimental and is not clinically validated. It must not be used as a substitute for professional medical diagnosis. Kubernetes verification was performed through port forwarding; a public cloud deployment and externally accessible endpoint have not been established.
