import pandas as pd

# Load the data from the Excel file
data = pd.read_excel("D:\\Documents\\Documents\\Uni\\Security_Privacy\\final_project\\security-and-privacy-project\\even_more_private_dataD.xlsx")

# Specify the key variables (quasi-identifiers) and sensitive variables
key_vars = ['dob', 'education', 'citizenship', 'zip', 'marital_status', 'sex']
sensitive_var = 'party'

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

# Display the results
print(f"Risk of re-identification: {risk_of_reidentification}")
print("Count per unique combination:")
print(count_per_combination)
print(f"Overall risk: {overall_risk}")
