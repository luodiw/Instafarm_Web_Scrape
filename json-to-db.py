import json
import psycopg

with open("vendors-map.json") as f:
    vendors = json.load(f)

# Convert the dicts to tuples
vendors = [tuple(v.values()) for v in vendors]

# Connect to a DB
conn = psycopg.connect(
    dbname="vendortest", user="postgres", password="12345678", host="localhost"
)

with conn.cursor() as curr:
    # Create the vendors table - Vendor, type, address, website, phone
    curr.execute(
        """CREATE TABLE IF NOT EXISTS vendors (
        vendor VARCHAR(255) NOT NULL,
        type VARCHAR(255) NOT NULL,
        address VARCHAR(255),
        website VARCHAR(255),
        phone VARCHAR(255)
    )"""
    )

    # Insert the vendors into the table
    curr.executemany(
        """INSERT INTO vendors (vendor, type, address, website, phone)
        VALUES (%s, %s, %s, %s, %s)""",
        vendors,
    )

    # Commit the changes
    conn.commit()
