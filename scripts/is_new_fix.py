import pandas as pd
import webbrowser

# Define the tagger
tag = 'Tag1'


def get_diff_in_browser(row):
    base_url = ('https://diff2html.xyz/demo?matching=none&matchWordsThreshold=0.25&maxLineLengthHighlight='
                '10000&diffStyle=word&colorScheme=light&renderNothingWhenEmpty=0&matchingMaxComparisons='
                '2500&maxLineSizeInBlockForComparison=200&outputFormat=side-by-side&drawFileList=1&'
                'synchronisedScroll=1&highlight=1&fileListToggle=1&fileListStartVisible=0&highlightLanguages='
                '[object%20Map]&smartSelection=1&fileContentToggle=1&stickyFileHeaders=1&diff=')
    url = row["URL"]
    commit = row["Commit"]
    full_url = f"{base_url}{url}/commit/{commit}"
    print("Opening diff in browser...")
    webbrowser.open(full_url)


def main():
    path = '../sample_of_interest/relevant_commits.csv'
    df = pd.read_csv(path)

    # Iterate through each row
    for index, row in df.iterrows():
        is_new_employable_fix = row["IsNewEmployableFix"]
        print(f"res: {is_new_employable_fix}")

        if str(row["IsNewEmployableFix"]) == "False":
            continue

        is_in_literature = row["IsInLiteratureTag"]
        print(f"is_in_literature: {is_in_literature}")

        if not str(is_in_literature) == "False":
            continue
        # Determine which column to write the result to based on the tag
        if tag == 'Tag1':
            relevant_column = 'IsEmployableFixTag1'
        elif tag == 'Tag2':
            relevant_column = 'IsEmployableFixTag2'
        else:
            print(f"Unexpected value in 'Tag1' for row {index}: {row['Tag1']}")
            continue

        # Check if the column is already filled (i.e., not NaN or empty)
        if pd.notna(row[relevant_column]) and row[relevant_column] != "":
            print(f"Row {index} already has a value in {relevant_column}, skipping.")
            continue

        # Ask for user input after the browser is opened
        try:
            label = row["Tag"]
            print(f"assigned vulenrability: {label}")
            # FIxme insert your dasp class here
            if label.strip().lower() == 'arithmetic':


                # Open the browser before asking for user input
                get_diff_in_browser(row)
                link = row["URL"] + '/commits/' + row["Commit"]
                message = row["Message"]
                print(f"Tag assigned: {label}")
                print(f"Commit message: {message}")
                print(f"Check on GitHub: {link}")

                user_input = input(f"Enter 1 if the change is a new and employable fix, 2 otherwise, or 's' to skip for {tag}: ")

                if user_input == 's':
                    print(f"Row {index} skipped.")
                    continue  # Skip this row and proceed to the next one
                elif user_input == '1':
                    df.at[index, relevant_column] = "True"
                elif user_input == '2':
                    df.at[index, relevant_column] = "False"
                elif user_input == '3':
                    df.at[index, relevant_column] = "DROP"
                else:
                    print("Invalid input. Skipping this row.")
                    continue  # Skip if the input is not valid

                # Save the entire DataFrame back to the CSV after updating the current row
                df.to_csv(path, index=False)
                print(f"Row {index} updated and saved to {path}")
                print(df.loc[index])

        except ValueError:
            print("Invalid input. Skipping this row.")
            continue


if __name__ == "__main__":
    main()
