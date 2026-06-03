import streamlit as st

from utils.data_loader import load_data
from dashboard.kpi_calculator import calculate_kpis
from dashboard.charts import revenue_by_country


st.set_page_config(
    page_title="Logistics Revenue Intelligence",
    layout="wide"
)

st.title("🚚 Logistics Pricing & Revenue Intelligence")


df = load_data("data/supply_chain_data.csv")

kpis = calculate_kpis(df)


col1, col2, col3, col4 = st.columns(4)

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


st.divider()

st.subheader("Revenue Analysis")

country_fig = revenue_by_country(df)

st.plotly_chart(
    country_fig,
    width="stretch"
)
