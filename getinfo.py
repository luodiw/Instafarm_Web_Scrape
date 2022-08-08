import json
import requests
import re

# Load the vendors file
with open("vendors.json") as f:
    vendors = json.load(f)

contact = []

# NOTE: The contact numbers might be invalid because regex can consider normal number as a phone number
# To avoid this, I'm planning to fetch text from `p`, `div`, and `span` tags and use them.
"""
all_text = []

# Get all text from tags in the HTML - `p` and `div` and `span`
for elem in soup.find_all(['p', 'div', 'span']):
    # If current element doesn't have nested element and only text, append it
    if not elem.find_all(['p', 'div', 'span']):
        all_text.append(elem.text)
"""

# Go through all vendors
for vendor in vendors:
    # Visit the URL
    req = requests.get(vendor["url"]).text

    # Get the contact number from HTML using regex
    phr = r"[\+\(]?[1-9][0-9 \-\(\)]{8,10}[0-9]"
    contact_number = re.search(phr, req)

    # If there's a contact number, add it to the list
    contact_number = contact_number.group(0) if contact_number else None

    # Get the email from HTML using regex
    emr = r"[\w.+-]+@[\w-]+\.[\w.-]+"
    email = re.search(emr, req)

    email = email.group(0) if email else None

    # Get the address from HTML using regex
    addr = r"^(\d+) ?([A-Za-z](?= ))? (.*?) ([^ ]+?) ?((?<= )APT)? ?((?<= )\d*)?$"
    address = re.search(addr, req)

    address = address.group(0) if address else None

    # Add the contact info to the list
    contact.append(
        {
            "vendor": vendor["vendor"],
            "contact_number": contact_number,
            "email": email,
            "address": address,
        }
    )


# Save the contact info to `contact.json`
with open("contact.json", "w") as f:
    json.dump(contact, f)
