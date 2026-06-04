import pandas as pd


def parse_delivery_dates(df):

    df = df.copy()

    df["delivery_recorded_date"] = pd.to_datetime(
        df["delivery_recorded_date"],
        format="%d-%b-%y",
        errors="coerce"
    )

    return df
