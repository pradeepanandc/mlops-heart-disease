
from pathlib import Path
import pandas as pd

# Project paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_PATH = PROJECT_ROOT / "data" / "raw" / "processed.cleveland.data"
PROCESSED_DATA_PATH = PROJECT_ROOT / "data" / "processed" / "heart_disease.csv"

COLUMNS = [
    "age", "sex", "cp", "trestbps", "chol", "fbs",
    "restecg", "thalach", "exang", "oldpeak", "slope",
    "ca", "thal", "target"
]

def prepare_data():
    # Load source data; '?' represents missing values
    df = pd.read_csv(
        RAW_DATA_PATH,
        header=None,
        names=COLUMNS,
        na_values="?"
    )

    print("Original dataset shape:", df.shape)
    print("Missing values before preparation:", int(df.isna().sum().sum()))

    # Convert columns to numeric where appropriate
    for column in COLUMNS:
        df[column] = pd.to_numeric(df[column], errors="coerce")

    # Remove records without a target, if any
    df = df.dropna(subset=["target"]).copy()

    # Convert the target into binary classification:
    # 0 = absence of heart disease; 1-4 = presence
    df["target"] = (df["target"] > 0).astype(int)

    # Create output directory and save a separate prepared file
    PROCESSED_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(PROCESSED_DATA_PATH, index=False)

    print("\nPrepared dataset shape:", df.shape)
    print("Missing values remaining:", int(df.isna().sum().sum()))
    print("\nBinary target distribution:")
    print(df["target"].value_counts().sort_index())
    print("\nSaved prepared dataset to:", PROCESSED_DATA_PATH)

if __name__ == "__main__":
    prepare_data()
