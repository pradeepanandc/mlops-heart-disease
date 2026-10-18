
from pathlib import Path
import json

import joblib
import pandas as pd
import matplotlib.pyplot as plt
import mlflow
import mlflow.sklearn

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    classification_report,
    ConfusionMatrixDisplay,
    RocCurveDisplay,
)

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "processed" / "heart_disease.csv"
MODEL_DIR = PROJECT_ROOT / "models"
RESULTS_DIR = PROJECT_ROOT / "results"
MLFLOW_DIR = PROJECT_ROOT / "mlruns"

NUMERIC_FEATURES = ["age", "trestbps", "chol", "thalach", "oldpeak"]
CATEGORICAL_FEATURES = [
    "sex", "cp", "fbs", "restecg", "exang",
    "slope", "ca", "thal"
]


def build_preprocessor():
    numeric_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])

    categorical_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore")),
    ])

    return ColumnTransformer([
        ("numeric", numeric_pipeline, NUMERIC_FEATURES),
        ("categorical", categorical_pipeline, CATEGORICAL_FEATURES),
    ])


def main():
    df = pd.read_csv(DATA_PATH)

    X = df[NUMERIC_FEATURES + CATEGORICAL_FEATURES]
    y = df["target"].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y,
    )

    models = {
        "logistic_regression": LogisticRegression(
            max_iter=2000,
            random_state=42,
        ),
        "random_forest": RandomForestClassifier(
            n_estimators=300,
            min_samples_leaf=2,
            random_state=42,
            class_weight="balanced",
        ),
    }

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    MLFLOW_DIR.mkdir(parents=True, exist_ok=True)

    # Configure local MLflow experiment tracking.
    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    mlflow.set_experiment("heart-disease-classification")

    results = {}
    fitted_pipelines = {}

    for name, estimator in models.items():
        with mlflow.start_run(run_name=name):
            print(f"\nTraining {name}...")

            # Record model parameters.
            mlflow.log_params(estimator.get_params())
            mlflow.set_tag("model_name", name)
            mlflow.set_tag("dataset", "Cleveland Heart Disease")
            mlflow.set_tag("selection_metric", "cv_roc_auc_mean")

            pipeline = Pipeline([
                ("preprocessor", build_preprocessor()),
                ("model", estimator),
            ])

            # Cross-validation uses training data only.
            cv_scores = cross_val_score(
                pipeline,
                X_train,
                y_train,
                cv=5,
                scoring="roc_auc",
            )

            # Fit and evaluate on the held-out test set.
            pipeline.fit(X_train, y_train)
            predictions = pipeline.predict(X_test)
            probabilities = pipeline.predict_proba(X_test)[:, 1]

            metrics = {
                "cv_roc_auc_mean": float(cv_scores.mean()),
                "cv_roc_auc_std": float(cv_scores.std()),
                "test_accuracy": float(
                    accuracy_score(y_test, predictions)
                ),
                "test_precision": float(
                    precision_score(
                        y_test, predictions, zero_division=0
                    )
                ),
                "test_recall": float(
                    recall_score(
                        y_test, predictions, zero_division=0
                    )
                ),
                "test_f1": float(
                    f1_score(y_test, predictions, zero_division=0)
                ),
                "test_roc_auc": float(
                    roc_auc_score(y_test, probabilities)
                ),
            }

            results[name] = metrics
            fitted_pipelines[name] = pipeline

            # Record evaluation metrics in MLflow.
            mlflow.log_metrics(metrics)

            print("Metrics:")
            print(json.dumps(metrics, indent=2))

            report = classification_report(
                y_test,
                predictions,
                zero_division=0,
                output_dict=True,
            )

            print("\nClassification report:")
            print(
                classification_report(
                    y_test,
                    predictions,
                    zero_division=0,
                )
            )

            # Save and log the classification report.
            report_path = RESULTS_DIR / f"classification_report_{name}.json"
            with open(report_path, "w", encoding="utf-8") as f:
                json.dump(report, f, indent=2)

            mlflow.log_artifact(str(report_path))

            # Generate, save and log the confusion matrix.
            ConfusionMatrixDisplay.from_predictions(
                y_test,
                predictions,
                display_labels=["No disease", "Disease"],
            )
            plt.title(f"Confusion Matrix - {name}")
            plt.tight_layout()

            confusion_path = RESULTS_DIR / f"confusion_matrix_{name}.png"
            plt.savefig(confusion_path, dpi=150)
            plt.close()

            mlflow.log_artifact(str(confusion_path))

            # Generate, save and log the model's ROC curve.
            RocCurveDisplay.from_predictions(
                y_test,
                probabilities,
                name=name,
            )
            plt.title(f"ROC Curve - {name}")
            plt.tight_layout()

            roc_path = RESULTS_DIR / f"roc_curve_{name}.png"
            plt.savefig(roc_path, dpi=150)
            plt.close()

            mlflow.log_artifact(str(roc_path))

            # Log the complete fitted pipeline, including preprocessing.
            

            print(f"MLflow run logged: {name}")

    # Select the model with the highest mean cross-validation ROC-AUC.
    best_name = max(
        results,
        key=lambda name: results[name]["cv_roc_auc_mean"],
    )
    best_pipeline = fitted_pipelines[best_name]

    # Save the selected model locally for the API and deployment stages.
    joblib.dump(
        best_pipeline,
        MODEL_DIR / "heart_disease_model.joblib",
    )

    # Save the evaluation results locally.
    metrics_path = RESULTS_DIR / "model_metrics.json"
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump(
            {
                "selection_metric": "mean 5-fold training ROC-AUC",
                "selected_model": best_name,
                "models": results,
            },
            f,
            indent=2,
        )

    # Create a comparison ROC plot for both models.
    fig, ax = plt.subplots(figsize=(7, 6))

    for name, pipeline in fitted_pipelines.items():
        RocCurveDisplay.from_estimator(
            pipeline,
            X_test,
            y_test,
            name=name,
            ax=ax,
        )

    ax.set_title("ROC Curves - Heart Disease Models")
    fig.tight_layout()

    comparison_path = RESULTS_DIR / "roc_curves.png"
    fig.savefig(comparison_path, dpi=150)
    plt.close(fig)

    # Log the overall comparison and selected model in a summary run.
    with mlflow.start_run(run_name="model_comparison_summary"):
        mlflow.log_param("selection_metric", "cv_roc_auc_mean")
        mlflow.log_param("selected_model", best_name)

        for name, metrics in results.items():
            mlflow.log_metric(
                f"{name}_cv_roc_auc_mean",
                metrics["cv_roc_auc_mean"],
            )
            mlflow.log_metric(
                f"{name}_test_accuracy",
                metrics["test_accuracy"],
            )
            mlflow.log_metric(
                f"{name}_test_roc_auc",
                metrics["test_roc_auc"],
            )

        mlflow.log_artifact(str(metrics_path))
        mlflow.log_artifact(str(comparison_path))

    print("\nSelected model:", best_name)
    print("Saved model:", MODEL_DIR / "heart_disease_model.joblib")
    print("Saved metrics:", metrics_path)
    print("Saved plots:", RESULTS_DIR)
    print("MLflow tracking directory:", MLFLOW_DIR)


if __name__ == "__main__":
    main()
