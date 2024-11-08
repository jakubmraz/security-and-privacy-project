import pandas as pd

PATH = r"data/new/synthetic_dataD.xlsx"
K = 2

df = pd.read_excel(PATH, sheet_name='Sheet1')

# List of quasi-identifiers to check for k-anonymity
quasi_identifiers = ['sex', 'dob', 'education', 'marital_status', 'zip']

# Group by quasi-identifiers and count occurrences
grouped = df.groupby(quasi_identifiers).size().reset_index(name='count')

# Identify groups that violate k=K anonymity
violations = grouped[grouped['count'] < K]

# Print results
num_violations = len(violations)
print(f"Number of entries violating k={K} anonymity: {num_violations}")

if num_violations > 0:
    print("Details of violating entries:")
    print(violations)

# Save the violating entries to a CSV file (optional)
violations.to_csv("violating_entries.csv", index=False)