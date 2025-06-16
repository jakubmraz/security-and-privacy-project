import pandas as pd
"""
This script performs record linkage between anonymized data and public data based on common attributes
and infers vote preferences from the matched records.
Functions:
    - Load the datasets from CSV and Excel files.
    - Identify common attributes between the datasets.
    - Match records based on common attributes.
    - Check vote preferences in the matched records.
    - Display the matches with inferred vote preferences.
    - Calculate and display match confidence.
Variables:
    - anonymized_data (DataFrame): The anonymized dataset loaded from a CSV file.
    - public_data (DataFrame): The public dataset loaded from an Excel file.
    - common_attributes (list): List of common attributes between the anonymized and public datasets.
    - matches (list): List of dictionaries containing matched records and inferred vote preferences.
    - match_confidence (float): The percentage of public records that were successfully matched.
Usage:
    Run the script to perform record linkage and infer vote preferences. The results will be printed to the console.
"""

# Load the datasets
anonymized_data = pd.read_csv(r'deanonymisation-phase2/data/old/anonymized_dataZ.csv')
public_data = pd.read_excel(r'deanonymisation-phase2/data/new/variable_adjusted_filtered_data_registerZ.xlsx')


# Identify common attributes
common_attributes = list(set(anonymized_data.columns) & set(public_data.columns))

# Match records based on common attributes and check vote preference
matches = []  # Initialize an empty list to store matches
for index, public_row in public_data.iterrows():  # Iterate over each row in the public data
    potential_matches = anonymized_data[(anonymized_data[common_attributes] == public_row[common_attributes]).all(axis=1)]  # Find potential matches in the anonymized data based on common attributes
    if not potential_matches.empty:  # Check if there are any potential matches
        if 'party' in potential_matches.columns:  # Check if the 'party' column exists in the potential matches
            vote_preferences = potential_matches['party'].unique()  # Get the unique vote preferences from the potential matches
            if len(vote_preferences) == 1:  # Check if there is only one unique vote preference
                match = {  # Create a match dictionary
                    'public_index': index,  # Store the index of the public data row
                    'anon_index': potential_matches.index.tolist(),  # Store the indices of the potential matches in the anonymized data
                    'public_data': public_row.to_dict(),  # Convert the public data row to a dictionary and store it
                    'anon_records': potential_matches.to_dict('records'),  # Convert the potential matches to a list of dictionaries and store it
                    'vote_preference': vote_preferences[0]  # Store the unique vote preference
                }
                matches.append(match)  # Add the match dictionary to the matches list

# Display the matches with inferred vote preferences
    print(f"Public Index: {match['public_index']}, Anonymized Indices: {match['anon_index']}")
    print(f"Public Index: {match['public_index']}, Anonymized Indices: {match['anon_index']}")
    print(f"Public Data: {match['public_data']}")
    print(f"Anonymized Data: {match['anon_records']}")
    print(f"Inferred Vote Preference: {match['vote_preference']}")
    print()

# Calculate match confidence
match_confidence = len(matches) / len(public_data) * 100
print(f'Match confidence: {match_confidence:.2f}%')