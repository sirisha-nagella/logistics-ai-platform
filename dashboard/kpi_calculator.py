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


def calculate_freight_ratio(df):

    # ~40% of rows carry non-numeric freight values (e.g. "Freight Included
    # in Commodity Cost", "Invoiced Separately"). Coercing those to 0 and
    # dividing by total revenue understates the ratio, because the numerator
    # drops those shipments while the denominator keeps them. Compare freight
    # against revenue for the SAME shipments: those with a real freight value.

    freight = pd.to_numeric(df["freight_cost_(usd)"], errors="coerce")

    has_freight = freight.notna()

    freight_total = freight[has_freight].sum()

    revenue_total = (
        df.loc[has_freight, "line_item_value"]
        .fillna(0)
        .sum()
    )

    if revenue_total == 0:
        return 0.0

    return (freight_total / revenue_total) * 100
