import pandas as pd

PATH = r"private_dataD.xlsx"
NEW = r"even_more_private_dataD.xlsx"

# Load the Excel sheet into a DataFrame
df = pd.read_excel(PATH, sheet_name='Sheet 1')

# Replace non-Denmark citizenships with "Foreign"
df['citizenship'] = df['citizenship'].apply(lambda x: "Foreign" if x != "Denmark" else x)

# Combine non-university education levels
df['education'] = df['education'].apply(
    lambda x: "Non-university" if x in ["Not stated", "Primary education", "Vocational Education and Training (VET)", "Upper secondary education"] else (
        "Undergraduate" if x in ["Bachelors programmes", "Short cycle higher education"] else x
    )
)

# Ensure the 'dob' column is a datetime object (if not, convert it)
if not pd.api.types.is_datetime64_any_dtype(df['dob']):
    df['dob'] = pd.to_datetime(df['dob'], errors='coerce')

# Replace 'dob' with the modified integer year, rounded down to 3-year intervals
df['dob'] = df['dob'].apply(lambda x: int(x.year) - int(x.year) % 3 if pd.notnull(x) else x)

# Cap all ages above 75 to the year corresponding to 75 (e.g., birth year <= 1949)
df['dob'] = df['dob'].apply(lambda x: 1949 if pd.notnull(x) and x < 1949 else x)

# Save the modified DataFrame to a new .xlsx file
df.to_excel(NEW, index=False)
