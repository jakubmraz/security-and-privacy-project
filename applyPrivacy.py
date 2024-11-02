import pandas as pd

PATH = r"private_dataD.xlsx"
NEW = r"even_more_private_dataD.xlsx"

# Load the Excel sheet into a DataFrame
df = pd.read_excel(PATH, sheet_name='Sheet 1')

# Track the number of changes for each operation
citizenship_changes = (df['citizenship'] != "Denmark").sum()

# Replace non-Denmark citizenships with "Foreign"
df['citizenship'] = df['citizenship'].apply(lambda x: "Foreign" if x != "Denmark" else x)

# Log the number of rows modified for citizenship
print(f"{citizenship_changes} rows were modified for citizenship")

# Track changes for education
original_education = df['education'].copy()
df['education'] = df['education'].apply(
    lambda x: "Non-university" if x in ["Not stated", "Primary education", "Vocational Education and Training (VET)", "Upper secondary education"] else (
        "Undergraduate" if x in ["Bachelors programmes", "Short cycle higher education"] else x
    )
)
education_changes = (original_education != df['education']).sum()

# Log the number of rows modified for education
print(f"{education_changes} rows were modified for education")

# Ensure the 'dob' column is a datetime object (if not, convert it)
if not pd.api.types.is_datetime64_any_dtype(df['dob']):
    df['dob'] = pd.to_datetime(df['dob'], errors='coerce')

# Track changes for 'dob'
original_dob = df['dob'].copy()
df['dob'] = df['dob'].apply(lambda x: int(x.year) - int(x.year) % 3 if pd.notnull(x) else x)
dob_changes_rounding = (original_dob != df['dob']).sum()

# Cap all ages above 75 to the year corresponding to 75 (e.g., birth year <= 1949)
dob_changes_capping = ((df['dob'] < 1949) & pd.notnull(df['dob'])).sum()
df['dob'] = df['dob'].apply(lambda x: 1949 if pd.notnull(x) and x < 1949 else x)

# Log the number of rows modified for date of birth
print(f"{dob_changes_rounding} rows were modified for date of birth (rounded)")
print(f"{dob_changes_capping} rows were capped at the year 1949 for date of birth")

# Drop the 'name' column and log the removal
if 'name' in df.columns:
    df.drop(columns=['name'], inplace=True)
    print(f"The 'name' column has been removed.")

# Save the modified DataFrame to a new .xlsx file
df.to_excel(NEW, index=False)
