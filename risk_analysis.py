import pandas as pd

# Load the data from the Excel file
data = pd.read_excel("differentially_private_dataD.xlsx")

# Specify the key variables (quasi-identifiers) and sensitive variables
key_vars = ['dob', 'education', 'citizenship', 'zip', 'marital_status', 'sex']
sensitive_var = 'party'

# Convert all key variables to string type to avoid mixed type issues
data[key_vars] = data[key_vars].astype(str)

# Calculate unique combinations of key variables
unique_combinations = data[key_vars].drop_duplicates()

# Calculate risk metrics
# 1. Count the number of unique combinations
risk_of_reidentification = unique_combinations.shape[0]

# 2. Calculate the number of records for each unique combination
count_per_combination = data[key_vars].value_counts()

# 3. Calculate the risk for each unique combination (1 / count)
risk_per_combination = 1 / count_per_combination

# 4. Calculate overall risk
overall_risk = risk_per_combination.mean()

# Additional Metrics
# 5. Frequency of each key variable
frequency_key_vars = data[key_vars].apply(lambda x: x.value_counts())

# 6. Risk of unique values in key variables
risk_per_key_variable = {key: 1 / data[key].value_counts() for key in key_vars}

# 7. Cumulative risk across key variables
cumulative_risk = risk_per_combination.sum()

# 8. Count of sensitive variables per unique combination
sensitive_counts = data.groupby(key_vars)[sensitive_var].nunique()

# Display the results
print(f"Risk of re-identification: {risk_of_reidentification}")
print("Count per unique combination:")
print(count_per_combination)
print(f"Overall risk: {overall_risk}")
print("\nFrequency of each key variable:")
print(frequency_key_vars)
print("\nRisk per unique value in key variables:")
for key, risk in risk_per_key_variable.items():
    print(f"{key} risk:\n{risk}\n")
print(f"Cumulative risk across key variables: {cumulative_risk}")
print("\nCount of sensitive variables per unique combination:")
print(sensitive_counts)