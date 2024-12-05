import pandas as pd

df = pd.read_csv('../sample_of_interest/relevant_commits.csv')
count = 0

for index, row in df.iterrows():
    # releveant = row["IsInLiteratureTag"]
    #
    # if str(releveant) == "True":
    #     continue
    tag1 = str(row['Tag1'])
    tag2 = str(row['Tag2'])

    if tag1 != tag2:
        print(tag1)
        print(tag2)
        count = count + 1


print(count)
# Stampa i valori discordanti
# print(discordanti["Tag1"], discordanti["Tag2"])
