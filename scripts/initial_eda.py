
import pandas as pd

#Load dataset
df = pd.read_csv("data/SCMS_Delivery_History_Dataset.csv")

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

print("n\Duplicate Rows:")
print(df.duplicated().sum())

