# MLOps Assignment 01 — Deliverables Checklist

## Project
**Heart Disease Prediction — End-to-End MLOps Pipeline**

Status key:
- [ ] Not completed
- [x] Completed and verified

## 1. Dataset and Exploratory Data Analysis
- [x] Obtain the Cleveland Heart Disease dataset.
- [x] Inspect dataset structure, data types and target distribution.
- [x] Identify missing values.
- [x] Prepare a binary classification target.
- [x] Generate the prepared dataset CSV.
- [x] Inspect descriptive statistics.
- [x] Generate the target class distribution chart.
- [x] Generate numerical feature histograms.
- [x] Generate a correlation heatmap.
- [x] Document EDA findings and preprocessing decisions.

## 2. Model Development and Evaluation
- [x] Define the training and testing strategy.
- [x] Build reproducible preprocessing pipelines.
- [x] Train at least two classification models.
- [x] Evaluate models using appropriate classification metrics.
- [x] Compare model performance and select a model.
- [x] Save the selected model and preprocessing pipeline.
- [x] Document modelling decisions and results.

## 3. Experiment Tracking
- [x] Set up MLflow tracking using a local SQLite database (`mlflow.db`).
- [x] Log model parameters and evaluation metrics for both classifiers.
- [x] Log relevant artifacts, including classification reports, confusion matrices and ROC curves.
- [x] Save the selected model as models/heart_disease_model.joblib.
- [x] Capture experiment evidence by verifying successful runs and artifacts in the MLflow UI.

## 4. API and Automated Testing
- [x] Implement a prediction API.
- [x] Validate input data and prediction responses.
- [x] Create unit tests.
- [x] Run tests and record results.
- [x] Document API usage and test instructions.

## 5. Docker and Reproducible Packaging

- [x] Create the Dockerfile.
- [x] Build the Docker image.
- [x] Run the Docker container locally and verify the API prediction endpoint.
- [x] Document the Docker image name, tag, build and run instructions in README.md.
- [ ] Publish the image to the required registry, if applicable.

## 6. CI/CD
- [x] Create the required GitHub Actions workflow or Jenkins pipeline.
- [x] Automate relevant testing and build steps.
- [x] Execute the workflow and verify its result.
- [x] Record the workflow URL and evidence.

## 7. Deployment

- [x] Prepare Kubernetes deployment and service manifests.
- [x] Deploy the application to the local Kubernetes environment.
- [x] Verify pod readiness and service status.
- [x] Test the deployed API health and prediction endpoints.
- [x] Record deployment instructions and local access details.

**Evidence:** `k8s/deployment.yaml`, `k8s/service.yaml`, `screenshots/kubernetes_health_check.png`, `screenshots/kubernetes_swagger_docs.png`, `screenshots/kubernetes_prediction_success.png`.

**Access method:** `kubectl port-forward service/heart-disease-api-service 8001:8000`, followed by `http://127.0.0.1:8001/docs`.

**Limitation:** Direct access through the configured NodePort on localhost was unsuccessful. The API was verified using port forwarding; no public cloud endpoint has been established.


## 8. Monitoring and Logging

- [x] Configure application request logging.
- [x] Expose Prometheus-compatible API metrics at `/metrics`.
- [x] Configure Prometheus scraping through `monitoring/prometheus.yml`.
- [x] Configure Grafana with Prometheus as its data source.
- [x] Create and save the monitoring dashboard.
- [x] Capture screenshots of the monitoring components.

**Evidence:**
- `monitoring/docker-compose.yml`
- `monitoring/prometheus.yml`
- `screenshots/api_metrics_endpoint.png`
- `screenshots/prometheus_target_health.png`
- `screenshots/grafana_heart_disease_monitoring_dashboard.png`

The Grafana dashboard contains panels for total API requests and average API request latency. The Prometheus target was verified as UP.


## 9. Prayogshala Execution and Evidence
- [ ] Clone or transfer the project into the correct Prayogshala workspace.
- [ ] Verify dependencies and environment configuration.
- [ ] Execute the required workflow in Prayogshala.
- [ ] Capture relevant screenshots in the workspace.
- [ ] Record any environment-specific changes and results.

## 10. Documentation and Submission
- [x] Complete README setup and execution instructions.
- [ ] Maintain the project progress log.
- [ ] Complete the final assignment report.
- [ ] Include the GitHub repository URL.
- [ ] Include actual workflow, registry and deployment links where applicable.
- [ ] Include API access details or local testing instructions.
- [ ] Include architecture diagram and required screenshots.
- [ ] Record the short end-to-end pipeline video.
- [ ] Produce the required final report in DOC/DOCX/PDF format.
- [ ] Verify all required deliverables against the original assignment instructions.

## Links Register

| Resource | Link or Access Details | Status |
|---|---|---|
| GitHub repository | https://github.com/pradeepanandc/mlops-heart-disease | Available |
| GitHub Actions | Open the repository → Actions → select the successful Heart Disease MLOps CI run | Verified; add the specific run URL if required |
| Container registry | Not published | Not applicable unless required |
| Deployed API | Local Kubernetes: `kubectl port-forward service/heart-disease-api-service 8001:8000`, then open `http://127.0.0.1:8001/docs` | Verified locally |
| Monitoring dashboard | `http://localhost:3000` when Grafana is running | Verified locally |
| Prometheus | `http://localhost:9090` when Prometheus is running | Target verified UP |
| Pipeline video | Not yet recorded | Pending |
| Final report | `REPORT.md` | Markdown report updated; export format to verify |

## Important Notes
- Mark a deliverable complete only after it has been implemented and verified.
- Keep secrets, passwords, access tokens and private credentials out of GitHub.
- Preserve the original dataset and record all preprocessing decisions.
- Verify the final checklist against the assignment's original deliverables before submission.
