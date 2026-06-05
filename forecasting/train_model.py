import pandas as pd
import matplotlib.pyplot as plt

from xgboost import XGBRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    mean_absolute_percentage_error
)

from forecasting.feature_engineering import (
    create_time_features,
    create_lag_features,
    create_rolling_features,
    create_trend_feature
)

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

# Create features:

feature_columns = [
    "year",
    "month",
    "quarter",
    "lag_1",
    "lag_3",
    "lag_12",
    "rolling_mean_3",
    "rolling_mean_6"
]

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

# Prediction (naive baseline: predict each month as the previous month):

predictions = X_test["lag_1"]

results = test_df.copy()

results["predicted_revenue"] = predictions

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
    label="predicted"
)

plt.legend()

plt.title("Actual vs Predicted Revenue")

plt.show()

# Evaluation:

mae = mean_absolute_error(
    y_test,
    predictions
)

rmse = mean_squared_error(
    y_test,
    predictions
) ** 0.5

mape = mean_absolute_percentage_error(
    y_test,
    predictions
) * 100

print(f"MAE: ${mae:,.2f}")
print(f"RMSE: ${rmse:,.2f}")
print(f"MAPE: {mape:.2f}%")
