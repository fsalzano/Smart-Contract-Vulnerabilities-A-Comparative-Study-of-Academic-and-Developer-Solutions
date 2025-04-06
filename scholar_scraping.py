import requests
import json


def search_google_scholar(query):
    api_key = "YOUR_KEY!"
    url = "https://serpapi.com/search"

    params = {
        "engine": "google_scholar",
        "q": f"allintitle: {query}",
        "api_key": api_key
    }

    response = requests.get(url, params=params)
    data = response.json()

    titles = []
    if "organic_results" in data:
        count = len(data["organic_results"])
        titles = [article["title"] for article in data["organic_results"]]
        print(f"Number of articles found for '{query}': {count}")
        return count, titles
    else:
        print(f"No results found for '{query}' or an error occurred during the request.")
        return 0, []


if __name__ == "__main__":
    queries = []

    # Base search queries targeting smart contract vulnerabilities
    base_queries = [
        '"smart contracts" "access control" "vulnerability"',
        '"smart contracts" "arithmetic" "vulnerability"',
        '"smart contracts" "overflow" "vulnerability"',
        '"smart contracts" "reentrancy" "vulnerability"',
        '"smart contracts" "bad randomness" "vulnerability"',
        '"smart contracts" "DoS" "vulnerability"',
        '"smart contracts" "denial of service" "vulnerability"',
        '"smart contracts" "front running" "vulnerability"',
        '"smart contracts" "transaction order dependency" "vulnerability"',
        '"smart contracts" "time manipulation" "vulnerability"',
        '"smart contracts" "short address" "vulnerability"',
        '"smart contract" "access control" "vulnerability"',
        '"smart contract" "arithmetic" "vulnerability"',
        '"smart contract" "overflow" "vulnerability"',
        '"smart contract" "reentrancy" "vulnerability"',
        '"smart contract" "bad randomness" "vulnerability"',
        '"smart contract" "DoS" "vulnerability"',
        '"smart contract" "denial of service" "vulnerability"',
        '"smart contract" "front running" "vulnerability"',
        '"smart contract" "transaction order dependency" "vulnerability"',
        '"smart contract" "time manipulation" "vulnerability"',
        '"smart contract" "short address" "vulnerability"',
        '"smart contract" "low level call" "vulnerability"',

        '"smart contract" "overflow"',
        '"smart contract" "arithmetic"',
        '"smart contracts" "overflow"',
        '"smart contracts" "arithmetic"',

        '"smart contracts" "low level call" "vulnerability"',
        '"smart contracts" "low level calls" "vulnerability"',
        '"smart contracts" "low-level"',
        '"smart contracts" "low level"',
    ]

    # Add variants replacing "vulnerability" with "vulnerabilities"
    for query in base_queries:
        queries.append(query)
        queries.append(query.replace("vulnerability", "vulnerabilities"))

    results = {}
    all_titles = []

    # Perform the search and store the results
    for q in queries:
        count, titles = search_google_scholar(q)
        results[q] = count
        all_titles.extend(titles)

    # Save results to JSON
    with open("search_results.json", "a") as json_file:
        json.dump(results, json_file, indent=4)

    # Save article titles to TXT
    with open("article_titles.txt", "a") as txt_file:
        for title in all_titles:
            txt_file.write(title + "\n")

    # Print final summary
    for query, count in results.items():
        print(f"{query}: {count}")
