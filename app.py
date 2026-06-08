import streamlit as st

from utils.data_loader import load_data
from dashboard.filters import apply_filters

st.set_page_config(
    page_title="Logistics Revenue Intelligence",
    layout="wide"
)

st.title("🚚 Logistics Pricing & Revenue Intelligence")

# Load + filter ONCE. The sidebar filters render for every page and the
# filtered frame is shared with each page via session state.
df = load_data("data/supply_chain_data.csv")
df = apply_filters(df)
st.session_state["df"] = df

st.caption(f"Filtered Records: {len(df):,}")

pages = [
    st.Page("pages/overview.py", title="Overview", icon="📊"),
    st.Page("pages/trends.py", title="Trends", icon="📈"),
    st.Page("pages/spike_investigation.py", title="Spike Investigation", icon="🔎"),
    st.Page("pages/revenue_drivers.py", title="Revenue Drivers", icon="🏆"),
    st.Page("pages/concentration.py", title="Concentration & Risk", icon="⚠️"),
    st.Page("pages/ask_the_data.py", title="Ask the Data", icon="🤖"),
]

st.navigation(pages).run()
