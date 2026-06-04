import pandas as pd
import os

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "supply_chain_data.csv")


def load_data(filepath: str = DATA_PATH) -> pd.DataFrame:
    df = pd.read_csv(filepath, encoding="latin-1")
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_").str.replace("/", "_")
    return df


def get_shape(df: pd.DataFrame) -> tuple:
    return df.shape


def get_summary(df: pd.DataFrame) -> pd.DataFrame:
    return df.describe(include="all")


def get_missing(df: pd.DataFrame) -> pd.Series:
    missing = df.isnull().sum()
    return missing[missing > 0].sort_values(ascending=False)


if __name__ == "__main__":
    df = load_data()
    print(f"Shape: {get_shape(df)}")
    print(f"\nMissing values:\n{get_missing(df)}")
    print(f"\nColumns:\n{df.columns.tolist()}")
