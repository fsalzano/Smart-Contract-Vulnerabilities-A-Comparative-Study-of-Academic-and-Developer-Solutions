import pandas as pd
#this script is used to extract fixes that are not known in the available literature
# Read the CSV file
df = pd.read_csv('../sample_of_interest/relevant_commits.csv')

# Filter rows where 'IsInLiteratureTag1' is False
filtered_df = df[df['IsInLiterature'] == False]

# Write the filtered rows to a new CSV file
filtered_df.to_csv('untracked_fixes.csv', index=False)

print(f"Filtered rows written to 'untracked_fixes.csv'")
