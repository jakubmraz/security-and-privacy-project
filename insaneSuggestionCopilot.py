import pandas as pd

# Load the datasets
dataset1 = pd.read_excel('data/new/differentially_private_dataD.xlsx')
#dataset1 = pd.read_excel("data/old/private_dataD.xlsx")
dataset2 = pd.read_excel("data/old/public_data_registerD.xlsx")

for dataset in [dataset1, dataset2]:
    for col in dataset.columns:
        if pd.api.types.is_datetime64_any_dtype(dataset[col]):
            print(f"The '{col}' column is of datetime type.")
            dataset[col] = pd.DatetimeIndex(dataset[col]).year
            # Your code to execute if 'dob' is datetime
        else:
            print(f"The '{col}' column is not of datetime type.")
            # Your code to execute if 'dob'







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

print(f'Re-identification rate: {reidentification_rate:.2f}%')