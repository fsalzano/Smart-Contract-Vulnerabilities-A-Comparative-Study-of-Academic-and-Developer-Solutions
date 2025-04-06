import json
import re
from collections import defaultdict

try:
    with open("search_results.json", "r") as json_file:
        data = json.load(json_file)
        print("\nSaved results:")

        word_counter = defaultdict(int)

        merge_mapping = {
            "arithmetic": "arithmetic",
            "overflow": "arithmetic",
            "underflow": "arithmetic",
            "front running": "front running",
            "transaction order dependency": "front running",
            "DoS": "denial of service",
            "low level": "unchecked",
            "low-level": "unchecked",
            "low level call": "unchecked",
            "low level calls": "unchecked",
        }

        for query, count in data.items():
            match = re.findall(r'"(.*?)"', query)
            if len(match) >= 2:
                extracted_word = match[1]  # Second word between quotes
                merged_key = merge_mapping.get(extracted_word, extracted_word)  # Merge synonyms
                word_counter[merged_key] += count
                print(f"{query}: {count} | Extracted: {extracted_word} (Mapped to: {merged_key})")
            else:
                print(f"{query}: {count} | Extracted: Not available")

        print("\nAggregated count by extracted word:")
        for word, total_count in word_counter.items():
            print(f"{word}: {total_count}")

except FileNotFoundError:
    print("Error: The file 'search_results.json' does not exist. Make sure to run the search first.")
except json.JSONDecodeError:
    print("Error: The file 'search_results.json' is not a valid JSON.")
