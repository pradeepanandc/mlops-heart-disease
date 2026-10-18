## Exploratory Data Analysis (EDA)

### Dataset Overview
The Cleveland Heart Disease dataset contains 303 records and 14 columns, including 13 input features and one target variable.

### Data Quality
Initial inspection identified six missing values:
- `ca`: 4 missing values
- `thal`: 2 missing values

These missing values remain in the current prepared dataset. A suitable imputation strategy must be incorporated into the model preprocessing pipeline.

### Target Distribution
The binary target distribution is:
- No heart disease (0): 164 records (54.13%)
- Heart disease present (1): 139 records (45.87%)

The classes are reasonably balanced, so both classes can be represented during model training and evaluation.

### Numerical Feature Distributions
Histograms were generated for age, resting blood pressure (`trestbps`), cholesterol (`chol`), maximum heart rate (`thalach`), and ST depression (`oldpeak`).

The plots indicate variation in the numerical features. Cholesterol and resting blood pressure contain some unusually high observations, while `oldpeak` has a right-skewed distribution with many values close to zero. These observations will be considered when evaluating preprocessing and model performance.

### Correlation Analysis
A correlation heatmap was generated to examine relationships among the numerical features and the target variable. Specific correlation findings will be recorded after reviewing the heatmap.

### EDA Conclusion
The dataset is suitable for proceeding to binary classification experiments, subject to appropriate missing-value handling, feature preprocessing, reproducible train-test splitting, and evaluation using suitable classification metrics.
## Model Development and Evaluation

### Models Implemented

Two classification algorithms were trained and compared using the prepared Cleveland Heart Disease dataset:

1. **Logistic Regression**
2. **Random Forest Classifier**

Both models use preprocessing pipelines that handle missing numerical values with median imputation, scale numerical features, impute missing categorical values using the most frequent value, and one-hot encode categorical features.

The dataset was split into training and test sets using an 80:20 ratio, with stratification to preserve the target-class proportions. Five-fold cross-validation was used to compare the models using ROC-AUC.

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

Random Forest was selected as the final model because it achieved the higher mean cross-validation ROC-AUC of approximately 0.904. It also achieved a higher test recall and F1-score than Logistic Regression. However, Logistic Regression achieved a higher test ROC-AUC.

The evaluation uses a relatively small test set of 61 records. Therefore, the results should be interpreted cautiously and do not establish clinical suitability.

### Saved Artifacts

- Selected model pipeline: `models/heart_disease_model.joblib`
- Evaluation metrics: `results/model_metrics.json`
- Confusion matrices and ROC curves: `results/`

The selected model and evaluation artifacts were used for experiment tracking with MLflow. The saved model pipeline has also been integrated into the FastAPI prediction service, and the initial automated API test suite has passed. Docker packaging, CI/CD, and deployment remain future stages.


## Experiment Tracking with MLflow

### Configuration

MLflow was configured to track experiments using a local SQLite database named `mlflow.db`. A dedicated experiment, `heart-disease-classification`, was created to organize the training runs.

### Tracked Experiments and Artifacts

Separate MLflow runs were recorded for Logistic Regression and Random Forest, along with a model-comparison summary. The training script logged model parameters, evaluation metrics, and supporting artifacts.

The logged artifacts include:
- Classification reports in JSON format.
- Confusion matrix plots.
- ROC curve plots.
- A model-comparison summary containing evaluation metrics and the ROC curve comparison.

The successful runs and Random Forest artifacts were verified using the MLflow user interface.

### Results and Model Selection

Random Forest achieved a mean five-fold cross-validation ROC-AUC of **0.9036**, compared with **0.8937** for Logistic Regression. Based on the mean cross-validation ROC-AUC, Random Forest was selected as the final model.

Its test-set results were:
- Accuracy: 88.52%
- Precision: 81.82%
- Recall: 96.43%
- F1-score: 88.52%
- ROC-AUC: 95.13%

### Model Storage

The selected fitted preprocessing and classification pipeline was saved locally as `models/heart_disease_model.joblib`. MLflow currently tracks experiment parameters, metrics, and artifacts; the fitted model itself is not logged as an MLflow model artifact.

### Evidence

Screenshots of the MLflow training runs, Random Forest metrics, classification report, confusion matrix, and ROC curve should be included in the final submission.

## Prediction API and Automated Testing

### Docker Packaging and Verification

The prediction API was packaged using Docker to provide a reproducible runtime environment. A Docker image named `heart-disease-api:1.0` was built successfully using the project Dockerfile and the dependencies specified in `requirements-docker.txt`.

The container was started with port 8000 mapped to port 8000 on the host machine. The API was accessed through the container using the health-check endpoint and the interactive API documentation at `/docs`.

A sample request to the `/predict` endpoint returned **HTTP 200**, confirming that the containerized API processed the request successfully and returned a prediction with confidence and class-probability values.

The Docker image was built and tested locally. Container registry publishing and Kubernetes deployment remain pending.

### API Implementation

A REST API was implemented using FastAPI and Uvicorn. The application loads the saved preprocessing and classification pipeline from `models/heart_disease_model.joblib`.

The API exposes the following endpoints:

- `GET /` — returns API information.
- `GET /health` — checks the API health and whether the model is loaded.
- `POST /predict` — accepts 13 heart-disease input features as JSON and returns the predicted class, descriptive label, confidence, and probabilities for both classes.

The API was started locally using Uvicorn and tested through the interactive Swagger documentation at `/docs`.

### Input Validation

The API validates incoming prediction requests. A valid sample request returned HTTP 200 with a prediction and probability values. An invalid age of 150 and a request missing a required field were both rejected with HTTP 422.

### Automated Testing

Automated tests were created using pytest and FastAPI's TestClient. Five tests were executed:

| Test | Result |
|---|---|
| Health endpoint | Passed |
| Root endpoint | Passed |
| Valid prediction | Passed |
| Invalid age rejected | Passed |
| Missing required field rejected | Passed |

The test command was:

`python -m pytest tests/test_api.py -v`

The test run completed with **5 passed tests in 23.63 seconds**. One dependency deprecation warning was reported, but it did not affect the test results.

### Evidence

The following screenshots should be retained for the final submission:

- `screenshots/api_health_check.png`
- `screenshots/api_prediction_success.png`
- `screenshots/api_input_validation_error.png`
- `screenshots/api_tests_passed.png`

These screenshots provide evidence of API health, successful prediction, input validation, and automated test execution.

### Limitations

The API and automated tests have been verified locally. Docker packaging, CI/CD, deployment, monitoring, and execution in the Prayogshala environment remain to be completed. The model's predictions are experimental and should not be interpreted as medical diagnoses.