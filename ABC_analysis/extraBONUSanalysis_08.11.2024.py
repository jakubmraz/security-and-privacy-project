import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Load the Excel file
file_path = 'data/new/synthetic_dataD.xlsx'  # Replace with the actual file path
df = pd.read_excel(file_path)

# Data preprocessing (e.g., converting columns to appropriate data types)
df['dob'] = pd.to_numeric(df['dob'], errors='coerce')  # Convert year of birth to numeric
df['age'] = 2024 - df['dob']  # Calculate age assuming the data collection year is 2024

# Set up the plotting style
sns.set(style="whitegrid")

# Plot 1: Distribution of political preferences by gender
party_gender_table = pd.crosstab(df['party'], df['sex'])
party_gender_table.plot(kind='bar', stacked=True)
plt.title('Political Preferences by Gender')
plt.xlabel('Party')
plt.ylabel('Count')
plt.legend(title='Gender')
plt.tight_layout()
plt.show()

# Plot 2: Distribution of voting method by education level
evote_edu_table = pd.crosstab(df['evote'], df['education'])
evote_edu_table.plot(kind='bar', stacked=True)
plt.title('Choice of Voting Method by Education Level')
plt.xlabel('E-vote (0 = In-person, 1 = Online)')
plt.ylabel('Count')
plt.legend(title='Education Level')
plt.tight_layout()
plt.show()

# Plot 3: Age distribution for e-voters vs. in-person voters
plt.figure(figsize=(10, 6))
sns.histplot(evote_age_group, color='blue', label='E-voters', kde=True, bins=20)
sns.histplot(in_person_age_group, color='orange', label='In-person Voters', kde=True, bins=20)
plt.title('Age Distribution Comparison Between E-voters and In-person Voters')
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.legend()
plt.tight_layout()
plt.show()
