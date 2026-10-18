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
- [ ] Prepare Kubernetes manifests or Helm charts as required.
- [ ] Deploy the application in the required environment.
- [ ] Verify pod and service status.
- [ ] Test the deployed API.
- [ ] Record deployment instructions and access details.

## 8. Monitoring and Logging
- [ ] Configure application logging.
- [ ] Expose application metrics.
- [ ] Configure Prometheus scraping.
- [ ] Configure Grafana.
- [ ] Create the required monitoring dashboard.
- [ ] Capture screenshots of actual working monitoring components.

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

| Resource | Link | Status |
|---|---|---|
| GitHub repository | To be added | Pending |
| GitHub Actions / Jenkins | To be added | Pending |
| Container registry | To be added | Pending |
| Deployed API | To be added | Pending |
| Monitoring dashboard | To be added if accessible | Pending |
| Pipeline video | To be added | Pending |
| Final report | To be added | Pending |

## Important Notes
- Mark a deliverable complete only after it has been implemented and verified.
- Keep secrets, passwords, access tokens and private credentials out of GitHub.
- Preserve the original dataset and record all preprocessing decisions.
- Verify the final checklist against the assignment's original deliverables before submission.
