import requests

# A Census API URL always had this shape:
# https://api.census.gov/data/{year}/{dataset}?get={variables}&for={geography}

YEAR = 2020
DATASET = "dec/pl"
URL = f"https://api.census.gov/data/{YEAR}/{DATASET}"
API_KEY = "d4ed7255c38ce7cce82b7f2bc52856d08388a5d1"

params = {
    "get": "NAME,P1_001N",   # NAME = State name, B01003_001E = total population
    "for": "state:*",            # means "every state"
    "key": API_KEY,
}

response = requests.get(URL, params=params)

print(response)
if response.status_code == 200:
    print(f"Request failed ({response.status_code})")
    print(response.text)
    raise SystemExit(1)

data = response.json()

# The API returns a list of lists. The first row is the column h

print(f"Got {len(data) - 1} rows back.")

for i in data:
    print(i)