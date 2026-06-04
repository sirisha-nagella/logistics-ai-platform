import pandas as pd
import plotly.express as px


def revenue_by_country(df):

    revenue_df = (
        df.groupby("country", as_index=False)["line_item_value"]
        .sum()
        .sort_values(
            by="line_item_value",
            ascending=False
        )
        .head(10)
    )

    revenue_df["revenue_millions"] = (
        revenue_df["line_item_value"] / 1_000_000
    )

    fig = px.bar(
        revenue_df,
        x="country",
        y="revenue_millions",
        title="Top 10 Countries by Revenue (Millions USD)"
    )

    fig.update_layout(
        xaxis_title="Country",
        yaxis_title="Revenue (Millions USD)"
    )

    fig.update_xaxes(
        tickangle=-30
    )

    return fig


def revenue_by_shipment_mode(df):

    shipment_df = (
        df.assign(shipment_mode=df["shipment_mode"].fillna("Unknown"))
        .groupby("shipment_mode", as_index=False)["line_item_value"]
        .sum()
        .sort_values(
            by="line_item_value",
            ascending=False
        )
    )

    shipment_df["revenue_millions"] = (
        shipment_df["line_item_value"] / 1_000_000
    )

    fig = px.bar(
        shipment_df,
        x="shipment_mode",
        y="revenue_millions",
        title="Revenue by Shipment Mode"
    )

    return fig


def monthly_revenue_trend(df):

    trend_df = df.copy()

    trend_df["delivery_recorded_date"] = pd.to_datetime(
        trend_df["delivery_recorded_date"],
        format="%d-%b-%y",
        errors="coerce"
    )

    trend_df = trend_df.dropna(
        subset=["delivery_recorded_date"]
    )

    trend_df["year_month"] = (
        trend_df["delivery_recorded_date"]
        .dt.to_period("M")
        .dt.to_timestamp()
    )

    monthly_revenue = (
        trend_df.groupby(
            "year_month",
            as_index=False
        )["line_item_value"]
        .sum()
    )

    monthly_revenue["revenue_millions"] = (
        monthly_revenue["line_item_value"]
        / 1_000_000
    )

    fig = px.line(
        monthly_revenue,
        x="year_month",
        y="revenue_millions",
        title="Monthly Revenue Trend (Millions USD)"
    )


    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Revenue (Millions USD)"
    )

    return fig


def monthly_freight_cost_trend(df):

    trend_df = df.copy()

    trend_df["delivery_recorded_date"] = pd.to_datetime(
        trend_df["delivery_recorded_date"],
        format="%d-%b-%y",
        errors="coerce"
    )

    trend_df = trend_df.dropna(
        subset=["delivery_recorded_date"]
    )

    trend_df["freight_cost_(usd)"] = pd.to_numeric(
        trend_df["freight_cost_(usd)"],
        errors="coerce"
    )

    trend_df["year_month"] = (
        trend_df["delivery_recorded_date"]
        .dt.to_period("M")
        .dt.to_timestamp()
    )

    monthly_freight = (
        trend_df.groupby(
            "year_month",
            as_index=False
        )["freight_cost_(usd)"]
        .sum()
    )

    monthly_freight["freight_millions"] = (
        monthly_freight["freight_cost_(usd)"]
        / 1_000_000
    )

    fig = px.line(
        monthly_freight,
        x="year_month",
        y="freight_millions",
        title="Monthly Freight Cost Trend (Millions USD)"
    )


    fig.update_layout(
        xaxis_title="Month",
        yaxis_title="Freight Cost (Millions USD)"
    )

    return fig


