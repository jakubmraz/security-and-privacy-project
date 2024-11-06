import anonypy
import pandas as pd

# Load the dataset
data = pd.read_excel("data/new/even_more_private_dataD.xlsx")

# Drop the name column if it exists
#if 'name' in data.columns:
 #   data = data.drop("name", axis=1)

for col in data.columns:
    if pd.api.types.is_datetime64_any_dtype(data[col]):
        data[col] = pd.DatetimeIndex(data[col]).year



# Define columns and categorical columns
columns = data.columns.tolist()
categorical = set(["dob", "education", "citizenship", "zip", "marital_status"])

def k_anonimizer(feature_columns, sensitive_column, k=3):
    if sensitive_column not in data.columns:
        raise KeyError(f"Sensitive column '{sensitive_column}' does not exist in the dataset.")
    
    df = pd.DataFrame(data=data, columns=columns)

    for name in categorical:
        df[name] = df[name].astype("category")

    p = anonypy.Preserver(df, feature_columns, sensitive_column)
    rows = p.anonymize_k_anonymity(k=k)

    dfn = pd.DataFrame(rows)
    print(dfn)

    
    # Save the anonymized DataFrame to an Excel file
    dfn.to_excel("data/new/anonymized_data_from_generealisationAlgorithmy_k=3.xlsx", index=True)

# Define feature columns and sensitive column
feature_columns = ["dob", "education", "citizenship", "zip", "marital_status"]
sensitive_column = "party"  # Replace with the actual sensitive column name

# Ensure the sensitive column exists
if sensitive_column not in data.columns:
    raise KeyError(f"Sensitive column '{sensitive_column}' does not exist in the dataset.")

k_anonimizer(feature_columns, sensitive_column, 3)

