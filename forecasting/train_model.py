import os

import pandas as pd
import matplotlib.pyplot as plt

from xgboost import XGBRegressor

from forecasting.feature_engineering import (
    create_time_features,
    create_lag_features,
    create_rolling_features,
    create_trend_feature,
    FEATURE_COLUMNS
)
from forecasting.evaluate import evaluate_predictions, format_metrics

MODEL_PATH = "models/xgb_revenue.json"

# Load the monthly revenue dataset

monthly_df = pd.read_csv(
    "data/monthly_revenue.csv"
)

# Convert date:

monthly_df["date"] = pd.to_datetime(
    monthly_df["date"]
)

# Build features (time + lag) from the monthly series:

df = create_time_features(monthly_df)

df = create_lag_features(df)

df = create_rolling_features(df)

df = create_trend_feature(df)

# Features (shared with predict.py via feature_engineering.FEATURE_COLUMNS):

feature_columns = FEATURE_COLUMNS

# Remove NaNs (lag columns leave gaps at the start):

df = df.dropna()

# Chronological Split:

split_index = int(len(df) * 0.8)

train_df = df.iloc[:split_index]

test_df = df.iloc[split_index:]

# Create Train/test sets:

X_train = train_df[feature_columns]

y_train = train_df["revenue"]

X_test = test_df[feature_columns]

y_test = test_df["revenue"]

# Create and train the model:

model = XGBRegressor(
    n_estimators=300,
    max_depth=4,
    learning_rate=0.05,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)

model.fit(X_train, y_train)

# Feature importance:

importance_df = pd.DataFrame({
    "feature": feature_columns,
    "importance": model.feature_importances_
})

print(
    importance_df.sort_values(
        "importance",
        ascending=False
    )
)

print("Training Period")

print(
    train_df["date"].min(),
    train_df["date"].max()
)

print("\nTesting Period")

print(
    test_df["date"].min(),
    test_df["date"].max()
)

# After the split print:

print(f"Rows before lagging: {len(monthly_df)}")
print(f"Rows after lagging: {len(df)}")

# Verify year month quarter lag_1 lag_3 lag_12

print(train_df[feature_columns].head())

print(train_df[feature_columns].isna().sum())

# Model predictions, plus a naive baseline (predict each month as the
# previous month) so we can show the model actually beats carry-forward:

predictions = model.predict(X_test)

baseline = X_test["lag_1"]

results = test_df.copy()

results["predicted_revenue"] = predictions

results["baseline_revenue"] = baseline.values

# Persist the trained model so predict.py / the app can load it:

os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)

model.save_model(MODEL_PATH)

print(f"\nModel saved to {MODEL_PATH}")

# Plot

plt.figure(figsize=(12, 6))

plt.plot(
    results["date"],
    results["revenue"],
    label="Actual"
)
plt.plot(
    results["date"],
    results["predicted_revenue"],
    label="Predicted (XGBoost)"
)
plt.plot(
    results["date"],
    results["baseline_revenue"],
    label="Baseline (lag_1)",
    linestyle="--"
)

plt.legend()

plt.title("Actual vs Predicted Revenue")

plt.show()

# Evaluation: report the model and the baseline side by side.

model_metrics = evaluate_predictions(y_test, predictions)

baseline_metrics = evaluate_predictions(y_test, baseline)

print("\nXGBoost model:")
print(format_metrics(model_metrics))

print("\nNaive baseline (lag_1):")
print(format_metrics(baseline_metrics))
