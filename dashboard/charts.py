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
        df.groupby("shipment_mode", as_index=False)["line_item_value"]
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


