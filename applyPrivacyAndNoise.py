import pandas as pd
import numpy as np

PATH = r"private_dataD.xlsx"
NEW = r"differentially_private_dataD.xlsx"

# Load the Excel sheet into a DataFrame
df = pd.read_excel(PATH, sheet_name='Sheet 1')

# Apply initial transformations
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

# Drop the 'name' column and log the removal
if 'name' in df.columns:
    df.drop(columns=['name'], inplace=True)
    print(f"The 'name' column has been removed.")

# Add differential privacy after transformations
epsilon = 1.0  # Privacy budget for noise addition

# Add noise to 'dob' using the Laplace mechanism
def add_laplace_noise(value, sensitivity=1, epsilon=1.0):
    scale = sensitivity / epsilon
    noise = np.random.laplace(0, scale)
    return value + noise

df['dob'] = df['dob'].apply(lambda x: int(add_laplace_noise(x, epsilon=epsilon)) if pd.notnull(x) else x)

# Apply randomized response to 'citizenship' and 'marital status' after transformations
def randomize_response(value, true_value, epsilon=1.0):
    probability = np.exp(epsilon) / (np.exp(epsilon) + 1)
    return true_value if np.random.rand() < probability else value

df['citizenship'] = df['citizenship'].apply(lambda x: randomize_response("Foreign", x, epsilon=epsilon) if x != "Denmark" else x)
df['marital_status'] = df['marital_status'].apply(lambda x: randomize_response("Single", x, epsilon=epsilon))

# Save the modified DataFrame to a new .xlsx file
df.to_excel(NEW, index=False)
