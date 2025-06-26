"""
Author: Nelson Durrant
Date: April 2025

This script checks the Utah Division of Wildlife Resources (UDWR) website for new stocking data.
It compares the current data with previously saved data to identify new stocking events.
"""

import requests
from bs4 import BeautifulSoup
import pickle
import sys
import os
from collections import Counter
import datetime

# Define constants for data file, target county, and website URL
DATA_FILE = "data.pickle"
TARGET_COUNTY = "UTAH"
CURRENT_YEAR = datetime.datetime.now().year
URL = f"https://dwrapps.utah.gov/fishstocking/Fish?y={CURRENT_YEAR}"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
}

# Navigate to the directory of the script for consistent file access
try:
    script_directory = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_directory)
except OSError as e:
    print()
    print(f"[ERROR] Could not change directory.")
    print()
    sys.exit(1)

# Load previously saved fish stocking data
saved_counts = {}
try:
    with open(DATA_FILE, "rb") as file:
        saved_counts = pickle.load(file)
except FileNotFoundError:
    pass  # File not found, will create a new one
except EOFError:
    pass  # File is empty, will create a new one
except Exception as e:
    print()
    print(f"[ERROR] Could not load data from '{DATA_FILE}'.")
    print()
    sys.exit(1)

# Fetch the current fish stocking data from the UDWR website
try:
    response = requests.get(URL, headers=HEADERS, timeout=1)
    response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
except requests.exceptions.RequestException as e:
    print()
    print(f"[ERROR] Could not connect to UDWR website.")
    print()
    sys.exit(1)
except requests.exceptions.Timeout:
    print()
    print(f"[ERROR] Connection to UDWR website timed out.")
    print()
    sys.exit(1)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.text, "lxml")
current_counts = Counter()
found_rows = False

# Find all table rows with the specified class
table_rows = soup.find_all("tr", class_="table1")

# Iterate through each table row to extract relevant data
for row in table_rows:
    county_cell = row.find("td", class_="county")
    water_cell = row.find("td", class_="watername")

    # Check if both county and water name cells exist in the row
    if county_cell and water_cell:
        found_rows = True
        county_name = county_cell.get_text(strip=True)
        water_name = water_cell.get_text(strip=True)

        # Check if the county matches the target county
        if county_name == TARGET_COUNTY:
            current_counts[water_name] += 1

# Compare current data with previously saved data
print()
found_update = False
updated_locations = []

# Iterate through the current counts and compare with saved counts
for water, current_count in current_counts.items():
    saved_count = saved_counts.get(
        water, 0
    )  # Default to 0 if the water body was not in the saved data
    if current_count > saved_count:
        diff = current_count - saved_count
        plural = "s" if diff > 1 else ""
        updated_locations.append(f"{water} has {diff} new stocking event{plural}!")
        found_update = True

# Print the comparison results
if found_update:
    print(f"[INFO] New UDWR fish stocking data found! 🎣")
    for update_msg in updated_locations:
        print(f"- {update_msg}")
    print(f"\n{URL}")

    # Ask the user if they want to update the data
    user_choice = input("\nDo you want to save this new data? (y/n): ").strip().lower()
    if user_choice == "y":
        try:
            with open(DATA_FILE, "wb") as file:
                pickle.dump(dict(current_counts), file)
            print("\n[INFO] UDWR fish stocking data updated successfully!")
        except Exception as e:
            print(f"\n[ERROR] Could not save data to '{DATA_FILE}'. Error: {e}")
    else:
        print("\n[INFO] New data not saved.")
else:
    print(f"[INFO] No new UDWR fish stocking data found. 🎣")

print()
