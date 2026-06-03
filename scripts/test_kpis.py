from utils.data_loader import load_data
from dashboard.kpi_calculator import calculate_kpis

df = load_data("data/supply_chain_data.csv")

kpis = calculate_kpis(df)

print(kpis)
