import pandas as pd

pop_register_path = r"data/adversarial/public_data_registerZ.xlsx"
names_path = r"data/adversarial/survey_listZ.txt"
filtered_path = r'data/adversarial/filtered_data_registerZ.xlsx'

# Read the population register
pop_register = pd.read_excel(pop_register_path)

# Read the names into a list
with open(names_path, 'r') as f:
    names_list = [line.strip() for line in f]

# Filter based on the names list
filtered_pop_register = pop_register[pop_register['name'].isin(names_list)]
filtered_pop_register.reset_index(drop=True, inplace=True)

# Ensure the 'dob' column is formatted as date only (no time part)
filtered_pop_register['dob'] = filtered_pop_register['dob'].dt.date

# Save the filtered DataFrame to Excel
filtered_pop_register.to_excel(filtered_path, index=False)
