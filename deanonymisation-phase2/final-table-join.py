import pandas as pd

# Load the anonymized data
anonymized_data = pd.read_csv(r'deanonymisation-phase2/data/old/anonymized_dataZ.csv')

# Drop the 'evote' and 'education' columns
anonymized_data = anonymized_data.drop(columns=['evote', 'education'])

# Exclude the 'party' column to create combinations of non-party attributes
non_party_columns = ['sex', 'citizenship', 'marital_status', 'age_group']

# Group by all combinations of non-party attributes and count occurrences of each 'party'
aggregated_counts = anonymized_data.groupby(non_party_columns)['party'].value_counts().unstack(fill_value=0)

# Filter combinations where at least two of the three party counts are 0
filtered_combinations = aggregated_counts[(aggregated_counts == 0).sum(axis=1) >= 2].reset_index()

# Load the provided file with additional data
variable_adjusted_data = pd.read_excel(r'deanonymisation-phase2/data/new/variable_adjusted_filtered_data_registerZ.xlsx')

# Merge the filtered combinations with the new dataset
merged_data = pd.merge(
    filtered_combinations[non_party_columns], 
    variable_adjusted_data, 
    on=non_party_columns, 
    how='inner'
)

# Merge back with anonymized_data to get the 'party' column
final_result = pd.merge(
    merged_data, 
    anonymized_data[['party'] + non_party_columns], 
    on=non_party_columns, 
    how='left'
)

# Remove duplicate names before exporting
final_result = final_result.drop_duplicates(subset='name', keep='first')  # Assuming 'name' is the unique column

# Export the final result
final_result.to_excel('Filtered_Unique_Merged_Data.xlsx', index=False)

print("Filtered and uniquely merged data has been exported to 'Filtered_Unique_Merged_Data.xlsx'.")
