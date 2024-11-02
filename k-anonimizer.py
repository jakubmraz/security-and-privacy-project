import pandas as pd

def load_data(file_path):
    # Load the Excel file
    return pd.read_excel(file_path)

def apply_k_anonymity(df, key_columns, k):
    # Create a copy of the DataFrame to avoid modifying the original
    modified_df = df.copy()

    # Group by key_columns to check counts
    group_counts = modified_df.groupby(key_columns).size().reset_index(name='count')

    # Identify rows that do not meet k-anonymity
    for index, row in group_counts.iterrows():
        if row['count'] < k:
            # Modify attributes to achieve k-anonymity
            # Create a condition based on the values in the row
            condition = (modified_df[key_columns] == row[key_columns].values).all(axis=1)
            modified_df.loc[condition, 'dob'] = None

    return modified_df

# Load your data
file_path = 'even_more_private_dataD.xlsx'  # Replace with your file path
data = load_data(file_path)

# Specify the columns that constitute the key for k-anonymity
key_columns = ['dob', 'education', 'citizenship', 'zip', 'marital_status', 'sex']
k = 3  # Set your desired k-anonymity level

# Apply k-anonymity
anonymized_data = apply_k_anonymity(data, key_columns, k)

# Save the anonymized data to a new Excel file
anonymized_data.to_excel('even_more_and_more_private_data.xlsx', index=False)

# Assume the code does its job


