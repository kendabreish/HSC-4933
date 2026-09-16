import requests

# Census API information
YEAR = 2023
DATASET = "acs/acs5"
URL = f"https://api.census.gov/data/{YEAR}/{DATASET}"
API_KEY = "fb540bd7012156687dd3d45a5a09d7ec26522a39"

# Ask user for state FIPS codes
print("Census Population Lookup")
print("------------------------")
print("Examples: 06 = California, 12 = Florida, 36 = New York")
state_codes = input("Enter the State FIPS code:").strip()

# Ask user for variable name
variables = input("Enter the variable names that you would like data for:").strip()

# Build API request
params = {
    "get": f"NAME,{variables}",
    "for": f"state:{state_codes}",
    "key": API_KEY,
}

# Send request
response = requests.get(URL, params=params)

print(response.url)
print(response)

# Process response
if response.status_code != 200:
    print(f"Request failed ({response.status_code})")
    print(response.text)
    raise SystemExit(1)

data = response.json()

print(f"Got {len(data) -1} rows back.")

for i in data:
    print(i)