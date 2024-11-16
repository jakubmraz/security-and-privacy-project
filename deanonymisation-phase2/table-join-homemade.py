import pandas as pd

# Load the datasets
anonymized_data = pd.read_csv(r'deanonymisation-phase2/data/old/anonymized_dataZ.csv')
public_data = pd.read_excel(r'deanonymisation-phase2/data/new/variable_adjusted_filtered_data_registerZ.xlsx')
 

anonymized_data.drop(columns=['evote', 'education'], inplace=True)

# Group by all columns except 'party'
grouped = anonymized_data.groupby([col for col in anonymized_data.columns if col != 'party'])

# Filter groups where all rows within the group have the same 'party' value
valid_duplicates = grouped.filter(lambda x: x['party'].nunique() == 1)

# Group by all columns including 'party' and filter duplicates
duplicates = valid_duplicates.groupby(list(valid_duplicates.columns)).filter(lambda x: len(x) > 1)

# Drop exact duplicates to get unique duplicate rows
unique_duplicates = duplicates.drop_duplicates()

# Convert to a list of dictionaries
duplicates_list = unique_duplicates.to_dict(orient='records')

# Convert duplicates_list to DataFrame
duplicates_df = pd.DataFrame(duplicates_list)

# Perform an inner join on the specified columns
matching_entries = pd.merge(
    public_data,
    duplicates_df,
    on=['sex', 'citizenship', 'marital_status', 'age_group'],
    how='inner'
)

# Select the desired columns
result = matching_entries[['name', 'sex', 'citizenship', 'marital_status', 'party', 'age_group']]

# Convert the result to a list of dictionaries
matching_list = result.to_dict(orient='records')

# Display the number of matches and the matching entries
print(f"Number of matching entries: {len(matching_list)}")
result.to_excel(r'deanonymisation-phase2/data/new/deanonymizedZ.xlsx', index=False)


