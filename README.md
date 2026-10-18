# MLOps Heart Disease Prediction

## 1. Project Overview

This project develops a machine learning classification system to predict the presence or absence of heart disease using the Cleveland Heart Disease dataset. It applies MLOps practices to support reproducible experiments, model packaging, automated testing, deployment and monitoring.

## 2. Project Objectives

- Explore and preprocess the heart disease dataset.
- Develop and evaluate multiple classification models.
- Track experiments, parameters, metrics and artifacts using MLflow.
- Package the selected model for reusable predictions.
- Implement unit tests and a CI/CD workflow.
- Containerize and deploy the prediction API.
- Monitor API activity and model service performance.

## 3. Dataset

The project uses the Cleveland Heart Disease dataset.

- **Raw data:** `data/raw/processed.cleveland.data`
- **Prepared data:** `data/processed/heart_disease.csv`
- **Original records:** 303
- **Features:** 13 input features and 1 target column
- **Target:** Binary classification, where `0` represents no heart disease and `1` represents heart disease present.

The original target values greater than zero are grouped into the positive class. Missing feature values are handled by the model preprocessing pipeline.

## 4. Technology Stack

Technologies currently used:

- Python
- pandas and NumPy
- scikit-learn
- Matplotlib and Seaborn
- Jupyter Notebook
- MLflow for experiment tracking
- FastAPI and Uvicorn for the prediction API
- pytest and FastAPI TestClient for automated testing
- Git and GitHub

Planned integrations include Docker, CI/CD and monitoring tools.

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
├── requirements.txt
├── README.md
├── REPORT.md
└── DELIVERABLES.md
```

Additional files and folders will be added as the project progresses.

## 6. Environment Setup

Run these commands in the VS Code terminal from the project root.

Activate the existing virtual environment in Windows PowerShell:

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

Train and evaluate the classification models:

```powershell
python src/train_models.py
```

The training script saves the selected model under `models/` and evaluation outputs under `results/`.

## 7. Model Development Results

Two classification models were evaluated:

- Logistic Regression
- Random Forest

Random Forest was selected based on its higher mean five-fold cross-validation ROC-AUC of approximately 0.904, compared with approximately 0.894 for Logistic Regression.

The test accuracy of both models was approximately 88.5%. Detailed evaluation metrics are documented in `REPORT.md` and saved in `results/model_metrics.json`.

These results are preliminary and are based on a test set of 61 records.

## 7A. Prediction API

A REST API was implemented using FastAPI and Uvicorn. It loads the saved preprocessing and classification pipeline from `models/heart_disease_model.joblib`.

Available endpoints:

- `GET /` — API information.
- `GET /health` — checks API health and model loading.
- `POST /predict` — accepts 13 heart-disease input features as JSON and returns a predicted class, label, confidence, and probabilities for both classes.

### Start the API

Activate the virtual environment and run:

```powershell
.\.venv\Scripts\Activate.ps1
python -m uvicorn src.app:app --reload --host 127.0.0.1 --port 8000
```

Open `http://127.0.0.1:8000/docs` to test the API interactively.

### Run Automated Tests

Run the API test suite from the project root:

```powershell
python -m pytest tests/test_api.py -v
```

The initial test run passed all five tests, covering the root endpoint, health endpoint, valid prediction, invalid age rejection, and missing required field rejection.

The prediction is a model estimate for demonstration purposes and is not a medical diagnosis.

## Docker Setup

The prediction API is packaged as a Docker container to provide a reproducible runtime environment.

### Docker Image

- **Image name:** `heart-disease-api`
- **Image tag:** `1.0`
- **Full image name:** `heart-disease-api:1.0`
- **Container port:** `8000`

### Build the Docker Image

Run the following command from the project root directory, where the `Dockerfile` is located:

```bash
docker build -t heart-disease-api:1.0 .
```

### Run the Docker Container

Start the container using:

```bash
docker run -d --name heart-disease-api-container -p 8000:8000 heart-disease-api:1.0
```

### Verify the Container

Check whether the container is running:

```bash
docker ps
```

Open the following URLs in a browser:

- API health check: http://127.0.0.1:8000/health
- API documentation: http://127.0.0.1:8000/docs

Use the interactive API documentation to send a sample JSON request to `POST /predict` and verify that the API returns a successful response.

### Stop the Container

When finished testing, stop the container using:

```bash
docker stop heart-disease-api-container
```

The Docker image is built locally. Publishing it to a container registry and deploying it to a Kubernetes environment remain pending, subject to the assignment requirements.


## 8. Current Progress

- [x] Prepared the Cleveland Heart Disease dataset for binary classification.
- [x] Completed initial exploratory data analysis, including class balance, numerical histograms, and a correlation heatmap.
- [x] Implemented and compared Logistic Regression and Random Forest pipelines.
- [x] Evaluated both models using five-fold cross-validation and test-set classification metrics.
- [x] Selected Random Forest based on mean cross-validation ROC-AUC.
- [x] Saved the selected model pipeline in `models/heart_disease_model.joblib`.
- [x] Saved evaluation metrics and plots under `results/`.
- [x] Configured MLflow experiment tracking using the local SQLite database `mlflow.db`.
- [x] Logged parameters and evaluation metrics for both classifiers.
- [x] Logged classification reports, confusion matrices, and ROC curves as MLflow artifacts.
- [x] Verified successful training runs and Random Forest artifacts in the MLflow UI.
- [x] Implemented the FastAPI prediction API and health endpoint.
- [x] Verified successful predictions and input validation through the API.
- [x] Created and executed five automated API tests; all five passed.

### Next Steps

- [ ] Document API usage and test instructions in the deliverables checklist.
- [ ] Build and test the Docker image.
- [ ] Implement CI/CD using the required workflow.
- [ ] Deploy the application and verify its endpoint.
- [ ] Configure monitoring and logging.
- [ ] Validate the workflow in the Prayogshala environment.
- [ ] Complete the final report, screenshots, and demonstration video.

## 9. Documentation

- `REPORT.md` — EDA, model evaluation and project findings.
- `DELIVERABLES.md` — assignment requirements and completion checklist.
- `docs/progress_log.md` — development progress and execution notes.

## 10. Project Status

The dataset preparation, exploratory data analysis, model development, MLflow experiment tracking, prediction API, and initial automated API tests have been completed and verified. Docker packaging, CI/CD, deployment, monitoring, and Prayogshala execution remain in progress.