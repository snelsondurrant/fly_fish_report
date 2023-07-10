import requests
from bs4 import BeautifulSoup

url = "https://dwrapps.utah.gov/fishstocking/Fish?y=2023"
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "lxml")

print()
print("Running web crawler to check for UDWR fishing updates...")

if str(soup).count("VIVIAN PARK P") > 4:
    print("Vivian Park Pond has been stocked! (new stock count: " + str(str(soup).count("VIVIAN PARK P")) + ")")

if str(soup).count("PROVO R") > 2:
    print("The Provo River has been stocked! (new stock count: " + str(str(soup).count("PROVO R")) + ")")

if str(soup).count("HOBBLE CR") > 0:
    print("Hobble Creek has been stocked! (new stock count: " + str(str(soup).count("HOBBLE CR")) + ")")

print()
