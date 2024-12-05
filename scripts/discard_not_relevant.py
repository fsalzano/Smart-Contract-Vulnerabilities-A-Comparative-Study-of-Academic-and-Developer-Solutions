import csv
import pandas as pd
# List of input datasets
path = "../sample_of_interest/sample_of_interest_commit_relevance.csv"

# Name of the output CSV file
output_file = "../sample_of_interest/relevant_commits.csv"

# Initialize the header_written flag
header_written = False

# Open the output file for writing
with open(output_file, 'w', newline='') as outfile:
    writer = csv.writer(outfile)

    # Open the input file for reading
    with open(path, 'r') as infile:
        reader = csv.reader(infile)
        header = next(reader)  # Read the header

        # Write the header to the output file if not written yet
        if not header_written:
            writer.writerow(header)
            header_written = True

        # Iterate over each row in the input file
        for row in reader:
            # Check the values of Tag1 and Tag2
            tag = row[header.index('Tag')]

            # If both Tag1 and Tag2 are not "Not relevant", write the row to the output file
            if tag != "Not Relevant":
                writer.writerow(row)

print(f"Filtered rows written to {output_file}")

print(pd.read_csv(output_file).shape)


