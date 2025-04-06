import pandas as pd
import json

# Load the dataset
df = pd.read_csv('fix_survivability_analysis.csv')

# Iterate through the DataFrame rows
for index, row in df.iterrows():
    if row['is_fixing'] == True:
        added_lines = list()

        diff = row['diff']
        for line in diff.splitlines():
            line = line.strip()
            if line.startswith('+') and not line.startswith('+++'):
                # Remove the '+' sign and add to the set
                added_lines.append(line[1:].strip())

                added_lines = list(added_lines)  # Make sure it's a list, not a set
                df.at[index, 'added_lines_when_fixing'] = json.dumps(added_lines)
    else:
        added_lines = list(added_lines)
        df.at[index, 'added_lines_when_fixing'] = json.dumps(added_lines)
        df.at[index, 'is_fixing'] = False

df.to_csv('fix_survivability_analysis.csv', index=False)

df = pd.read_csv('fix_survivability_analysis.csv')
last_to_check_lines=[]

for index, row in df.iterrows():
    is_fixing = row['is_fixing']
    after = row["after"]

    if not is_fixing:
        after = row['after']
        added_lines_when_fixing = row['added_lines_when_fixing']
        lines = json.loads(added_lines_when_fixing)

        to_check_lines = []

        for l in lines:

            if l.strip():  # Skip empty strings
                if l not in after:
                    to_check_lines.append(l)

        if len(to_check_lines) > 0:
            print('*' * 50)

            print(last_to_check_lines)
            print(to_check_lines)
            print('*' * 50)
            if last_to_check_lines != to_check_lines:
                last_to_check_lines = to_check_lines
                df.at[index, 'lines_to_check'] = json.dumps(to_check_lines)
                df.at[index, 'is_changed'] = True
            else:
                df.at[index, 'is_changed'] = False

df['is_changed'] = df['is_changed'].fillna(False)
df.to_csv('fix_survivability_analysis.csv', index=False)
