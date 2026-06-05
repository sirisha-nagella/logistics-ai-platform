from utils.data_loader import load_data
import pandas as pd

df = load_data("data/supply_chain_data.csv")

df["delivery_recorded_date"] = pd.to_datetime(
    df["delivery_recorded_date"],
    format="%d-%b-%y"
)

df["year_month"] = (
    df["delivery_recorded_date"]
    .dt.to_period("M")
    .dt.to_timestamp()
)

monthly_df = (
    df.groupby("year_month", as_index=False)
    ["line_item_value"]
    .sum()
)

monthly_df.columns = [
    "date",
    "revenue"
]

print(monthly_df.head())
print(monthly_df.tail())

monthly_df.to_csv(
    "data/monthly_revenue.csv",
    index=False
)