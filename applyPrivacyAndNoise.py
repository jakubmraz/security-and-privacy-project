import pandas as pd
import numpy as np

PATH = r"even_more_private_dataD.xlsx"
NEW = r"differentially_private_dataD.xlsx"

# Load the Excel sheet into a DataFrame
df = pd.read_excel(PATH, sheet_name='Sheet1')

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
