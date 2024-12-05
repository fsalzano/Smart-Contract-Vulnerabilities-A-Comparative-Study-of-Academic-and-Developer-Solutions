import pandas as pd

# Read the CSV file
file_path = "../sample_of_interest/sample_of_interest_commit_relevance.csv"
df = pd.read_csv(file_path)
print(df.shape)

# Iterate through the rows
for index, row in df.iterrows():


    # Check if Tag1 is different from Tag2 and if Tag is NaN
    if row["Tag1"] != row["Tag2"] and pd.isna(row["Tag"]):
        # Print the message in green using ANSI escape codes
        print(f"\033[92m\nMessage: {row['Message']}\033[0m")  # Green color for Message


        # Print Tag1 in blue and Tag2 in yellow using ANSI escape codes
        print(
            f"Tag1: \033[94m{row['Tag1']}\033[0m, Tag2: \033[93m{row['Tag2']}\033[0m")  # Blue for Tag1, Yellow for Tag2
        print(row["URL"]+"/commits/"+row["Commit"])
        # Ask for input: 1 or 2
        user_input = input("Choose the correct tag value for 'Tag' (1 for Tag1, 2 for Tag2): ")

        # Update 'Tag' based on input
        if user_input == '1':
            df.at[index, 'Tag'] = row["Tag1"]
        elif user_input == '2':
            df.at[index, 'Tag'] = row["Tag2"]
        else:
            print("Invalid input. Skipping this row.")

        # Save the DataFrame after each update
        df.to_csv(file_path, index=False)
        print(f"Row {index} updated and file saved.\n")

print("All updates completed.")
