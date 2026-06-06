import pandas as pd

from xgboost import XGBRegressor

from forecasting.feature_engineering import build_features, FEATURE_COLUMNS

MODEL_PATH = "models/xgb_revenue.json"


def load_model(model_path=MODEL_PATH):
    """Load the trained XGBoost revenue model saved by train_model.py."""

    model = XGBRegressor()
    model.load_model(model_path)
    return model


def predict_from_monthly(monthly_df, model=None, model_path=MODEL_PATH):
    """Predict revenue for every month that has complete lag features.

    Returns a copy of the feature frame with a ``predicted_revenue`` column.
    """

    if model is None:
        model = load_model(model_path)

    features = build_features(monthly_df)

    features = features.copy()
    features["predicted_revenue"] = model.predict(features[FEATURE_COLUMNS])

    return features


if __name__ == "__main__":
    monthly_df = pd.read_csv("data/monthly_revenue.csv")
    monthly_df["date"] = pd.to_datetime(monthly_df["date"])

    predictions = predict_from_monthly(monthly_df)

    print(
        predictions[["date", "revenue", "predicted_revenue"]].tail(12)
    )
