from pydriller import Repository, ModificationType
import pandas as pd
import spacy
import csv

# Load the SpaCy model
nlp = spacy.load("en_core_web_lg")

# Specific provided lemmas
fixing_keywords = ["fix", "fixed", "patch", "resolve", "resolved"]
security_keywords = [
    "reentrancy", "access control", "bad randomness", "arithmetic",
    "underflow", "overflow", "denial", "service", "dos", "front", "running",
    "time", "manipulation", "short", "address",
    "entrancy", "unchecked", "calls", "low", "level", "recursive", "ordering",
    "dependency", "condition", "race", "dependence", "timestamp"
]

dasp_keywords = [
    "reentrancy", "access control", "arithmetic", "overflow", "underflow", "bad randomness",
    "front-running", "front running", "transaction order dependency",
    "unchecked low level calls", "denial of service", "dos",
    "time manipulation", "short address"
]


def drop_duplicates():
    """Removes duplicates from the final CSV file."""
    df = pd.read_csv("candidate_commits2.csv", encoding='latin1')
    filtered_commits_unique = df.drop_duplicates(subset=["Commit", "File"], keep="first")
    filtered_commits_unique.to_csv("candidate_commits2.csv", index=False)


def update_vocab():
    """Updates the SpaCy vocabulary to exclude unwanted stop words."""
    nlp.vocab["call"].is_stop = False


def define_security_lemmas():
    """Defines security lemmas based on the provided keywords."""
    lemmas = []
    for keyword in security_keywords:
        lemma_nlp = nlp(keyword.lower())
        for token in lemma_nlp:
            lemmas.append(token.lemma_)
    return lemmas


def contain_fix_dasp(message):
    """Checks if the message contains 'fix' and any DASP lemma."""
    doc = nlp(message.lower())
    message_lower = message.lower()

    lemmata_found = set([token.lemma_ for token in doc if not token.is_stop])

    contains_fix = "fix" in lemmata_found
    contains_dasp = any(keyword in message_lower for keyword in dasp_keywords)

    return contains_fix and contains_dasp


def has_fix_and_security_keywords(message):
    """Checks if a commit message contains both fixing and security lemmas."""
    security_lemmas = define_security_lemmas()
    fixing_lemmas = fixing_keywords  # Directly use fixing_keywords

    doc = nlp(message.lower())
    lemmata_found = set([token.lemma_ for token in doc if not token.is_stop])

    contains_fix = any(lemma in lemmata_found for lemma in fixing_lemmas)
    contains_security = any(lemma in lemmata_found for lemma in security_lemmas)

    contains_fix_dasp = contain_fix_dasp(message)
    return contains_fix or contains_security or contains_fix_dasp


def mine_commit_fixing_vulnerabilities(repo_path):
    """Mines commits that fix vulnerabilities."""
    rows = []
    try:
        for commit in (Repository(repo_path, only_modifications_with_file_types=['.sol'], only_no_merge=True)
                .traverse_commits()):
            modified_files = [file for file in commit.modified_files if file.change_type == ModificationType.MODIFY]

            # Skip commits with more than 3 modified files
            if len(modified_files) > 3:
                continue
            # Check commit messages
            if has_fix_and_security_keywords(commit.msg):
                for modified_file in modified_files:
                    try:
                        if modified_file.source_code_before is None:
                            before = ''
                        else:
                            before = modified_file.source_code_before

                        if '.sol' in modified_file.filename and '.t.sol' not in modified_file.filename:
                            row = {
                                "Commit": commit.hash,
                                "File": modified_file.filename,
                                "Message": commit.msg,
                                "Before": before,
                                "After": modified_file.source_code,
                                "URL": repo_path,
                                "Tag1": '',
                                "Tag2": ''
                            }
                            rows.append(row)
                    except Exception as ex:
                        print("Error processing modified file:", ex)

        # Write data to the CSV file
        csv_file = 'candidate_commits.csv'
        fieldnames = ["Commit", "File", "Message", "Before", "After", "URL", "Tag1", "Tag2"]

        with open(csv_file, 'a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)

            if file.tell() == 0:
                writer.writeheader()

            writer.writerows(rows)

        drop_duplicates()

    except Exception as ex:
        print("Exception during mining:", ex)


def main():
    update_vocab()

    try:
        df = pd.read_csv("solidity_repos_filtered.csv")
    except pd.errors.ParserError as e:
        print("Error parsing the CSV file:", e)
        return

    for index, row in df.iterrows():
        url = row["url"]
        print("Analyzing repository:", url)
        mine_commit_fixing_vulnerabilities(url)


if __name__ == '__main__':
    main()
