
from pathlib import Path
import pandas as pd

# Locate the project directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = PROJECT_ROOT / "data" / "raw" / "processed.cleveland.data"

# Column names documented for the Cleveland dataset
COLUMNS = [
    "age", "sex", "cp", "trestbps", "chol", "fbs",
    "restecg", "thalach", "exang", "oldpeak", "slope",
    "ca", "thal", "target"
]

def main():
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"Dataset not found: {DATA_PATH}")

    df = pd.read_csv(
        DATA_PATH,
        header=None,
        names=COLUMNS,
        na_values="?"
    )

    print("Dataset shape:", df.shape)
    print("\nFirst five rows:")
    print(df.head())

    print("\nData types:")
    print(df.dtypes)

    print("\nMissing values by column:")
    print(df.isnull().sum())
    print("\nTotal missing values:", df.isnull().sum().sum())

    print("\nTarget value counts:")
    print(df["target"].value_counts(dropna=False).sort_index())

if __name__ == "__main__":
    main()
