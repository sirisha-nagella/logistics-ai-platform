from utils.data_loader import load_data
from dashboard.driver_analysis import (
    revenue_by_product_group,
    revenue_by_vendor
)
df = load_data("data/supply_chain_data.csv")

result = revenue_by_product_group(df)

print(result.head(10))

vendor_df = revenue_by_vendor(df)

print(vendor_df.head(10))


