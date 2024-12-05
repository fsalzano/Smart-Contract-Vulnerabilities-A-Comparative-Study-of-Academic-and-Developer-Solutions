# Assuming the DataFrame `new_fixes` has been created and all filtered DataFrames are defined
import pandas as pd

# Simulating the loaded DataFrame
df = pd.read_csv("../sample_of_interest/relevant_commits.csv")

# Filter rows where "IsEmployableFixTag" is True
new_fixes = df[df["IsEmployableFixTag"] == True]

front_running = new_fixes[new_fixes["Tag"] == "Front-Running"]
arithmetic = new_fixes[new_fixes["Tag"] == "arithmetic"]
access_control = new_fixes[new_fixes["Tag"] == "access control"]
bad_randomness = new_fixes[new_fixes["Tag"] == "bad randomness"]
dos = new_fixes[new_fixes["Tag"] == "denial of service"]
short_address = new_fixes[new_fixes["Tag"] == "short addresses attack"]
reentrancy = new_fixes[new_fixes["Tag"] == "reentrancy"]
time_manipulation = new_fixes[new_fixes["Tag"] == "time manipulation"]
unchecked = new_fixes[new_fixes["Tag"] == "Unchecked Return Values For Low Level Calls"]

vulnerability_in_exam = "reentrancy"


if vulnerability_in_exam == "Front-Running":
    print(f"Iterating over DataFrame for: Front-Running")
    for index, row in front_running.iterrows():
        print(row["URL"] + "/commits/" + row["Commit"])
elif vulnerability_in_exam == "arithmetic":
    print(f"Iterating over DataFrame for: arithmetic")
    for index, row in arithmetic.iterrows():
        print(row["URL"] + "/commits/" + row["Commit"])
elif vulnerability_in_exam == "access control":
    print(f"Iterating over DataFrame for: access control")
    for index, row in access_control.iterrows():
        print(row["URL"] + "/commits/" + row["Commit"])
elif vulnerability_in_exam == "bad randomness":
    print(f"Iterating over DataFrame for: bad randomness")
    for index, row in bad_randomness.iterrows():
        print(row["URL"] + "/commits/" + row["Commit"])
elif vulnerability_in_exam == "denial of service":
    print(f"Iterating over DataFrame for: denial of service")
    for index, row in dos.iterrows():
        print(row["URL"] + "/commits/" + row["Commit"])
elif vulnerability_in_exam == "short addresses attack":
    print(f"Iterating over DataFrame for: short addresses attack")
    for index, row in short_address.iterrows():
        print(row["URL"] + "/commits/" + row["Commit"])
elif vulnerability_in_exam == "reentrancy":
    print(f"Iterating over DataFrame for: reentrancy")
    for index, row in reentrancy.iterrows():
        print(row["URL"] + "/commits/" + row["Commit"])
elif vulnerability_in_exam == "time manipulation":
    print(f"Iterating over DataFrame for: time manipulation")
    for index, row in time_manipulation.iterrows():
        print(row["URL"] + "/commits/" + row["Commit"])
elif vulnerability_in_exam == "Unchecked Return Values For Low Level Calls":
    print(f"Iterating over DataFrame for: Unchecked Return Values For Low Level Calls")
    for index, row in unchecked.iterrows():
        print(row["URL"] + "/commits/" + row["Commit"])
else:
    print(f"No matching DataFrame found for: {vulnerability_in_exam}")
