import pandas as pd
import matplotlib.pyplot as plt

PATH = r"even_more_private_dataD.xlsx"

# Load the Excel sheet into a DataFrame
df = pd.read_excel(PATH, sheet_name='Sheet1')

# Demographic attributes to analyze: sex, age, zipcode, education, citizenship, marital status

# Sex
vote_counts = df[df['evote'].isin([0, 1])] \
    .groupby('sex')['evote'].value_counts(normalize=True).mul(100).unstack()
print("VOTING TRENDS BY GENDER\n" + str(vote_counts))

# Age
df['age'] = 2024 - df['dob']

e_voters = df[df['evote'] == 1]
person_voters = df[df['evote'] == 0]

# Prepare data for Zipcode, Education, Citizenship, and Marital status
df_filtered = df[df['evote'].isin([0, 1])]

# Zipcode
vote_counts_by_zipcode = df_filtered.groupby('zip')['evote'].value_counts(normalize=True).mul(100).unstack()
print(vote_counts_by_zipcode)

# Education
vote_counts_by_education = df_filtered.groupby('education')['evote'].value_counts(normalize=True) \
    .mul(100).unstack().fillna(0)
vote_counts_by_education = vote_counts_by_education.sort_values(by=1, ascending=False)

# Citizenship
vote_counts_by_citizenship = df_filtered.groupby('citizenship')['evote'].value_counts(normalize=False) \
    .unstack().fillna(0)
vote_counts_by_citizenship = vote_counts_by_citizenship.sort_values(by=1, ascending=False)

# Marital status
vote_counts_by_marital = df_filtered.groupby('marital_status')['evote'].value_counts(normalize=True) \
    .mul(100).unstack().fillna(0)
vote_counts_by_marital = vote_counts_by_marital.sort_values(by=1, ascending=False)

# Create a figure with multiple subplots
fig, axs = plt.subplots(2, 2, figsize=(16, 12))

# First subplot: Age Distribution
axs[0, 0].hist(e_voters['age'], bins=20, alpha=0.5, label='E-voters', color='blue')
axs[0, 0].hist(person_voters['age'], bins=20, alpha=0.5, label='In-person voters', color='yellow')
axs[0, 0].set_title('Age Distribution of Voters by voting method')
axs[0, 0].set_xlabel('Age')
axs[0, 0].set_ylabel('Number of Voters')
axs[0, 0].legend()

# Second subplot: Voting Trends by Education Level
vote_counts_by_education[[1, 0]].plot(kind='bar', ax=axs[0, 1], color=['blue', 'yellow'])
axs[0, 1].set_title('Voting Trends by Education Level')
axs[0, 1].set_xlabel('Education Level')
axs[0, 1].set_ylabel('Percentage of Voters')
axs[0, 1].legend(title='Voting Method')
axs[0, 1].tick_params(axis='x', rotation=45)

# Third subplot: Voting Trends by Citizenship
vote_counts_by_citizenship[[1, 0]].plot(kind='bar', ax=axs[1, 0], color=['blue', 'yellow'])
axs[1, 0].set_title('Voting Trends by Citizenship')
axs[1, 0].set_xlabel('Citizenship')
axs[1, 0].set_ylabel('Number of Voters')
axs[1, 0].legend(title='Voting Method')
axs[1, 0].tick_params(axis='x', rotation=45)

# Fourth subplot: Voting Trends by Marital Status
vote_counts_by_marital[[1, 0]].plot(kind='bar', ax=axs[1, 1], color=['blue', 'yellow'])
axs[1, 1].set_title('Voting Trends by Marital Status')
axs[1, 1].set_xlabel('Marital Status')
axs[1, 1].set_ylabel('Percentage of Voters')
axs[1, 1].legend(title='Voting Method')
axs[1, 1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()
