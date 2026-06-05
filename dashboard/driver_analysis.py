import pandas as pd

def revenue_by_product_group(df):

    result = (
        df.groupby("product_group", as_index=False)
        ["line_item_value"]
        .sum()
        .sort_values(
            by="line_item_value",
            ascending=False
        )
    )

    return result


def revenue_by_vendor(df):

    result = (
        df.groupby("vendor", as_index=False)
        ["line_item_value"]
        .sum()
        .sort_values(
            by="line_item_value",
            ascending=False
        )
    )

    return result


def country_revenue_share(df):

    country_df = (
        df.groupby("country", as_index=False)
        ["line_item_value"]
        .sum()
    )

    total_revenue = (
        country_df["line_item_value"]
        .sum()
    )

    country_df["revenue_share_pct"] = (
        country_df["line_item_value"]
        / total_revenue
        * 100
    )

    return country_df.sort_values(
        by="revenue_share_pct",
        ascending=False
    )


def vendor_pareto(df):

    vendor_df = (
        df.groupby("vendor", as_index=False)
        ["line_item_value"]
        .sum()
        .sort_values(
            by="line_item_value",
            ascending=False
        )
    )

    total = vendor_df[
        "line_item_value"
    ].sum()

    vendor_df["pct"] = (
        vendor_df["line_item_value"]
        / total
        * 100
    )

    vendor_df["cumulative_pct"] = (
        vendor_df["pct"]
        .cumsum()
    )

    return vendor_df


