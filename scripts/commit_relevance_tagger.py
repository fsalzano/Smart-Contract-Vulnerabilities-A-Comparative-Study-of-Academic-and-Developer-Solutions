import pandas as pd

path = "../sample_of_interest/4600-5600.csv"
tagger = 'Tag1'


def print_messages_and_get_input(row, df, index):
    global tagger

    if tagger == 'Tag1' and pd.notna(row["Tag1"]):
        print('skip')
        return df

    if tagger == 'Tag2' and pd.notna(row["Tag2"]):
        return df

    dasp_categories = [
        "Reentrancy",
        "Access Control",
        "Arithmetic Issues",
        "Unchecked Return Values For Low Level Calls",
        "Denial of Service",
        "Bad Randomness",
        "Front-Running",
        "Time manipulation",
        "Short Address Attack",
        "Not Relevant"
    ]

    # Stampa in verde il messaggio e il file
    print(f"\033[92m\nMessage: {row['Message']}, File: {row['File']}\033[0m")
    print(row["URL"] + '/commit/' + row["Commit"])

    print("\nDASP Categories:")
    for i, category in enumerate(dasp_categories):
        print(f"{i}: {category}")

    while True:
        try:
            user_input = int(input("\nEnter a number corresponding to one of the DASP categories (0-9): "))
            if 0 <= user_input < len(dasp_categories):
                break
            else:
                print("Invalid input. Please enter a number between 0 and 9.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    selected_category = dasp_categories[user_input]
    if tagger == 'Tag1':
        df.at[index, 'Tag1'] = selected_category
    if tagger == 'Tag2':
        df.at[index, 'Tag2'] = selected_category
    print(f"\nYou selected: {selected_category}")
    return df


df = pd.read_csv(path)
#print(df.shape)

for index, row in df.iterrows():
    df = print_messages_and_get_input(row, df, index)
    df.to_csv(path, index=False)
