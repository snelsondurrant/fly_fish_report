#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import pickle
import sys
import os
import subprocess
from collections import Counter
import datetime

DATA_FILE = "data.pickle"
TARGET_COUNTY = "UTAH"
CURRENT_YEAR = datetime.datetime.now().year
URL = f"https://dwrapps.utah.gov/fishstocking/Fish?y={CURRENT_YEAR}"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36"
}

try:
    script_directory = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_directory)
except OSError as e:
    print()
    print(f"[ERROR] Could not change directory.")
    print()
    sys.exit(1)

try:
    subprocess.run(["git", "pull"], check=True, capture_output=True, text=True)
except subprocess.CalledProcessError as e:
    print(f"[WARNING] Could not pull from GitHub: {e}")

saved_counts = {}
try:
    with open(DATA_FILE, "rb") as file:
        saved_counts = pickle.load(file)
except FileNotFoundError:
    pass
except EOFError:
    pass
except Exception as e:
    print()
    print(f"[ERROR] Could not load data from '{DATA_FILE}'.")
    print()
    sys.exit(1)

try:
    response = requests.get(URL, headers=HEADERS, timeout=1)
    response.raise_for_status()
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

soup = BeautifulSoup(response.text, "lxml")
current_counts = Counter()
found_rows = False

table_rows = soup.find_all("tr", class_="table1")

for row in table_rows:
    county_cell = row.find("td", class_="county")
    water_cell = row.find("td", class_="watername")

    if county_cell and water_cell:
        found_rows = True
        county_name = county_cell.get_text(strip=True)
        water_name = water_cell.get_text(strip=True)

        if county_name == TARGET_COUNTY:
            current_counts[water_name] += 1

print()
found_update = False
updated_locations = []

for water, current_count in current_counts.items():
    saved_count = saved_counts.get(
        water, 0
    )
    if current_count > saved_count:
        diff = current_count - saved_count
        plural = "s" if diff > 1 else ""
        updated_locations.append(f"{water} has {diff} new stocking event{plural}!")
        found_update = True

if found_update:
    print(f"[INFO] New UDWR fish stocking data found! 🎣")
    for update_msg in updated_locations:
        print(f"- {update_msg}")
    print(f"\n{URL}")

    user_choice = input("\nDo you want to save this new data? (y/n): ").strip().lower()
    if user_choice == "y":
        try:
            with open(DATA_FILE, "wb") as file:
                pickle.dump(dict(current_counts), file)
            print("\n[INFO] UDWR fish stocking data updated successfully!")
            
            try:
                subprocess.run(["git", "add", DATA_FILE], check=True, capture_output=True, text=True)
                subprocess.run(["git", "commit", "-m", "Update fish stocking data"], check=True, capture_output=True, text=True)
                subprocess.run(["git", "push"], check=True, capture_output=True, text=True)
            except subprocess.CalledProcessError as e:
                print(f"[WARNING] Could not push to GitHub: {e}")

        except Exception as e:
            print(f"\n[ERROR] Could not save data to '{DATA_FILE}'. Error: {e}")
    else:
        print("\n[INFO] New data not saved.")
else:
    print(f"[INFO] No new UDWR fish stocking data found. 🎣")

print()
