
import pandas as pd

from utils.data_loader import load_data


#Load dataset
df = load_data("data/supply_chain_data.csv")
#df = pd.read_csv("data/supply_chain_data.csv")

#Display basic Information
print("\nDataset Shape:")
print(df.shape)

print("\nColumn Names:")
print(df.columns)

print("\nFirst 5 Rows:")
print(df.head())

print("\nData Types:")
print(df.dtypes)

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Rows:")
print(df.duplicated().sum())

