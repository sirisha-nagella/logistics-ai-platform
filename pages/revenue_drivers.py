import streamlit as st

from dashboard.charts import (
    product_group_chart,
    vendor_pareto_chart,
    country_share_chart,
)
from dashboard.driver_analysis import (
    revenue_by_product_group,
    vendor_pareto,
    country_revenue_share,
)

df = st.session_state["df"]

st.header("Revenue Driver Analysis")

country_df = country_revenue_share(df)
vendor_df = vendor_pareto(df)
product_group_df = revenue_by_product_group(df)

top_country = country_df.iloc[0]
top_vendor = vendor_df.iloc[0]
top_product_group = product_group_df.iloc[0]

st.subheader("Top Revenue Driver Summary")
c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Country", top_country["country"], f"{top_country['revenue_share_pct']:.1f}% of revenue")
with c2:
    st.metric("Vendor", top_vendor["vendor"], f"${top_vendor['line_item_value']:,.0f}")
with c3:
    st.metric("Product Group", top_product_group["product_group"], f"${top_product_group['line_item_value']:,.0f}")

st.subheader("Product Group Revenue")
st.plotly_chart(product_group_chart(product_group_df), width="stretch")

st.subheader("Vendor Concentration")
st.plotly_chart(vendor_pareto_chart(vendor_df), width="stretch")

st.subheader("Country Revenue Share")
st.plotly_chart(country_share_chart(country_df), width="stretch", key="country_share_drivers")
