import pandas as pd
from pydriller import Repository, ModificationType
import os


def get_later_commits(repo_url, commit_hash, file_path):

    print(f"Processing {repo_url} - Commit: {commit_hash}")

    found_commit = False
    commits = []

    for commit in Repository(repo_url, only_no_merge=True).traverse_commits():
        modified_files = [file for file in commit.modified_files if file.change_type == ModificationType.MODIFY]

        for mod in modified_files:
            if mod.filename == file_path:
                if commit.hash == commit_hash:
                    found_commit = True
                if found_commit:
                    commits.append({
                        "repo_url": repo_url,
                        "commit_hash": commit.hash,
                        "author": commit.author.name,
                        "date": commit.author_date,
                        "msg": commit.msg,
                        "file": file_path,
                        "diff": mod.diff,
                        "after": mod.source_code
                    })

    return commits


def process_csv(input_csv, output_csv):

    df = pd.read_csv(input_csv)

    if os.path.exists(output_csv):
        existing_df = pd.read_csv(output_csv)
    else:
        existing_df = pd.DataFrame()

    all_commits = []

    for _, row in df.iterrows():
        repo_url = row["URL"]
        commit_hash = row["Commit"]
        file_path = row["File"]

        modifying_commits = get_later_commits(repo_url, commit_hash, file_path)

        if modifying_commits:
            new_df = pd.DataFrame(modifying_commits)

            if not existing_df.empty:
                new_df = new_df[~new_df["commit_hash"].isin(existing_df["commit_hash"])]

            if not new_df.empty:
                new_df.to_csv(output_csv, mode='a', header=not os.path.exists(output_csv), index=False)
                print(f"Saved {len(new_df)} New commit per {repo_url}")


input_csv = "commits_with_dates.csv"
output_csv = "modified_files_commits.csv"
process_csv(input_csv, output_csv)
