import pandas as pd
from pydriller import Repository, ModificationType

# Load the dataset
df = pd.read_csv("../repo_stats.csv")

# Check the available columns
print("Available columns:", df.columns)

# Filter repos with at least 50 commits
df_filtered = df[df['Commits'] >= 50]

# Take a random sample of 10a
#random_sample = df_filtered.sample(n=10, random_state=42)
#random_sample.to_csv("random_sample_for_NLP-filter_recall_evaluation.csv", index=False)
df_sample=pd.read_csv("random_sample_for_NLP-filter_recall_evaluation.csv")

commit_data = []

# Iterate over each repository URL
for index, row in df_sample.iterrows():
    repo_url = row["URL"]
    print(f"⛏️ Mining repo: {repo_url}")

    try:
        for commit in (Repository(repo_url, only_modifications_with_file_types=['.sol'], only_no_merge=True)
                .traverse_commits()):

            if not commit.merge:  # Exclude merge commits
                commit_data.append({
                    "repo_url": repo_url,
                    "commit_hash": commit.hash,
                    "message": commit.msg
                })
    except Exception as e:
        print(f"❌ Failed to mine {repo_url}: {e}")

# Create DataFrame from mined commits
df_commits = pd.DataFrame(commit_data)

# Save to CSV
df_commits.to_csv("mined_commits_from_random_sample.csv", index=False)

sample_size = min(400, len(df_commits))
random_sample = df_commits.sample(n=sample_size, random_state=42)

# Save to CSV
random_sample.to_csv("random_commit_sample.csv", index=False)
print("✅ Saved mined commit data (excluding merges) to mined_commits_from_random_sample.csv")

