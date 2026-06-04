import streamlit as st


def apply_filters(df):

    st.sidebar.header("Dashboard Filters")

    # Country Filter
    countries = sorted(df["country"].dropna().unique())

    selected_country = st.sidebar.selectbox(
        "Country",
        ["All"] + countries
    )

    if selected_country != "All":
        df = df[df["country"] == selected_country]

    # Shipment Mode Filter
    shipment_modes = sorted(
        df["shipment_mode"]
        .fillna("Unknown")
        .unique()
    )

    selected_modes = st.sidebar.multiselect(
        "Shipment Mode",
        shipment_modes
    )

    if selected_modes:
        df = df[
            df["shipment_mode"]
            .fillna("Unknown")
            .isin(selected_modes)
        ]

    # Vendor Filter
    vendors = sorted(
        df["vendor"]
        .dropna()
        .unique()
    )

    selected_vendors = st.sidebar.multiselect(
        "Vendor",
        vendors
    )

    if selected_vendors:
        df = df[
            df["vendor"].isin(selected_vendors)
        ]

    return df
