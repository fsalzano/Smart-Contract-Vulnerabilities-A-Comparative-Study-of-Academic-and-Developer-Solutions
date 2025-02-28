import pandas as pd
from pydriller import Repository, ModificationType



def get_later_commits(repo_url, commit_hash, file_path, commit_date):
    """
    Trova tutte le commit successive alla commit specificata
    che hanno modificato il file dato, escludendo le merge commit.
    """

    print(repo_url)
    if not commit_date:
        print(f"Commit {commit_hash} non trovata nel repository {repo_url}")
        return []

    commits = []
    for commit in Repository(repo_url, only_no_merge=True, since=commit_date, only_modifications_with_file_types=['.sol']).traverse_commits():
        modified_files = [file for file in commit.modified_files if file.change_type == ModificationType.MODIFY]
        for mod in modified_files:

            if mod.filename == file_path :
                commits.append({
                    "commit_hash": commit.hash,
                    "author": commit.author.name,
                    "date": commit.author_date,
                    "msg": commit.msg,
                    "file": file_path
                })
    return commits


def process_csv(input_csv, output_csv):
    """
    Legge il CSV di input, analizza le commit successive e salva i risultati in un CSV di output.
    """
    df = pd.read_csv(input_csv)
    all_commits = []
    df["Commit Date"] = pd.to_datetime(df["Commit Date"], errors='coerce', utc=True)  # Convert string to datetime

    for _, row in df.iterrows():
        repo_url = row["URL"]
        commit_hash = row["Commit"]
        file_path = row["File"]
        date = row["Commit Date"]

        later_commits = get_later_commits(repo_url, commit_hash, file_path, date)
        all_commits.extend(later_commits)

    result_df = pd.DataFrame(all_commits)
    result_df.to_csv(output_csv, index=False)
    print(f"Risultati salvati in {output_csv}")


# Esempio di utilizzo
input_csv = "commits_with_dates.csv"  # Nome del file CSV in input
output_csv = "modified_files_commits.csv"  # Nome del file CSV in output
process_csv(input_csv, output_csv)
