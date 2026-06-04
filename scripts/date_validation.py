from utils.data_loader import load_data
from utils.date_utils import parse_delivery_dates

df = load_data("data/supply_chain_data.csv")

df = parse_delivery_dates(df)

print(df["delivery_recorded_date"].min())
print(df["delivery_recorded_date"].max())

print(
    df["delivery_recorded_date"]
    .isna()
    .sum()
)
