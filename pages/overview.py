import streamlit as st

from dashboard.kpi_calculator import calculate_kpis, calculate_freight_ratio
from dashboard.charts import revenue_by_country, revenue_by_shipment_mode

df = st.session_state["df"]

kpis = calculate_kpis(df)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Total Revenue", f"${kpis['total_revenue']:,.0f}")
with col2:
    st.metric("Total Freight Cost", f"${kpis['total_freight_cost']:,.0f}")
with col3:
    st.metric("Total Units", f"{kpis['total_units']:,.0f}")
with col4:
    st.metric("Countries", kpis["total_countries"])
with col5:
    st.metric("Freight Cost %", f"{calculate_freight_ratio(df):.2f}%")

st.divider()

st.subheader("Revenue Analysis")
st.plotly_chart(revenue_by_country(df), width="stretch")
st.plotly_chart(revenue_by_shipment_mode(df), width="stretch")
