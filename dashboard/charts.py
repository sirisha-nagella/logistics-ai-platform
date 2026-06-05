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


def spike_country_chart(country_df):

    chart_df = country_df.copy()

    chart_df["revenue_millions"] = (
        chart_df["line_item_value"] / 1_000_000
    )

    fig = px.bar(
        chart_df,
        x="country",
        y="revenue_millions",
        title="Top Countries Driving Revenue (Millions USD)"
    )

    fig.update_layout(
        xaxis_title="Country",
        yaxis_title="Revenue (Millions USD)"
    )

    fig.update_xaxes(
        tickangle=-30
    )

    return fig


def spike_vendor_chart(vendor_df):

    chart_df = vendor_df.copy()

    chart_df["revenue_millions"] = (
        chart_df["line_item_value"] / 1_000_000
    )

    fig = px.bar(
        chart_df,
        x="vendor",
        y="revenue_millions",
        title="Top Vendors Driving Revenue (Millions USD)"
    )

    fig.update_layout(
        xaxis_title="Vendor",
        yaxis_title="Revenue (Millions USD)"
    )

    fig.update_xaxes(
        tickangle=-30
    )

    return fig


def spike_shipment_chart(shipment_df):

    chart_df = shipment_df.copy()

    chart_df["revenue_millions"] = (
        chart_df["line_item_value"] / 1_000_000
    )

    fig = px.bar(
        chart_df,
        x="shipment_mode",
        y="revenue_millions",
        title="Shipment Mode Contribution (Millions USD)"
    )

    fig.update_layout(
        xaxis_title="Shipment Mode",
        yaxis_title="Revenue (Millions USD)"
    )

    return fig


def product_group_chart(df):

    chart_df = df.head(10).copy()

    chart_df["revenue_millions"] = (
        chart_df["line_item_value"] / 1_000_000
    )

    fig = px.bar(
        chart_df,
        x="product_group",
        y="revenue_millions",
        title="Top 10 Product Groups by Revenue (Millions USD)"
    )

    fig.update_layout(
        xaxis_title="Product Group",
        yaxis_title="Revenue (Millions USD)"
    )

    fig.update_xaxes(
        tickangle=-30
    )

    return fig


def vendor_pareto_chart(df):

    # Cumulative concentration curve across all vendors, ranked by revenue

    chart_df = df.copy()

    chart_df["vendor_rank"] = range(1, len(chart_df) + 1)

    fig = px.line(
        chart_df,
        x="vendor_rank",
        y="cumulative_pct",
        markers=True,
        title="Vendor Revenue Contribution"
    )

    fig.update_layout(
        xaxis_title="Vendor Rank",
        yaxis_title="Cumulative Revenue %"
    )

    return fig


def country_share_chart(df):

    chart_df = df.head(10).copy()

    chart_df["share_label"] = (
        chart_df["revenue_share_pct"]
        .round(1)
        .astype(str)
        + "%"
    )

    fig = px.bar(
        chart_df,
        x="country",
        y="revenue_share_pct",
        text="share_label",
        title="Top 10 Countries by Revenue Share"
    )

    fig.update_layout(
        xaxis_title="Country",
        yaxis_title="Revenue Share (%)"
    )

    fig.update_xaxes(
        tickangle=-30
    )

    return fig


def product_group_share_chart(df):

    chart_df = df.copy()

    chart_df["share_label"] = (
        chart_df["share_pct"]
        .round(1)
        .astype(str)
        + "%"
    )

    fig = px.bar(
        chart_df,
        x="product_group",
        y="share_pct",
        text="share_label",
        title="Product Group Revenue Share"
    )

    fig.update_layout(
        xaxis_title="Product Group",
        yaxis_title="Revenue Share (%)"
    )

    return fig


