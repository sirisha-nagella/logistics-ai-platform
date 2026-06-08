import streamlit as st

from dashboard.charts import (
    spike_country_chart,
    spike_vendor_chart,
    spike_shipment_chart,
)
from dashboard.investigation import (
    get_month_data,
    top_countries_for_month,
    top_vendors_for_month,
    shipment_mode_breakdown,
)

df = st.session_state["df"]

st.subheader("Revenue Spike Investigation")

available_months = ["2011-09", "2014-06", "2015-03"]
selected_month = st.selectbox("Select Spike Month", available_months)

month_df = get_month_data(df, selected_month)
st.write(f"Records analyzed: {len(month_df):,}")

st.subheader("Top Countries Driving Revenue")
st.plotly_chart(spike_country_chart(top_countries_for_month(month_df)), width="stretch")

st.subheader("Top Vendors Driving Revenue")
st.plotly_chart(spike_vendor_chart(top_vendors_for_month(month_df)), width="stretch")

st.subheader("Shipment Mode Contribution")
st.plotly_chart(spike_shipment_chart(shipment_mode_breakdown(month_df)), width="stretch")
