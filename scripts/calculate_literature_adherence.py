import pandas as pd
import matplotlib.pyplot as plt

# Read the CSV file
df = pd.read_csv('../sample_of_interest/relevant_commits.csv')

# Count the occurrences of True and False in the IsInLiteratureTag column
counts = df['IsInLiteratureTag'].value_counts()

# Get the count of True values
true_count = counts.get(True, 0)

# Get the total count of values in the IsInLiteratureTag column
total_count = df['IsInLiteratureTag'].count()

# Calculate the percentage of True values out of the total
true_percentage = (true_count / total_count) * 100

# Print the results
print(f"True count: {true_count}")
print(f"Total count: {total_count}")
print(f"Percentage of True values: {true_percentage:.2f}%")

# Calculate percentage of True values for each category in the 'Tag' column
grouped = df.groupby('Tag')['IsInLiteratureTag'].value_counts(normalize=True).unstack().fillna(0)

# Print the percentage of True values for each category in the 'Tag' column
for tag, values in grouped.iterrows():
    true_percentage = values.get(True, 0) * 100
    print(f"Tag: {tag} - Percentage of True values: {true_percentage:.2f}%")

# Extract tags and their respective True percentages
tags = grouped.index
true_percentages = [values.get(True, 0) * 100 for _, values in grouped.iterrows()]

# Filter tags with non-zero True percentages
filtered_tags = [tag.capitalize() for tag, percentage in zip(tags, true_percentages) if percentage > 0]
filtered_percentages = [percentage for percentage in true_percentages if percentage > 0]

print('*' * 30)
print(filtered_tags)
filtered_tags[1] = "Unchecked return values\n for low level calls"

# Plot the filtered percentage of True values for each category in the 'Tag' column
plt.figure(figsize=(16, 9))
bars = plt.bar(filtered_tags, filtered_percentages, color='skyblue', width=0.5)  # Adjusted width

# Add percentage labels on top of each bar
for bar, percentage in zip(bars, filtered_percentages):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(),
             f'{percentage:.2f}%', ha='center', va='bottom', fontsize=14)

plt.ylabel('Percentage of Adherence (%)', fontsize=14)
plt.title('Percentage of Literature Guidelines Adherence by Category', fontsize=14)
plt.xticks(rotation=45, ha='right', fontsize=14)
plt.tight_layout()
# plt.show()
plt.savefig("literature_adherence.png")
