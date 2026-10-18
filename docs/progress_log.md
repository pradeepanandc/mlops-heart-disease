# Project Progress Log

## Project
**MLOps Assignment 01 – Heart Disease Prediction**

## Environment Setup
- Local development environment: Visual Studio Code on Windows.
- Python version: 3.11.9.
- Virtual environment: `.venv`.
- Dependencies installed using `requirements.txt`.

## Dataset Acquisition
- Dataset: UCI Heart Disease dataset (Cleveland).
- Original dataset shape: 303 rows × 14 columns.
- Raw files stored under `data/raw/`.

## Data Inspection
- Created `src/inspect_data.py`.
- Inspected column names, data types, missing values and target distribution.
- Missing values identified: 6 (4 in `ca`, 2 in `thal`).

## Data Preparation
- Created `src/prepare_data.py`.
- Generated `data/processed/heart_disease.csv`.
- Prepared dataset shape: 303 rows × 14 columns.
- Binary target distribution:
  - Target 0: 164 records.
  - Target 1: 139 records.

**Note:** The six missing values remain in the current prepared dataset and require a documented preprocessing decision before model training.

## Exploratory Data Analysis
- Created `notebooks/01_eda.ipynb`.
- Inspected descriptive statistics and missing values.
- Generated the target class distribution chart.
- Further EDA visualizations are pending.

## Next Steps
1. Complete EDA visualizations.
2. Finalize missing-value handling and feature preprocessing.
3. Train and evaluate at least two classification models.
4. Integrate experiment tracking.
5. Package the model and develop automated tests.
6. Implement CI/CD, containerization, deployment and monitoring.
7. Complete the final report and submission evidence.

## Execution Environment Evidence
- Local setup and initial EDA completed.
- Prayogshala execution and deployment evidence: pending.
