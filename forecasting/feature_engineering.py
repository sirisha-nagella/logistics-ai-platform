import pandas as pd

# Single source of truth for the columns the model trains and predicts on.
# Keeping this here prevents train/predict feature drift.
FEATURE_COLUMNS = [
    "year",
    "month",
    "quarter",
    "lag_1",
    "lag_3",
    "lag_12",
    "rolling_mean_3",
    "rolling_mean_6",
]


def build_features(monthly_df):
    """Build the full feature frame from a monthly revenue dataframe.

    Expects a ``date`` (datetime) and ``revenue`` column. Returns the frame
    with all engineered features and rows containing NaN lags dropped.
    """

    df = create_time_features(monthly_df)
    df = create_lag_features(df)
    df = create_rolling_features(df)
    df = create_trend_feature(df)

    return df.dropna()


def create_time_features(df):

    df = df.copy()

    df["year"] = df["date"].dt.year

    df["month"] = df["date"].dt.month

    df["quarter"] = df["date"].dt.quarter

    return df

def create_lag_features(df):

    df = df.copy()

    df["lag_1"] = df["revenue"].shift(1)

    df["lag_3"] = df["revenue"].shift(3)

    df["lag_12"] = df["revenue"].shift(12)

    return df

# Additional features:

def create_rolling_features(df):

    df = df.copy()

    df["rolling_mean_3"] = (
        df["revenue"]
        .shift(1)
        .rolling(3)
        .mean()
    )

    df["rolling_mean_6"] = (
        df["revenue"]
        .shift(1)
        .rolling(6)
        .mean()
    )

    return df

# Add trend feature:

def create_trend_feature(df):

    df = df.copy()

    df["time_index"] = range(len(df))

    return df

