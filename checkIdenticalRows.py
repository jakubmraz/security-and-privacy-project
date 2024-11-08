import pandas as pd

# Load the original and synthetic datasets
original_file_path = 'data/new/even_more_private_dataD.xlsx'  # Original dataset
synthetic_file_path = 'data/new/synthetic_dataD.xlsx'  # Synthetic dataset

original_data = pd.read_excel(original_file_path)
synthetic_data = pd.read_excel(synthetic_file_path)

# Find identical rows between the original and synthetic datasets
identical_rows = pd.merge(original_data, synthetic_data, how='inner')

# Display the result
if identical_rows.empty:
    print("No identical rows found between the original and synthetic datasets.")
else:
    print(f"Found {len(identical_rows)} identical rows:")
    print(identical_rows)
