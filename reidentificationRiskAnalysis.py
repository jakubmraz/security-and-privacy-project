import pandas as pd

# Read the transformed dataset and the population registry from Excel files
transformed_df = pd.read_excel('differentially_private_dataD.xlsx')
population_df = pd.read_excel('public_data_registerD.xlsx')

# Convert 'dob' in the population registry to datetime if it's not already
population_df['dob'] = pd.to_datetime(population_df['dob'], errors='coerce')

# Extract the year from 'dob' in the population registry
population_df['dob_year'] = population_df['dob'].dt.year

# In the transformed dataset, 'dob' is already the year; rename it for consistency
transformed_df.rename(columns={'dob': 'dob_year'}, inplace=True)

# Ensure 'dob_year' is of integer type
transformed_df['dob_year'] = transformed_df['dob_year'].astype(int)
population_df['dob_year'] = population_df['dob_year'].astype(int)

# Define the matching columns (quasi-identifiers)
matching_columns = ['sex', 'dob_year', 'zip', 'citizenship', 'marital_status']

# Group the population registry by the matching columns and count occurrences
population_grouped = population_df.groupby(matching_columns).size().reset_index(name='match_count')

# Merge the transformed dataset with the grouped population registry on the matching columns
merged_df = pd.merge(
    transformed_df,
    population_grouped,
    on=matching_columns,
    how='left'
)

# Fill NaN values in 'match_count' with 0 (no matches found)
merged_df['match_count'] = merged_df['match_count'].fillna(0)

# Determine if each record can be uniquely identified (match_count == 1)
merged_df['unique_match'] = merged_df['match_count'] == 1

# Count the number of records that can be uniquely identified
num_uniquely_identified = merged_df['unique_match'].sum()

print(f"Number of records that can be uniquely identified: {int(num_uniquely_identified)}")