import json
import os

import requests
from bs4 import BeautifulSoup
from serpapi import GoogleSearch


def remove_duplicate(values):
    seen = set()

    for x in values:
        elems = tuple(x.items())
        if elems not in seen:
            yield x
            seen.add(elems)


# In-place data append
def append_data(vendors: list, results: dict) -> None:
    for res in results["local_results"]:
        vendors.append(
            {
                "vendor": res["title"],
                "type": res["type"],
                "website": res.get("website"),
                "address": res.get("address"),
                "phone": res.get("phone"),
            }
        )


term = "Farm Schenectady, NY"
ll = "@39.3619308,-163.6770291,3z"  # get this from google maps

key = os.getenv("SERPAPI_KEY")

search = GoogleSearch(
    {"api_key": key, "engine": "google_maps", "q": term, "type": "search"}
)
results = search.get_dict()

vendors = []
count = 1

# Initial data append
append_data(vendors, results)
# If the results has `['serpapi_pagination']['next']`, visit that page
while results.get("serpapi_pagination").get("next"):
    req = requests.get(
        results["serpapi_pagination"]["next"] + f"&api_key={key}&ll={ll}"
    ).json()
    print("page", count)

    append_data(vendors, req)
    count += 1

    # cap for now
    if count == 200:
        break

# Remove all entries with `type` != `Farm`
vendors = [v for v in vendors if v["type"] == "Farm"]

# Remove all duplicate entries by vendor key value
vendors = list(remove_duplicate(vendors))


with open("vendors-map.json", "w") as f:
    json.dump(vendors, f)
