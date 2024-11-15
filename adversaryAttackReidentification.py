import pandas as pd
from itertools import combinations

# Load the datasets
dataset1 = pd.read_excel('data/old/private_dataD.xlsx')
dataset2 = pd.read_excel("data/old/public_data_registerD.xlsx")

for dataset in [dataset1, dataset2]:
    for col in dataset.columns:
        if pd.api.types.is_datetime64_any_dtype(dataset[col]):
            dataset[col] = pd.DatetimeIndex(dataset[col]).year

# Identify common attributes
common_attributes = list(set(dataset1.columns) & set(dataset2.columns))

# Match records based on common attributes
matches = 0
for index, row in dataset1.iterrows():
    match = dataset2[(dataset2[common_attributes] == row[common_attributes]).all(axis=1)]
    if not match.empty:
        matches += 1

# Calculate re-identification rate
reidentification_rate = (matches / len(dataset1)) * 100

# Calculate k-anonymity
grouped = dataset1.groupby(common_attributes).size()
k_anonymity = grouped.min()

# Display the results
print(f'Re-identification rate: {reidentification_rate:.2f}%', matches)
print(f'k-anonymity: {k_anonymity}')