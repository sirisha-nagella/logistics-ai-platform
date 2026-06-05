import pandas as pd


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

