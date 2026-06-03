import pandas as pd


def calculate_kpis(df):

    total_revenue = df["line_item_value"].fillna(0).sum()

    total_freight_cost = (
        pd.to_numeric(df["freight_cost_(usd)"], errors="coerce")
        .fillna(0)
        .sum()
    )

    total_units = (
        df["line_item_quantity"]
        .fillna(0)
        .sum()
    )

    total_countries = df["country"].nunique()

    return {
        "total_revenue": total_revenue,
        "total_freight_cost": total_freight_cost,
        "total_units": total_units,
        "total_countries": total_countries
    }
