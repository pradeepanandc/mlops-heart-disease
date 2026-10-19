# Heart Disease Prediction — MLOps Assignment Report

## 1. Exploratory Data Analysis (EDA)

### Dataset Overview

The Cleveland Heart Disease dataset contains 303 records and 14 columns, including 13 input features and one target variable. The target was converted into a binary classification variable: 0 represents no heart disease, while 1 represents the presence of heart disease.

### Data Quality

Initial inspection identified six missing values: four in `ca` and two in `thal`. These missing values are handled within the model preprocessing pipeline. Numerical features use median imputation, while categorical features use most-frequent-value imputation.

### Target Distribution

The binary target distribution is:

- No heart disease (0): 164 records (54.13%).
- Heart disease present (1): 139 records (45.87%).

Histograms were generated for age, resting blood pressure (`trestbps`), cholesterol (`chol`), maximum heart rate (`thalach`), and ST depression (`oldpeak`). A correlation heatmap and target-class distribution plot were also generated.

### EDA Conclusion

The dataset was prepared for binary classification with missing-value handling incorporated into the model pipelines. The dataset is relatively small, so evaluation results should be interpreted cautiously.

## 2. System Architecture

The following diagram illustrates the end-to-end MLOps workflow, including data preparation, model training, experiment tracking, API serving, containerization, Kubernetes deployment, CI/CD, and monitoring.

```mermaid
flowchart TD
    A["Cleveland Heart Disease Dataset"] --> B["Data Inspection and EDA"]
    B --> C["Data Cleaning and Preprocessing"]
    C --> D["Model Training and Evaluation"]
    D --> E["MLflow Experiment Tracking"]
    D --> F["Saved Model Pipeline"]
    F --> G["FastAPI Prediction API"]
    G --> H["Docker Image"]
    H --> I["Local Kubernetes Deployment"]
    I --> J["Health and Prediction Endpoints"]
    G --> K["Request Logging and Prometheus Metrics"]
    K --> L["Prometheus"]
    L --> M["Grafana Monitoring Dashboard"]
    N["GitHub Repository"] --> O["GitHub Actions CI/CD"]
    O --> P["Automated Tests and Model Training"]
```

GitHub Actions automates the configured testing and training workflow when the specified repository events occur. The diagram represents the project's component relationships; it does not imply that a public-cloud deployment or automated Kubernetes release has been implemented.

## 3. Model Development and Evaluation

### Models Implemented

Two classifiers were trained and compared:

1. Logistic Regression
2. Random Forest Classifier

The preprocessing pipeline uses median imputation and scaling for numerical features, and most-frequent imputation and one-hot encoding for categorical features. The data was split into training and test sets using an 80:20 stratified split. Five-fold cross-validation was used to compare mean ROC-AUC.

### Model Evaluation Results

| Metric | Logistic Regression | Random Forest |
|---|---:|---:|
| Mean cross-validation ROC-AUC | 0.894 | 0.904 |
| Test accuracy | 0.885 | 0.885 |
| Test precision | 0.839 | 0.818 |
| Test recall | 0.929 | 0.964 |
| Test F1-score | 0.881 | 0.885 |
| Test ROC-AUC | 0.966 | 0.951 |

### Model Selection

Random Forest was selected based on its higher mean cross-validation ROC-AUC of approximately 0.904. It also achieved higher test recall and F1-score than Logistic Regression, although Logistic Regression achieved a higher test ROC-AUC.

The test set contains 61 records; therefore, these metrics should not be interpreted as evidence of clinical suitability.

### Saved Artifacts

- Selected model pipeline: `models/heart_disease_model.joblib`
- Evaluation metrics: `results/model_metrics.json`
- Confusion matrices and ROC curves: `results/`

## 4. Experiment Tracking with MLflow

MLflow was configured with a local SQLite database, `mlflow.db`, and the experiment `heart-disease-classification`.

Separate runs were recorded for Logistic Regression and Random Forest, together with a model-comparison summary. Parameters, evaluation metrics, classification reports, confusion matrices, and ROC curve plots were logged.

Random Forest achieved a mean five-fold cross-validation ROC-AUC of 0.9036, compared with 0.8937 for Logistic Regression. The selected fitted preprocessing and classification pipeline was saved locally as `models/heart_disease_model.joblib`.

**Limitation:** MLflow tracks the experiment parameters, metrics, and supporting artifacts. The fitted model itself is saved locally and is not logged as an MLflow model artifact.

## 5. Prediction API and Automated Testing

### API Implementation

A REST API was implemented using FastAPI and Uvicorn. It loads the saved model pipeline and provides these endpoints:

- `GET /` — returns API information.
- `GET /health` — checks API health and model loading.
- `POST /predict` — accepts 13 input features and returns the predicted class, descriptive label, confidence, and class probabilities.
- `GET /metrics` — exposes Prometheus-compatible application metrics.

Interactive API documentation is available at `/docs`.

### Input Validation

Valid prediction requests returned HTTP 200. Requests containing an invalid age of 150 or a missing required field were rejected with HTTP 422.

### Automated Testing

Five pytest tests passed:

| Test | Result |
|---|---|
| Health endpoint | Passed |
| Root endpoint | Passed |
| Valid prediction | Passed |
| Invalid age rejected | Passed |
| Missing required field rejected | Passed |

