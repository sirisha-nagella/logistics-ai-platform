import pandas as pd


def get_month_data(df, selected_month):

    temp_df = df.copy()

    temp_df["delivery_recorded_date"] = pd.to_datetime(
        temp_df["delivery_recorded_date"],
        format="%d-%b-%y",
        errors="coerce"
    )

    temp_df["year_month"] = (
        temp_df["delivery_recorded_date"]
        .dt.to_period("M")
        .astype(str)
    )

    return temp_df[
        temp_df["year_month"] == selected_month
    ]


def top_countries_for_month(df):

    country_df = (
        df.groupby("country", as_index=False)
        ["line_item_value"]
        .sum()
        .sort_values(
            by="line_item_value",
            ascending=False
        )
        .head(10)
    )

    return country_df


def top_vendors_for_month(df):

    vendor_df = (
        df.groupby("vendor", as_index=False)
        ["line_item_value"]
        .sum()
        .sort_values(
            by="line_item_value",
            ascending=False
        )
        .head(10)
    )

    return vendor_df


def shipment_mode_breakdown(df):

    shipment_df = (
        df.assign(shipment_mode=df["shipment_mode"].fillna("Unknown"))
        .groupby("shipment_mode", as_index=False)
        ["line_item_value"]
        .sum()
        .sort_values(
            by="line_item_value",
            ascending=False
        )
    )

    return shipment_df
