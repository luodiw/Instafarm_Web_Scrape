import json
import os

import requests
from bs4 import BeautifulSoup
from serpapi import GoogleSearch

req = requests.get("https://www.schenectadygreenmarket.com/meet-our-vendors").text
soup = BeautifulSoup(req, "lxml")

vendors = []
vendor_urls = []

for elem in soup.find_all("div", class_="image-slide-title"):
    vendors.append(elem.text)

# print(vendors[:5])

key = os.getenv("SERPAPI_KEY")

for vendor in vendors:
    search = GoogleSearch(
        {
            "api_key": key,
            "engine": "google",
            "q": vendor + " market",
            "gl": "us",
            "hl": "en",
        }
    )
    results = search.get_dict()

    print(results["organic_results"][0]["title"], results["organic_results"][0]["link"])

    for result in results["organic_results"]:
        # If the link is `instagram.com` or `facebook.com`, save it
        if result["link"].startswith("https://www.instagram.com") or result[
            "link"
        ].startswith("https://www.facebook.com"):
            vendor_urls.append({"vendor": vendor, "url": result["link"]})
            break

        # If the link has a slash, ensure there's nothing after that
        elif "/" in result["link"]:
            if result["link"].split("/")[-1] == "":
                vendor_urls.append({"vendor": vendor, "url": result["link"]})
                break
        # Else, go to next result
        else:
            continue


# Save vendors and vendor urls to `vendors.json`
with open("vendors.json", "w") as f:
    json.dump(vendor_urls, f)
