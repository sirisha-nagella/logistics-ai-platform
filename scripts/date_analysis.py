import pandas as pd

from utils.data_loader import load_data

df = load_data("data/supply_chain_data.csv")

date_columns = [
    "pq_first_sent_to_client_date",
    "po_sent_to_vendor_date",
    "scheduled_delivery_date",
    "delivered_to_client_date",
    "delivery_recorded_date"
]

for col in date_columns:
    print(f"\n{col}")
    print(df[col].head())


# Parse the columns that actually hold dates ("%d-%b-%y", e.g. 2-Jun-06)
parseable_columns = [
    "scheduled_delivery_date",
    "delivered_to_client_date",
    "delivery_recorded_date"
]

total = len(df)
print("\n\n=== Parsed date summary (format='%d-%b-%y') ===")

for col in parseable_columns:
    parsed = pd.to_datetime(df[col], format="%d-%b-%y", errors="coerce")
    valid = parsed.notna().sum()
    nat = parsed.isna().sum()
    print(f"\n{col}")
    print(f"  valid dates : {valid:,} / {total:,} ({valid / total:.1%})")
    print(f"  NaT (bad)   : {nat:,}")
    if valid:
        print(f"  range       : {parsed.min().date()}  ->  {parsed.max().date()}")
