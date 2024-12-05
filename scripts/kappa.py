import pandas as pd
from sklearn.metrics import cohen_kappa_score

# Read the CSV file
df = pd.read_csv('../sample_of_interest/relevant_commits.csv')

# Consider the columns Tag1 and Tag2
tag1 = df['Tag1']
tag2 = df['Tag2']

# Calculate Cohen's Kappa score between Tag1 and Tag2
relevance_commit_kappa = cohen_kappa_score(tag1, tag2)

is_in_literature_tag1 = df['IsInLiteratureTag1']
is_in_literature_tag2 = df['IsInLiteratureTag2']

is_in_literature_guidelines_kappa = cohen_kappa_score(is_in_literature_tag1, is_in_literature_tag2)

df_filtered = df[df['IsInLiteratureTag'] != True]
print(df_filtered.shape)

is_employable_tag1 = df_filtered['IsEmployableFixTag1']
is_employable_tag2 = df_filtered['IsEmployableFixTag2']

is_employable_tag1 = is_employable_tag1.astype(str)
is_employable_tag2 = is_employable_tag2.astype(str)


is_employable_kappa = cohen_kappa_score(is_employable_tag1, is_employable_tag2)

# Print the Cohen's Kappa score
print(f"Cohen's Kappa on commit relevance: {relevance_commit_kappa}")
print(f"Cohen's Kappa on literature adherence: {is_in_literature_guidelines_kappa}")
print(f"Cohen's Kappa on employable fixes analysis: {is_employable_kappa}")
