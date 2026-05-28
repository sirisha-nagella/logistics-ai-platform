from utils.data_loader import load_data

#Load dataset
df = load_data("data/supply_chain_data.csv")

#Standardize column nmaes

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ","_")
)

print("\nCleaned Column Names:")
print(df.columns.tolist())

print("\nData Types:")
print(df.dtypes)

print("\nSummary Statistics:")
print(df.descripbe())

df.to_csv("data/cleaned_supply_chain_data.csv", index=False)

print("\nCleaned dataset saved.")

