import streamlit as st

from utils.data_loader import load_data
from dashboard.kpi_calculator import calculate_kpis, calculate_freight_ratio
from dashboard.charts import (
    revenue_by_country,
    revenue_by_shipment_mode,
    monthly_revenue_trend,
    monthly_freight_cost_trend,
    spike_country_chart,
    spike_vendor_chart,
    spike_shipment_chart,
    product_group_chart,
    vendor_pareto_chart,
    country_share_chart
)
from dashboard.filters import apply_filters
from dashboard.investigation import (
    get_month_data,
    top_countries_for_month,
    top_vendors_for_month,
    shipment_mode_breakdown
)
from dashboard.driver_analysis import (
    revenue_by_product_group,
    vendor_pareto,
    country_revenue_share
)


st.set_page_config(
    page_title="Logistics Revenue Intelligence",
    layout="wide"
)

st.title("🚚 Logistics Pricing & Revenue Intelligence")


df = load_data("data/supply_chain_data.csv")

df = apply_filters(df)

st.caption(
    f"Filtered Records: {len(df):,}"
)

kpis = calculate_kpis(df)


col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Total Revenue",
        f"${kpis['total_revenue']:,.0f}"
    )

with col2:
    st.metric(
        "Total Freight Cost",
        f"${kpis['total_freight_cost']:,.0f}"
    )

with col3:
    st.metric(
        "Total Units",
        f"{kpis['total_units']:,.0f}"
    )

with col4:
    st.metric(
        "Countries",
        kpis["total_countries"]
    )

with col5:
    st.metric(
        "Freight Cost %",
        f"{calculate_freight_ratio(df):.2f}%"
    )


st.divider()

st.subheader("Revenue Analysis")

country_fig = revenue_by_country(df)

st.plotly_chart(
    country_fig,
    width="stretch"
)

shipment_fig = revenue_by_shipment_mode(df)

st.plotly_chart(
    shipment_fig,
    width="stretch"
)


st.divider()

st.subheader("Revenue Trends")

trend_fig = monthly_revenue_trend(df)

st.plotly_chart(
    trend_fig,
    width="stretch"
)

freight_trend_fig = monthly_freight_cost_trend(df)

st.plotly_chart(
    freight_trend_fig,
    width="stretch"
)


st.divider()

st.subheader("Revenue Spike Investigation")

available_months = [
    "2011-09",
    "2014-06",
    "2015-03"
]

selected_month = st.selectbox(
    "Select Spike Month",
    available_months
)

month_df = get_month_data(
    df,
    selected_month
)

st.write(
    f"Records analyzed: {len(month_df):,}"
)

country_analysis = top_countries_for_month(
    month_df
)

st.subheader(
    "Top Countries Driving Revenue"
)

st.plotly_chart(
    spike_country_chart(country_analysis),
    width="stretch"
)

vendor_analysis = top_vendors_for_month(
    month_df
)

st.subheader(
    "Top Vendors Driving Revenue"
)

st.plotly_chart(
    spike_vendor_chart(vendor_analysis),
    width="stretch"
)

shipment_analysis = shipment_mode_breakdown(
    month_df
)

st.subheader(
    "Shipment Mode Contribution"
)

st.plotly_chart(
    spike_shipment_chart(shipment_analysis),
    width="stretch"
)


st.divider()

st.header(
    "Revenue Driver Analysis"
)

# Ranked driver tables (reused for the summary card and the charts):

country_df = country_revenue_share(df)

vendor_df = vendor_pareto(df)

product_group_df = revenue_by_product_group(df)

# Top driver per dimension (first row of each ranked table):

top_country = country_df.iloc[0]

top_vendor = vendor_df.iloc[0]

top_product_group = product_group_df.iloc[0]

st.subheader("Top Revenue Driver Summary")

driver_col1, driver_col2, driver_col3 = st.columns(3)

with driver_col1:
    st.metric(
        "Country",
        top_country["country"],
        f"{top_country['revenue_share_pct']:.1f}% of revenue"
    )

with driver_col2:
    st.metric(
        "Vendor",
        top_vendor["vendor"],
        f"${top_vendor['line_item_value']:,.0f}"
    )

with driver_col3:
    st.metric(
        "Product Group",
        top_product_group["product_group"],
        f"${top_product_group['line_item_value']:,.0f}"
    )

st.subheader("Product Group Revenue")

st.plotly_chart(
    product_group_chart(product_group_df),
    width="stretch"
)

st.subheader("Vendor Concentration")

st.plotly_chart(
    vendor_pareto_chart(vendor_df),
    width="stretch"
)

st.subheader("Country Revenue Share")

st.plotly_chart(
    country_share_chart(country_df),
    width="stretch"
)
