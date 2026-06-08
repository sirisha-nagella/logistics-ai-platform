import streamlit as st

from dashboard.charts import monthly_revenue_trend, monthly_freight_cost_trend

df = st.session_state["df"]

st.subheader("Revenue Trends")
st.plotly_chart(monthly_revenue_trend(df), width="stretch")
st.plotly_chart(monthly_freight_cost_trend(df), width="stretch")
