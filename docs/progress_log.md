# Project Progress Log

## Project
**MLOps Assignment 01 – Heart Disease Prediction**

## 1. Environment Setup
- Local development environment: Visual Studio Code on Windows.
- Python version: 3.11.9.
- Virtual environment: `.venv`.
- Dependencies installed using `requirements.txt`.
- Docker Desktop and Git configured for local development.

## 2. Dataset Acquisition and Preparation
- Dataset: UCI Heart Disease dataset (Cleveland).
- Original dataset shape: 303 rows × 14 columns.
- Raw files stored under `data/raw/`.
- Created `src/inspect_data.py` to inspect the dataset.
- Created `src/prepare_data.py` to prepare the binary classification dataset.
- Prepared dataset saved as `data/processed/heart_disease.csv`.
- Binary target distribution: 164 records for class 0 and 139 records for class 1.
- Missing values identified: 4 in `ca` and 2 in `thal`.
- Missing values are handled by the model preprocessing pipeline.

## 3. Exploratory Data Analysis
- Created `notebooks/01_eda.ipynb`.
- Inspected descriptive statistics, missing values, and class distribution.
- Generated target class distribution, numerical feature histograms, and a correlation heatmap.
- Saved EDA evidence in `screenshots/`.

## 4. Model Development and Evaluation
- Implemented Logistic Regression and Random Forest classifiers.
- Created preprocessing pipelines with imputation, numerical scaling, and categorical encoding.
- Used an 80:20 stratified train-test split and five-fold cross-validation.
- Selected Random Forest based on its higher mean cross-validation ROC-AUC of approximately 0.904.
- Saved the selected fitted pipeline to `models/heart_disease_model.joblib`.
- Saved evaluation metrics and plots under `results/`.

## 5. Experiment Tracking
- Configured MLflow with a local SQLite database, `mlflow.db`.
- Created the `heart-disease-classification` experiment.
- Logged model parameters, evaluation metrics, classification reports, confusion matrices, and ROC curves.
- Verified successful experiment runs and artifacts in the MLflow UI.
- The fitted model is stored locally; it is not logged as an MLflow model artifact.

## 6. API and Automated Testing
- Implemented a FastAPI prediction service in `src/app.py`.
- Added `/`, `/health`, `/predict`, and `/metrics` endpoints.
- Verified successful prediction responses and input validation.
- Created API tests in `tests/test_api.py`.
- Verified that all five API tests passed.

## 7. Docker Packaging
- Created the root-level `Dockerfile` and `requirements-docker.txt`.
- Built and tested the Docker image locally.
- Rebuilt the image as `heart-disease-api:1.1` to include the metrics endpoint.
- Verified API health and prediction functionality in the container.

## 8. CI/CD
- Configured `.github/workflows/main.yml` for GitHub Actions.
- The workflow checks Python syntax, runs API tests, trains and evaluates models, and uploads training artifacts.
- Verified a successful GitHub Actions workflow run.
- A dedicated linting step has not yet been added.

## 9. Kubernetes Deployment
- Created `k8s/deployment.yaml` and `k8s/service.yaml`.
- Applied the Kubernetes manifests and verified a successful deployment rollout.
- Verified pod readiness and the API health endpoint.
- Tested the prediction endpoint through Swagger documentation.
- Used `kubectl port-forward` for local access because direct localhost NodePort access was unsuccessful.
- Saved Kubernetes evidence in `screenshots/`.
- No public cloud endpoint has been established.

## 10. Monitoring and Logging
- Added request logging and Prometheus-compatible metrics to the API.
- Configured Prometheus scraping in `monitoring/prometheus.yml`.
- Created `monitoring/docker-compose.yml` to run Prometheus and Grafana.
- Verified that the Prometheus API target was UP.
- Configured Grafana with Prometheus as the data source.
- Created the **Heart Disease API Monitoring** dashboard with total-request and average-latency panels.
- Saved monitoring screenshots in `screenshots/`.

## 11. Documentation and Submission
- Updated `README.md` with setup, API, Docker, CI/CD, deployment, and monitoring instructions.
- Updated `REPORT.md` with EDA, model results, experiment tracking, API, CI/CD, deployment, and monitoring details.
- Updated `DELIVERABLES.md` to reflect completed deployment and monitoring work.
- GitHub repository: https://github.com/pradeepanandc/mlops-heart-disease

## 12. Remaining Verification and Submission Tasks
- Review the final Git changes and push all intended project files to GitHub.
- Verify the final repository contents and latest CI/CD run.
- Check the original assignment instructions for any remaining requirements.
- Confirm whether execution in Prayogshala is required and complete it if necessary.
- Record the short end-to-end demonstration video.
- Export the final report to the required DOCX or PDF format if required.
- Verify all screenshots, links, and submission artifacts.

## Execution Environment Evidence
- Local Windows environment: development, testing, and Docker verification completed.
- Local Kubernetes: deployment and prediction verified through port forwarding.
- Prometheus and Grafana: monitoring setup verified locally.
- Prayogshala execution: not yet verified in this progress log.
- Kubernetes Service changed to `LoadBalancer`; assigned IP: `172.18.0.5`.
- Verified deployment status: 1/1 replicas available; pod 1/1 Running with zero restarts.
- Verified API health through port forwarding: `status: healthy`, `model_loaded: true`.
- Direct access to the assigned LoadBalancer IP from Windows was unsuccessful; port forwarding remains the verified local access method.
- No publicly accessible cloud endpoint has been established.
