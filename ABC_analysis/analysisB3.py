import pandas as pd
import matplotlib.pyplot as plt

PATH = r"data/new/synthetic_dataD.xlsx"

# Load the Excel sheet into a DataFrame
df = pd.read_excel(PATH, sheet_name='Sheet1')

# Demographic attributes to analyze: sex, age, zipcode, education, citizenship, marital status

# Sex
vote_counts = df[df['party'].isin(['Green', 'Red', 'Invalid Vote'])] \
    .groupby('sex')['party'].value_counts(normalize=True).mul(100).unstack()
print("VOTING TRENDS BY GENDER\n" + str(vote_counts))

# Age
df['age'] = 2024 - df['dob']

red_voters = df[df['party'] == 'Red']
green_voters = df[df['party'] == 'Green']

# Prepare data for Zipcode, Education, Citizenship, and Marital status
df_filtered = df[df['party'].isin(['Green', 'Red'])]

# Zipcode
vote_counts_by_zipcode = df_filtered.groupby('zip')['party'].value_counts(normalize=True).mul(100).unstack()
print(vote_counts_by_zipcode)

# Education
vote_counts_by_education = df_filtered.groupby('education')['party'].value_counts(normalize=True) \
    .mul(100).unstack().fillna(0)
vote_counts_by_education = vote_counts_by_education.sort_values(by='Green', ascending=False)

# Marital status
vote_counts_by_marital = df_filtered.groupby('marital_status')['party'].value_counts(normalize=True) \
    .mul(100).unstack().fillna(0)
vote_counts_by_marital = vote_counts_by_marital.sort_values(by='Green', ascending=False)

# Create a figure with multiple subplots
fig, axs = plt.subplots(2, 2, figsize=(16, 12))

# First subplot: Age Distribution
axs[0, 0].hist(red_voters['age'], bins=20, alpha=0.5, label='Red', color='red')
axs[0, 0].hist(green_voters['age'], bins=20, alpha=0.5, label='Green', color='green')
axs[0, 0].set_title('Age Distribution of Voters by Party (Red vs Green)')
axs[0, 0].set_xlabel('Age')
axs[0, 0].set_ylabel('Number of Voters')
axs[0, 0].legend()

# Second subplot: Voting Trends by Education Level
vote_counts_by_education[['Green', 'Red']].plot(kind='bar', ax=axs[0, 1], color=['green', 'red'])
axs[0, 1].set_title('Voting Trends by Education Level (Green vs Red)')
axs[0, 1].set_xlabel('Education Level')
axs[0, 1].set_ylabel('Percentage of Voters')
axs[0, 1].legend(title='Party')
axs[0, 1].tick_params(axis='x', rotation=45)

# Fourth subplot: Voting Trends by Marital Status
vote_counts_by_marital[['Green', 'Red']].plot(kind='bar', ax=axs[1, 1], color=['green', 'red'])
axs[1, 1].set_title('Voting Trends by Marital Status (Green vs Red)')
axs[1, 1].set_xlabel('Marital Status')
axs[1, 1].set_ylabel('Percentage of Voters')
axs[1, 1].legend(title='Party')
axs[1, 1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()
