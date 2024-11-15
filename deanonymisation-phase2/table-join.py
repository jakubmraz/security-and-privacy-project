import pandas as pd

# Load the datasets
anonymized_data = pd.read_csv(r'deanonymisation-phase2/data/old/anonymized_dataZ.csv')
public_data = pd.read_excel('data/new/variable_adjusted_filtered_data_registerZ.xlsx')

# Identify common attributes
common_attributes = list(set(anonymized_data.columns) & set(public_data.columns))

# Match records based on common attributes and check vote preference
matches = []
for index, public_row in public_data.iterrows():
    potential_matches = anonymized_data[(anonymized_data[common_attributes] == public_row[common_attributes]).all(axis=1)]
    if not potential_matches.empty:
        vote_preferences = potential_matches['party'].unique()
        if len(vote_preferences) == 1:
            match = {
                'public_index': index,
                'anon_index': potential_matches.index.tolist(),
                'public_data': public_row.to_dict(),
                'anon_data': potential_matches.to_dict('records'),
                'vote_preference': vote_preferences[0]
            }
            matches.append(match)

# Display the matches with inferred vote preferences
for match in matches:
    print(f"Public Index: {match['public_index']}, Anonymized Indices: {match['anon_index']}")
    print(f"Public Data: {match['public_data']}")
    print(f"Anonymized Data: {match['anon_data']}")
    print(f"Inferred Vote Preference: {match['vote_preference']}")
    print()

# Calculate match confidence
match_confidence = len(matches) / len(public_data) * 100
print(f'Match confidence: {match_confidence:.2f}%')