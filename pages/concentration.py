import streamlit as st
import pandas as pd

from dashboard.charts import country_share_chart, product_group_share_chart
from dashboard.driver_analysis import (
    revenue_by_product_group,
    vendor_pareto,
    country_revenue_share,
    product_group_share,
    classify_risk,
)

df = st.session_state["df"]

country_df = country_revenue_share(df)
vendor_df = vendor_pareto(df)
product_group_df = revenue_by_product_group(df)
product_group_share_df = product_group_share(df)

top_country = country_df.iloc[0]
top_vendor = vendor_df.iloc[0]
top_product_group = product_group_df.iloc[0]

top_country_share = top_country["revenue_share_pct"]
top_vendor_share = top_vendor["pct"]
top_product_group_share = product_group_share_df.iloc[0]["share_pct"]

top_5_country_share = country_df.head(5)["revenue_share_pct"].sum()
top_5_vendor_share = vendor_df.head(5)["pct"].sum()
top_5_product_group_share = product_group_share_df.head(5)["share_pct"].sum()

dependency_score = (top_vendor_share + top_product_group_share) / 2

st.header("Revenue Concentration Analysis")

c1, c2, c3 = st.columns(3)
with c1:
    st.metric("Top Country", top_country["country"], f"{top_country_share:.1f}%")
with c2:
    st.metric("Top Vendor", top_vendor["vendor"], f"{top_vendor_share:.1f}%")
with c3:
    st.metric("Top Product Group", top_product_group["product_group"], f"{top_product_group_share:.1f}%")

st.subheader("Top 5 Concentration")
t1, t2, t3 = st.columns(3)
with t1:
    st.metric("Top 5 Countries", f"{top_5_country_share:.1f}%")
with t2:
    st.metric("Top 5 Vendors", f"{top_5_vendor_share:.1f}%")
with t3:
    st.metric("Top 5 Product Groups", f"{top_5_product_group_share:.1f}%")

st.subheader("Revenue Dependency Score")
st.metric("Dependency Score", f"{dependency_score:.1f}")
st.caption(
    "Custom metric (avg of top vendor and top product group share). "
    "Higher score = higher concentration risk."
)

st.subheader("Top 10 Countries by Revenue %")
st.plotly_chart(country_share_chart(country_df), width="stretch", key="country_share_top10")

st.subheader("Product Group Revenue Share")
st.plotly_chart(product_group_share_chart(product_group_share_df), width="stretch")

st.subheader("Key Business Insights")
st.markdown(
    f"""
- {top_country['country']} contributes {top_country_share:.1f}% of total revenue.
- {top_vendor['vendor']} contributes {top_vendor_share:.1f}% of total revenue.
- {top_product_group['product_group']} products account for {top_product_group_share:.1f}% of total revenue.
- Revenue appears highly concentrated across both vendor and product dimensions.
"""
)

st.divider()
st.header("Executive Revenue Intelligence")

st.subheader("Revenue Concentration Scorecard")
scorecard_df = pd.DataFrame(
    {
        "KPI": ["Top Vendor Share", "Top Product Share", "Top Country Share", "Top 5 Vendor Share", "Top 5 Country Share"],
        "Value": [
            f"{top_vendor_share:.1f}%",
            f"{top_product_group_share:.1f}%",
            f"{top_country_share:.1f}%",
            f"{top_5_vendor_share:.1f}%",
            f"{top_5_country_share:.1f}%",
        ],
    }
)
st.table(scorecard_df)

st.subheader("Risk Classification")
risk_df = pd.DataFrame(
    {
        "Category": ["Vendor Dependency", "Product Dependency", "Country Dependency"],
        "Share": [f"{top_vendor_share:.1f}%", f"{top_product_group_share:.1f}%", f"{top_country_share:.1f}%"],
        "Risk": [classify_risk(top_vendor_share), classify_risk(top_product_group_share), classify_risk(top_country_share)],
    }
)
st.table(risk_df)
