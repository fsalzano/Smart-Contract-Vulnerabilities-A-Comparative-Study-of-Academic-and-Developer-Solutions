import pandas as pd

path = 'filtered_post_fixing_commit_dataset.csv'
df = pd.read_csv(path)

df = df[~df["is_fixing"].fillna(False)]

counts = df["motivation"].value_counts()
print(counts)
df.to_csv(path, index=False)
