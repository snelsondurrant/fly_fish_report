'''
:author: Nelson Durrant
:date: Apr 2025

This script checks the Utah Division of Wildlife Resources (UDWR) website for new fly fishing data
'''

import requests
from bs4 import BeautifulSoup
import pickle
import sys
import os
from collections import Counter
import datetime

DATA_FILE = "data.pickle"
TARGET_COUNTY = "UTAH"
CURRENT_YEAR = datetime.datetime.now().year
URL = f"https://dwrapps.utah.gov/fishstocking/Fish?y={CURRENT_YEAR}"
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

# Navigate to this file's directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Load the previously saved data
try:
    with open(DATA_FILE, "rb") as file:
        saved_counts = pickle.load(file)
except (FileNotFoundError, EOFError):
    saved_counts = {} # Initialize if file doesn't exist or is empty

# Get the current data from the UDWR website
try:
    response = requests.get(URL, headers=HEADERS, timeout=10)
    response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
except (requests.RequestException, requests.exceptions.Timeout) as e:
    print()
    print(f"[ERROR] Could not connect to UDWR website: {e}")
    print()
    sys.exit(1) # Exit if we can't get data

# Parse the HTML response
soup = BeautifulSoup(response.text, "lxml")
current_counts = Counter()
found_rows = False

table_rows = soup.find_all('tr', class_='table1')

for row in table_rows:
    county_cell = row.find('td', class_='county')
    water_cell = row.find('td', class_='watername')

    if county_cell and water_cell:
        found_rows = True
        county_name = county_cell.get_text(strip=True)
        water_name = water_cell.get_text(strip=True)

        if county_name == TARGET_COUNTY:
            current_counts[water_name] += 1

# Check for update request
if len(sys.argv) > 1 and sys.argv[1] == "--update":
    with open(DATA_FILE, "wb") as file:
        pickle.dump(dict(current_counts), file)

    print()
    print("UDWR fly fishing data updated successfully! 🎣")
    print()

else:

  # Compare current counts with saved counts
  print()
  found_update = False
  updated_locations = []

  # Check for new stocking events or increased counts
  for water, current_count in current_counts.items():
      saved_count = saved_counts.get(water, 0) # Default to 0 if not seen before
      if current_count > saved_count:
          diff = current_count - saved_count
          plural = "s" if diff > 1 else ""
          updated_locations.append(f"{water} has {diff} new stocking event{plural}!")
          found_update = True

  # Print the results
  if found_update:
      print(f"New UDWR fly fishing data found! 🎣")
      for update_msg in updated_locations:
          print(f"- {update_msg}")
      print(f"\nDetails: {URL}")
      print("\nRun `python fishing.py --update` to save the new data.")
  else:
      print(f"No new UDWR fly fishing data found. 🎣")

  print()