Command used:

```powershell
python -m pytest tests/test_api.py -v
```

The test run completed with five passing tests. A dependency deprecation warning was reported but did not cause test failure.

## 6. Docker Packaging

The API was packaged into a Docker image and tested locally. The application image was subsequently rebuilt as `heart-disease-api:1.1` to include the monitoring endpoint.

The Dockerfile installs runtime dependencies, copies the API source and saved model into the image, and starts the service with Uvicorn on port 8000. Runtime dependencies are maintained in `requirements-docker.txt`.

The containerized API was verified using its health endpoint and interactive documentation. The `/predict` endpoint returned a successful prediction response.

## 7. CI/CD and GitHub Actions

A GitHub Actions workflow is configured at `.github/workflows/main.yml`. It runs on pushes and pull requests targeting the `main` branch.

The workflow:

- Checks out the repository.
- Sets up Python 3.11.
- Installs runtime and testing/training dependencies.
- Checks Python syntax.
- Runs the automated API tests.
- Trains and evaluates the models.
- Uploads training results and the saved model as workflow artifacts.

The workflow completed successfully on GitHub. This provides automated validation and training when the configured repository events occur.

**Limitation:** The current workflow does not include a dedicated linting step. The workflow also does not establish that the API image is published to a container registry or automatically deployed to Kubernetes.

## 8. Kubernetes Deployment

The API was deployed to a local Kubernetes environment using the manifests in `k8s/`.

- `k8s/deployment.yaml` defines the API deployment and its health probes.
- `k8s/service.yaml` defines a `LoadBalancer` Service exposing port 8000.
- The deployment uses the locally available image `heart-disease-api:1.1`.

### Deployment Verification

The following results were verified:

- Deployment: one replica available (`1/1`).
- Pod: `1/1 Running`, with zero restarts at the time of verification.
- Service type: `LoadBalancer`.
- Assigned Service IP: `172.18.0.5`.
- API health response: `status: healthy` and `model_loaded: true`.
- Swagger documentation and prediction endpoint: tested successfully.

Direct access to the assigned LoadBalancer IP from Windows was unsuccessful. The verified local access method is port forwarding:

```powershell
kubectl port-forward service/heart-disease-api-service 8001:8000
```

Keep the port-forward terminal running and open:

- API documentation: `http://127.0.0.1:8001/docs`
- Health endpoint: `http://127.0.0.1:8001/health`

This is a local Docker Desktop Kubernetes deployment. No publicly accessible cloud endpoint has been established.

## 9. Monitoring and Logging

The API records request method, endpoint, HTTP status code, and request duration in application logs. It also exposes Prometheus metrics through `GET /metrics`, including request counts and request-duration measurements.

Prometheus and Grafana were started using `monitoring/docker-compose.yml`. Prometheus is configured through `monitoring/prometheus.yml` to scrape the API metrics endpoint.

The Prometheus target was verified as UP. A Grafana data source was configured to use Prometheus, and the **Heart Disease API Monitoring** dashboard was saved with panels for:

- Total API requests.
- Average API request latency.

The monitoring configuration uses `host.docker.internal:8001` as the API target, so the Kubernetes port-forward must be running for the configured scrape target to be reachable.

Screenshots of the monitoring setup are retained in the `screenshots/` directory.

## 10. Evidence and Project Files

The following screenshots provide evidence of exploratory data analysis, API functionality, automated testing, Kubernetes deployment, and monitoring.

### Exploratory Data Analysis

- `screenshots/eda Heart Disease Target Class Distribution.png`
- `screenshots/eda_correlation_heatmap.png`
- `screenshots/eda_numerical_histograms.png`

### API and Testing

- `screenshots/api_metrics_endpoint.png`
- `screenshots/api_tests_passed.png`

### Kubernetes Deployment

- `screenshots/kubernetes_health_check.png`
- `screenshots/kubernetes_swagger_docs.png`
- `screenshots/kubernetes_prediction_success.png`
- `screenshots/kubernetes_loadbalancer_service.png`

### Monitoring

- `screenshots/prometheus_target_health.png`
- `screenshots/grafana_heart_disease_monitoring_dashboard.png`

### CI/CD

- GitHub Actions workflow success screenshot: `screenshots/github_actions_success.png` — pending capture after the final code and documentation push.

The repository also contains the data preparation and training scripts, EDA notebook, saved model, evaluation artifacts, automated tests, Docker configuration, GitHub Actions workflow, Kubernetes manifests, and monitoring configuration.

## 11. Limitations and Conclusion

This project demonstrates an end-to-end MLOps workflow for a heart disease classification task, covering data preparation, EDA, model comparison, MLflow experiment tracking, API implementation, automated testing, Docker packaging, GitHub Actions CI/CD, Kubernetes deployment, and Prometheus/Grafana monitoring.

The dataset is small, and the results are experimental. The model is not clinically validated and must not be used as a substitute for professional medical diagnosis.

The Kubernetes service was verified through port forwarding; an externally accessible cloud endpoint has not been established. The Docker image has been built and tested locally but has not been published to a container registry. Execution in the Prayogshala environment has not yet been verified.

The report and checklist should be checked against the original assignment instructions before submission. The final report must also be exported to the required DOCX or PDF format, and the short end-to-end demonstration video must be recorded if required.
